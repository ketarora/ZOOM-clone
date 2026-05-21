"""
app/routers/recordings.py — Cloud & Local recording management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Literal

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.recording import Recording
from app.schemas.recording import RecordingOut

router = APIRouter(prefix="/recordings", tags=["recordings"])


@router.get(
    "",
    response_model=list[RecordingOut],
    summary="List recordings (cloud | local | all)",
)
def list_recordings(
    storage: Literal["cloud", "local", "all"] = Query("all"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Recording]:
    q = db.query(Recording).filter(Recording.host_id == current_user.id)
    if storage != "all":
        q = q.filter(Recording.storage_type == storage)
    return q.order_by(Recording.recorded_at.desc()).all()


@router.get("/{recording_id}", response_model=RecordingOut, summary="Get a single recording")
def get_recording(
    recording_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Recording:
    rec = db.query(Recording).filter(Recording.id == recording_id, Recording.host_id == current_user.id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recording not found")
    return rec


@router.delete("/{recording_id}", status_code=204, summary="Delete a recording")
def delete_recording(
    recording_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    rec = db.query(Recording).filter(Recording.id == recording_id, Recording.host_id == current_user.id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recording not found")
    db.delete(rec)
    db.commit()
