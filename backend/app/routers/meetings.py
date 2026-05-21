"""
app/routers/meetings.py — Full Meeting CRUD + join/start flow
"""
from datetime import datetime, timezone
from typing import Literal, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.meeting import Meeting
from app.schemas.meeting import MeetingCreate, MeetingUpdate, MeetingOut, JoinMeetingRequest

router = APIRouter(prefix="/meetings", tags=["meetings"])


def _get_owned_meeting(meeting_id: int, db: Session, user: User) -> Meeting:
    """Shared helper — 404 if not found, 403 if not owner."""
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    if meeting.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You don't own this meeting")
    return meeting


@router.get("", response_model=list[MeetingOut], summary="List meetings (upcoming | previous | all)")
def list_meetings(
    filter: Literal["upcoming", "previous", "all"] = Query("upcoming"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Meeting]:
    q = db.query(Meeting).filter(Meeting.owner_id == current_user.id)
    now = datetime.now(timezone.utc)
    if filter == "upcoming":
        q = q.filter(Meeting.start_time >= now)
    elif filter == "previous":
        q = q.filter(Meeting.start_time < now)
    return q.order_by(Meeting.start_time).all()


@router.post(
    "",
    response_model=MeetingOut,
    status_code=status.HTTP_201_CREATED,
    summary="Schedule a new meeting",
)
def create_meeting(
    body: MeetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Meeting:
    meeting = Meeting(**body.model_dump(), owner_id=current_user.id)
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting


@router.get("/{meeting_id}", response_model=MeetingOut, summary="Get a single meeting")
def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Meeting:
    return _get_owned_meeting(meeting_id, db, current_user)


@router.patch("/{meeting_id}", response_model=MeetingOut, summary="Update meeting details")
def update_meeting(
    meeting_id: int,
    body: MeetingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Meeting:
    meeting = _get_owned_meeting(meeting_id, db, current_user)
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(meeting, field, value)
    db.commit()
    db.refresh(meeting)
    return meeting


@router.delete(
    "/{meeting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a meeting",
)
def delete_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    meeting = _get_owned_meeting(meeting_id, db, current_user)
    db.delete(meeting)
    db.commit()


@router.post("/{meeting_id}/start", summary="Mark meeting as started")
def start_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    meeting = _get_owned_meeting(meeting_id, db, current_user)
    if meeting.status == "ended":
        raise HTTPException(status_code=400, detail="Meeting has already ended")
    meeting.status = "started"
    db.commit()
    return {
        "status": "started",
        "meeting_id": meeting.meeting_id,
        "topic": meeting.topic,
        "redirect_url": f"/room?id={meeting.meeting_id}",
    }


@router.post("/{meeting_id}/end", summary="Mark meeting as ended")
def end_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    meeting = _get_owned_meeting(meeting_id, db, current_user)
    meeting.status = "ended"
    db.commit()
    return {"status": "ended"}


@router.post("/join", summary="Join a meeting by meeting ID (public endpoint)")
def join_meeting(body: JoinMeetingRequest, db: Session = Depends(get_db)) -> dict:
    # Normalise meeting_id — strip spaces for lookup
    meeting_id_clean = body.meeting_id.strip()
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id_clean).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found. Check the ID and try again.")
    if meeting.status == "ended":
        raise HTTPException(status_code=410, detail="This meeting has already ended.")
    if meeting.use_passcode and body.passcode and meeting.passcode != body.passcode:
        raise HTTPException(status_code=403, detail="Incorrect passcode.")
    return {
        "status": "admitted" if not meeting.waiting_room else "waiting_room",
        "topic": meeting.topic,
        "meeting_id": meeting.meeting_id,
        "waiting_room": meeting.waiting_room,
        "redirect_url": f"/room?id={meeting.meeting_id}&name={body.name}",
    }
