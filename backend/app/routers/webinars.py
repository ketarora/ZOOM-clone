"""
app/routers/webinars.py — Webinar scheduling
"""
import random
import string
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.contact import Webinar
from app.schemas.webinar import WebinarCreate, WebinarOut

router = APIRouter(prefix="/webinars", tags=["webinars"])


def _gen_webinar_id() -> str:
    d = "".join(random.choices(string.digits, k=9))
    return f"{d[:3]} {d[3:6]} {d[6:]}"


@router.get("", response_model=list[WebinarOut], summary="List your webinars")
def list_webinars(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Webinar]:
    return db.query(Webinar).filter(Webinar.host_id == current_user.id).order_by(Webinar.start_time).all()


@router.post("", response_model=WebinarOut, status_code=201, summary="Schedule a webinar")
def create_webinar(
    body: WebinarCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Webinar:
    webinar = Webinar(**body.model_dump(), webinar_id=_gen_webinar_id(), host_id=current_user.id)
    db.add(webinar)
    db.commit()
    db.refresh(webinar)
    return webinar


@router.delete("/{webinar_id}", status_code=204, summary="Cancel a webinar")
def delete_webinar(
    webinar_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    wb = db.query(Webinar).filter(Webinar.id == webinar_id, Webinar.host_id == current_user.id).first()
    if not wb:
        raise HTTPException(status_code=404, detail="Webinar not found")
    db.delete(wb)
    db.commit()
