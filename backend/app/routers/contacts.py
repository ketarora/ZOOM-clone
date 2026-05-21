"""
app/routers/contacts.py — Contact directory management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactOut

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("", response_model=list[ContactOut], summary="List contacts (optionally filter by group)")
def list_contacts(
    group: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Contact]:
    q = db.query(Contact).filter(Contact.user_id == current_user.id)
    if group:
        q = q.filter(Contact.group_name.ilike(f"%{group}%"))
    return q.order_by(Contact.contact_name).all()


@router.post("", response_model=ContactOut, status_code=201, summary="Add a contact")
def add_contact(
    body: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Contact:
    contact = Contact(**body.model_dump(), user_id=current_user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.delete("/{contact_id}", status_code=204, summary="Remove a contact")
def remove_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    contact = db.query(Contact).filter(
        Contact.id == contact_id, Contact.user_id == current_user.id
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
