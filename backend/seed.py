"""
seed.py — Demo data seeder
Run: python seed.py (from the backend/ directory)
Creates a ready-to-demo dataset.
"""
import sys
import os
import random
from datetime import datetime, timezone, timedelta

# Allow running from backend/ directory
sys.path.insert(0, os.path.dirname(__file__))

from app.core.config import get_settings
from app.core.database import engine, SessionLocal
from app.core.security import hash_password
from app.core.database import Base

# Register all models
import app.models  # noqa: F401

Base.metadata.create_all(bind=engine)

from app.models.user import User
from app.models.meeting import Meeting
from app.models.recording import Recording
from app.models.chat import Channel, ChatMessage
from app.models.contact import Contact, Webinar

db = SessionLocal()
now = datetime.now(timezone.utc)

print("🌱  Seeding ZoomConnect demo data...")


# ── Users ────────────────────────────────────────────────────────
USERS = [
    dict(display_name="Alex Thompson",    email="alex@zoomconnect.demo",  job_title="Senior Product Designer",  department="User Experience"),
    dict(display_name="Sarah Jenkins",    email="sarah@zoomconnect.demo", job_title="Engineering Lead",         department="Engineering"),
    dict(display_name="David Chen",       email="david@zoomconnect.demo", job_title="Backend Engineer",         department="Engineering"),
    dict(display_name="Elena Rodriguez", email="elena@zoomconnect.demo", job_title="Product Manager",          department="Product"),
    dict(display_name="James Kwon",       email="james@zoomconnect.demo", job_title="Sales Director",           department="Sales"),
]

created_users: list[User] = []
for u in USERS:
    existing = db.query(User).filter(User.email == u["email"]).first()
    if not existing:
        user = User(**u, hashed_password=hash_password("demo1234"))
        db.add(user)
        db.flush()
        created_users.append(user)
    else:
        created_users.append(existing)
db.commit()

alex  = created_users[0]
sarah = created_users[1]
david = created_users[2]
elena = created_users[3]

print(f"  ✔ {len(created_users)} users ready")


# ── Meetings ─────────────────────────────────────────────────────
MEETINGS = [
    dict(topic="Product Sync: Q4 Roadmap",        meeting_id="812 3456 7890", start_time=now + timedelta(hours=1),    duration_minutes=60,  status="scheduled"),
    dict(topic="Design Review: System Tokens",     meeting_id="901 2345 6781", start_time=now + timedelta(hours=3),    duration_minutes=30,  status="scheduled"),
    dict(topic="Weekly Engineering Standup",        meeting_id="776 5432 1098", start_time=now + timedelta(days=1),     duration_minutes=15,  status="scheduled"),
    dict(topic="Q4 Planning Session",               meeting_id="847 291 3022",  start_time=now - timedelta(days=7),     duration_minutes=90,  status="ended"),
    dict(topic="Weekly Team Catch-up",              meeting_id="932 110 5490",  start_time=now + timedelta(hours=5),    duration_minutes=60,  status="scheduled"),
    dict(topic="Investor Demo Prep",                meeting_id="501 887 6633",  start_time=now + timedelta(days=2, hours=14), duration_minutes=45, status="scheduled"),
]

created_meetings: list[Meeting] = []
for m in MEETINGS:
    existing = db.query(Meeting).filter(Meeting.meeting_id == m["meeting_id"]).first()
    if not existing:
        meeting = Meeting(
            **m,
            passcode=str(random.randint(100000, 999999)),
            waiting_room=True,
            use_passcode=True,
            owner_id=alex.id,
            timezone="America/New_York",
        )
        db.add(meeting)
        db.flush()
        created_meetings.append(meeting)
    else:
        created_meetings.append(existing)
db.commit()

print(f"  ✔ {len(created_meetings)} meetings ready")


# ── Recordings ───────────────────────────────────────────────────
if db.query(Recording).count() == 0:
    meeting_ref = created_meetings[0]
    recs = [
        Recording(meeting_id=meeting_ref.id, host_id=alex.id,  title="Q4 Planning Session",    file_size_mb=245, duration_seconds=2720, status="ready",      storage_type="cloud",  recorded_at=now - timedelta(days=7)),
        Recording(meeting_id=meeting_ref.id, host_id=alex.id,  title="Weekly Product Sync",     file_size_mb=128, duration_seconds=1335, status="ready",      storage_type="cloud",  recorded_at=now - timedelta(days=14)),
        Recording(meeting_id=meeting_ref.id, host_id=sarah.id, title="Client Onboarding Call",  file_size_mb=0,   duration_seconds=0,    status="processing", storage_type="cloud",  recorded_at=now - timedelta(hours=2)),
        Recording(meeting_id=meeting_ref.id, host_id=alex.id,  title="Design Sprint Review",    file_size_mb=310, duration_seconds=3600, status="ready",      storage_type="local",  recorded_at=now - timedelta(days=3)),
    ]
    db.add_all(recs)
    db.commit()
print(f"  ✔ {db.query(Recording).count()} recordings ready")


# ── Channels + Messages ──────────────────────────────────────────
CHANNELS = [
    dict(name="product-design",    description="UI/UX and Product Team Sync",     is_private=False),
    dict(name="engineering-updates",description="Dev team announcements",          is_private=False),
    dict(name="general",           description="Company-wide announcements",       is_private=False),
    dict(name="sales-team",        description="Sales pipeline & leads",           is_private=True),
]

created_channels: list[Channel] = []
for c in CHANNELS:
    existing = db.query(Channel).filter(Channel.name == c["name"]).first()
    if not existing:
        ch = Channel(**c, created_by=alex.id)
        db.add(ch)
        db.flush()
        created_channels.append(ch)
    else:
        created_channels.append(existing)
db.commit()

if db.query(ChatMessage).count() == 0:
    prod_channel = created_channels[0]
    msgs = [
        ChatMessage(channel_id=prod_channel.id, sender_id=alex.id,  content="Morning team! Starting the design review at 11 AM today 🎨", message_type="text"),
        ChatMessage(channel_id=prod_channel.id, sender_id=sarah.id, content="Great! I'll have the component specs ready.", message_type="text"),
        ChatMessage(channel_id=prod_channel.id, sender_id=david.id, content="Can we align on the API schema first? I've got the endpoint draft ready.", message_type="text"),
        ChatMessage(channel_id=prod_channel.id, sender_id=elena.id, content="Sharing the PRD link → https://docs.internal/prd-q4", message_type="text"),
        ChatMessage(channel_id=prod_channel.id, sender_id=alex.id,  content="Perfect, see everyone in the meeting room!", message_type="text"),
    ]
    db.add_all(msgs)
    db.commit()

print(f"  ✔ {len(created_channels)} channels + messages ready")


# ── Contacts ─────────────────────────────────────────────────────
if db.query(Contact).filter(Contact.user_id == alex.id).count() == 0:
    for other in [sarah, david, elena] + [u for u in created_users if u.id not in [alex.id, sarah.id, david.id, elena.id]]:
        c = Contact(
            user_id=alex.id,
            contact_user_id=other.id,
            contact_name=other.display_name,
            contact_email=other.email,
            group_name=other.department,
            is_online=random.choice([True, False]),
        )
        db.add(c)
    db.commit()
print(f"  ✔ {db.query(Contact).filter(Contact.user_id == alex.id).count()} contacts ready")


# ── Webinar ──────────────────────────────────────────────────────
if db.query(Webinar).count() == 0:
    wb = Webinar(
        title="Q4 Global All Hands — Company Update",
        description="Quarterly company-wide all-hands. Q4 results, 2025 roadmap preview, and live Q&A.",
        webinar_id="842 911 304",
        start_time=now + timedelta(days=3, hours=10),
        duration_minutes=90,
        host_id=alex.id,
        registrant_count=1245,
        status="scheduled",
    )
    db.add(wb)
    db.commit()
print(f"  ✔ {db.query(Webinar).count()} webinars ready")

db.close()

print("\n✅  Seed complete!")
print("   Login: alex@zoomconnect.demo / demo1234")
print("   API:   http://localhost:8000/api/docs")
