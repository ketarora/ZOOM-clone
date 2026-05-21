"""
app/routers/auth.py — Register + Login endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new account",
)
def register(body: UserRegister, db: Session = Depends(get_db)) -> Token:
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )
    user = User(
        display_name=body.display_name,
        email=body.email,
        hashed_password=hash_password(body.password),
        job_title=body.job_title,
        department=body.department,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return Token(access_token=create_access_token(user.id))


@router.post(
    "/login",
    response_model=Token,
    summary="Login and get a JWT access token",
)
def login(body: UserLogin, db: Session = Depends(get_db)) -> Token:
    user = db.query(User).filter(User.email == body.email, User.is_active == True).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return Token(access_token=create_access_token(user.id))
