"""
ZoomConnect Backend — FastAPI
Main application entry point with all API routes
"""
import random
import string
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext

from models import Base, engine, get_db, User, Meeting, Recording, Channel, ChatMessage, Contact, Webinar
from schemas import (
    UserRegister, UserLogin, Token, UserOut, UserUpdate,
    MeetingCreate, MeetingUpdate, MeetingOut, JoinMeetingRequest,
    RecordingOut, ChannelCreate, ChannelOut, MessageCreate, MessageOut,
    ContactCreate, ContactOut, WebinarCreate, WebinarOut,
)

# ── Config ────────────────────────────────────────────────────────
SECRET_KEY = "zoomconnect-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ZoomConnect API",
    description="Backend API for ZoomConnect — Enterprise Video Conferencing Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve HTML pages directly from parent directory
import os, pathlib
FRONTEND_DIR = pathlib.Path(__file__).parent.parent

# ── Helpers ───────────────────────────────────────────────────────
def generate_meeting_id() -> str:
    digits = "".join(random.choices(string.digits, k=11))
    return f"{digits[:3]} {digits[3:7]} {digits[7:]}"


def generate_passcode() -> str:
    return "".join(random.choices(string.digits, k=6))


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# ── WebSocket Connection Manager ──────────────────────────────────
class ConnectionManager:
    def __init__(self):
        self.active: dict[str, list[WebSocket]] = {}

    async def connect(self, room: str, ws: WebSocket):
        await ws.accept()
        self.active.setdefault(room, []).append(ws)

    def disconnect(self, room: str, ws: WebSocket):
        if room in self.active:
            self.active[room].remove(ws)

    async def broadcast(self, room: str, data: dict):
        for ws in self.active.get(room, []):
            try:
                await ws.send_json(data)
            except Exception:
                pass


manager = ConnectionManager()


# ── Routes: Root / Health ─────────────────────────────────────────
@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "message": "ZoomConnect API is running 🚀", "version": "1.0.0"}


@app.get("/api/health", tags=["health"])
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# ── Routes: Auth ──────────────────────────────────────────────────
@app.post("/api/auth/register", response_model=Token, tags=["auth"])
def register(body: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    pmi = generate_meeting_id()
    user = User(
        display_name=body.display_name,
        email=body.email,
        hashed_password=hash_password(body.password),
        job_title=body.job_title,
        department=body.department,
        personal_meeting_id=pmi,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}


@app.post("/api/auth/login", response_model=Token, tags=["auth"])
def login(body: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}


# ── Routes: User Profile ──────────────────────────────────────────
@app.get("/api/users/me", response_model=UserOut, tags=["users"])
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.patch("/api/users/me", response_model=UserOut, tags=["users"])
def update_me(body: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user


# ── Routes: Meetings ──────────────────────────────────────────────
@app.get("/api/meetings", response_model=List[MeetingOut], tags=["meetings"])
def list_meetings(
    filter: Optional[str] = "upcoming",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Meeting).filter(Meeting.owner_id == current_user.id)
    now = datetime.utcnow()
    if filter == "upcoming":
        q = q.filter(Meeting.start_time >= now)
    elif filter == "previous":
        q = q.filter(Meeting.start_time < now)
    return q.order_by(Meeting.start_time).all()


@app.post("/api/meetings", response_model=MeetingOut, status_code=status.HTTP_201_CREATED, tags=["meetings"])
def create_meeting(body: MeetingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    meeting = Meeting(
        **body.model_dump(),
        meeting_id=generate_meeting_id(),
        passcode=generate_passcode(),
        owner_id=current_user.id,
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting


@app.get("/api/meetings/{meeting_id}", response_model=MeetingOut, tags=["meetings"])
def get_meeting(meeting_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id, Meeting.owner_id == current_user.id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@app.patch("/api/meetings/{meeting_id}", response_model=MeetingOut, tags=["meetings"])
def update_meeting(meeting_id: int, body: MeetingUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id, Meeting.owner_id == current_user.id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(meeting, field, value)
    db.commit()
    db.refresh(meeting)
    return meeting


@app.delete("/api/meetings/{meeting_id}", status_code=204, tags=["meetings"])
def delete_meeting(meeting_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id, Meeting.owner_id == current_user.id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    db.delete(meeting)
    db.commit()


@app.post("/api/meetings/{meeting_id}/start", tags=["meetings"])
def start_meeting(meeting_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id, Meeting.owner_id == current_user.id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    meeting.status = "started"
    db.commit()
    return {"status": "started", "meeting_id": meeting.meeting_id}


@app.post("/api/meetings/join", tags=["meetings"])
def join_meeting(body: JoinMeetingRequest, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.meeting_id == body.meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    if meeting.use_passcode and meeting.passcode != body.passcode:
        raise HTTPException(status_code=403, detail="Invalid passcode")
    return {"status": "joined", "topic": meeting.topic, "meeting_id": meeting.meeting_id, "waiting_room": meeting.waiting_room}


# ── Routes: Recordings ────────────────────────────────────────────
@app.get("/api/recordings", response_model=List[RecordingOut], tags=["recordings"])
def list_recordings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Recording).filter(Recording.host_id == current_user.id).order_by(Recording.recorded_at.desc()).all()


@app.delete("/api/recordings/{recording_id}", status_code=204, tags=["recordings"])
def delete_recording(recording_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = db.query(Recording).filter(Recording.id == recording_id, Recording.host_id == current_user.id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recording not found")
    db.delete(rec)
    db.commit()


# ── Routes: Channels & Chat ───────────────────────────────────────
@app.get("/api/channels", response_model=List[ChannelOut], tags=["chat"])
def list_channels(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Channel).all()


@app.post("/api/channels", response_model=ChannelOut, status_code=201, tags=["chat"])
def create_channel(body: ChannelCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ch = Channel(**body.model_dump(), created_by=current_user.id)
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return ch


@app.get("/api/channels/{channel_id}/messages", response_model=List[MessageOut], tags=["chat"])
def get_messages(channel_id: int, limit: int = 50, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(ChatMessage).filter(ChatMessage.channel_id == channel_id).order_by(ChatMessage.created_at).limit(limit).all()


@app.post("/api/channels/{channel_id}/messages", response_model=MessageOut, status_code=201, tags=["chat"])
def send_message(channel_id: int, body: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    msg = ChatMessage(channel_id=channel_id, sender_id=current_user.id, **body.model_dump(exclude={"channel_id", "recipient_id"}))
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


# ── Routes: Contacts ──────────────────────────────────────────────
@app.get("/api/contacts", response_model=List[ContactOut], tags=["contacts"])
def list_contacts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Contact).filter(Contact.user_id == current_user.id).all()


@app.post("/api/contacts", response_model=ContactOut, status_code=201, tags=["contacts"])
def add_contact(body: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contact = Contact(**body.model_dump(), user_id=current_user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@app.delete("/api/contacts/{contact_id}", status_code=204, tags=["contacts"])
def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == current_user.id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()


# ── Routes: Webinars ──────────────────────────────────────────────
@app.get("/api/webinars", response_model=List[WebinarOut], tags=["webinars"])
def list_webinars(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Webinar).filter(Webinar.host_id == current_user.id).all()


@app.post("/api/webinars", response_model=WebinarOut, status_code=201, tags=["webinars"])
def create_webinar(body: WebinarCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    webinar = Webinar(
        **body.model_dump(),
        webinar_id=generate_meeting_id(),
        host_id=current_user.id,
    )
    db.add(webinar)
    db.commit()
    db.refresh(webinar)
    return webinar


# ── WebSocket: Real-time Signaling ────────────────────────────────
@app.websocket("/ws/meeting/{meeting_id}")
async def meeting_ws(meeting_id: str, ws: WebSocket):
    """
    WebSocket for real-time meeting signaling (WebRTC offer/answer/ICE).
    Clients send JSON: { "type": "offer"|"answer"|"ice", "data": {...}, "target": "peer_id" }
    """
    await manager.connect(f"meeting:{meeting_id}", ws)
    try:
        while True:
            data = await ws.receive_json()
            await manager.broadcast(f"meeting:{meeting_id}", data)
    except WebSocketDisconnect:
        manager.disconnect(f"meeting:{meeting_id}", ws)


@app.websocket("/ws/chat/{channel_id}")
async def chat_ws(channel_id: int, ws: WebSocket):
    """
    WebSocket for real-time team chat messages.
    Clients send: { "sender": "Alex", "content": "Hello!", "type": "text" }
    """
    room = f"chat:{channel_id}"
    await manager.connect(room, ws)
    try:
        while True:
            data = await ws.receive_json()
            data["timestamp"] = datetime.utcnow().isoformat()
            await manager.broadcast(room, data)
    except WebSocketDisconnect:
        manager.disconnect(room, ws)


# ── Routes: Dashboard stats ───────────────────────────────────────
@app.get("/api/dashboard", tags=["dashboard"])
def dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    now = datetime.utcnow()
    upcoming = db.query(Meeting).filter(
        Meeting.owner_id == current_user.id,
        Meeting.start_time >= now,
    ).order_by(Meeting.start_time).limit(5).all()

    recent = db.query(Meeting).filter(
        Meeting.owner_id == current_user.id,
        Meeting.start_time < now,
    ).order_by(Meeting.start_time.desc()).limit(5).all()

    return {
        "user": {
            "display_name": current_user.display_name,
            "personal_meeting_id": current_user.personal_meeting_id,
        },
        "upcoming_meetings": [
            {
                "id": m.id,
                "topic": m.topic,
                "meeting_id": m.meeting_id,
                "start_time": m.start_time.isoformat(),
                "duration_minutes": m.duration_minutes,
                "status": m.status,
            }
            for m in upcoming
        ],
        "recent_meetings": [
            {
                "id": m.id,
                "topic": m.topic,
                "start_time": m.start_time.isoformat(),
                "status": m.status,
            }
            for m in recent
        ],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
