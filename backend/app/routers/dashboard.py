"""
app/routers/dashboard.py — Aggregated home page stats
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.meeting import Meeting
from app.models.recording import Recording
from app.models.contact import Contact

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", summary="Aggregated stats for the home dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    now = datetime.now(timezone.utc)

    upcoming = (
        db.query(Meeting)
        .filter(Meeting.owner_id == current_user.id, Meeting.start_time >= now)
        .order_by(Meeting.start_time)
        .limit(5)
        .all()
    )

    recent = (
        db.query(Meeting)
        .filter(Meeting.owner_id == current_user.id, Meeting.start_time < now)
        .order_by(Meeting.start_time.desc())
        .limit(3)
        .all()
    )

    total_meetings  = db.query(Meeting).filter(Meeting.owner_id == current_user.id).count()
    total_recordings = db.query(Recording).filter(Recording.host_id == current_user.id).count()
    total_contacts   = db.query(Contact).filter(Contact.user_id == current_user.id).count()

    def _meeting_dict(m: Meeting) -> dict:
        return {
            "id": m.id,
            "topic": m.topic,
            "meeting_id": m.meeting_id,
            "start_time": m.start_time.isoformat(),
            "duration_minutes": m.duration_minutes,
            "status": m.status,
        }

    return {
        "user": {
            "id": current_user.id,
            "display_name": current_user.display_name,
            "job_title": current_user.job_title,
            "personal_meeting_id": current_user.personal_meeting_id,
            "avatar_url": current_user.avatar_url,
        },
        "stats": {
            "total_meetings": total_meetings,
            "total_recordings": total_recordings,
            "total_contacts": total_contacts,
        },
        "upcoming_meetings": [_meeting_dict(m) for m in upcoming],
        "recent_meetings": [_meeting_dict(m) for m in recent],
    }
