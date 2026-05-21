"""
ZoomConnect Backend — FastAPI
Database models using SQLAlchemy
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./zoomconnect.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    job_title = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    personal_meeting_id = Column(String(20), unique=True, nullable=True)
    avatar_url = Column(String(300), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    meetings = relationship("Meeting", back_populates="owner", foreign_keys="Meeting.owner_id")
    contacts = relationship("Contact", back_populates="user", foreign_keys="Contact.user_id")
    messages = relationship("ChatMessage", back_populates="sender")


class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    meeting_id = Column(String(20), unique=True, index=True)
    passcode = Column(String(20), nullable=True)
    start_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    timezone = Column(String(50), default="UTC")
    waiting_room = Column(Boolean, default=True)
    use_passcode = Column(Boolean, default=True)
    is_recurring = Column(Boolean, default=False)
    status = Column(String(20), default="scheduled")  # scheduled, started, ended
    recording_url = Column(String(300), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="meetings", foreign_keys=[owner_id])
    participants = relationship("MeetingParticipant", back_populates="meeting")


class MeetingParticipant(Base):
    __tablename__ = "meeting_participants"
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    guest_name = Column(String(100), nullable=True)
    joined_at = Column(DateTime, nullable=True)
    left_at = Column(DateTime, nullable=True)

    meeting = relationship("Meeting", back_populates="participants")


class Recording(Base):
    __tablename__ = "recordings"
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    title = Column(String(200), nullable=False)
    file_url = Column(String(300), nullable=True)
    thumbnail_url = Column(String(300), nullable=True)
    duration_seconds = Column(Integer, default=0)
    file_size_mb = Column(Integer, default=0)
    status = Column(String(20), default="processing")  # processing, ready
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)


class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300), nullable=True)
    is_private = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("ChatMessage", back_populates="channel")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # for DMs
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")  # text, file, code
    file_url = Column(String(300), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    edited_at = Column(DateTime, nullable=True)

    sender = relationship("User", back_populates="messages", foreign_keys=[sender_id])
    channel = relationship("Channel", back_populates="messages")


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    contact_name = Column(String(100), nullable=True)
    contact_email = Column(String(150), nullable=True)
    phone = Column(String(30), nullable=True)
    group_name = Column(String(50), nullable=True)
    is_online = Column(Boolean, default=False)
    added_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="contacts", foreign_keys=[user_id])


class Webinar(Base):
    __tablename__ = "webinars"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    webinar_id = Column(String(20), unique=True, index=True)
    start_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    registrant_count = Column(Integer, default=0)
    status = Column(String(20), default="scheduled")
    created_at = Column(DateTime, default=datetime.utcnow)
