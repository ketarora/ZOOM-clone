"""
app/routers/chat.py — Channels + Messages REST endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.chat import Channel, ChatMessage
from app.schemas.chat import ChannelCreate, ChannelOut, MessageCreate, MessageOut

router = APIRouter(tags=["chat"])


# ── Channels ──────────────────────────────────────────────────────
@router.get("/channels", response_model=list[ChannelOut], summary="List all visible channels")
def list_channels(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Channel]:
    return db.query(Channel).filter(
        (Channel.is_private == False) | (Channel.created_by == current_user.id)
    ).all()


@router.post(
    "/channels",
    response_model=ChannelOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new channel",
)
def create_channel(
    body: ChannelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Channel:
    if db.query(Channel).filter(Channel.name == body.name).first():
        raise HTTPException(status_code=409, detail=f"Channel #{body.name} already exists")
    ch = Channel(**body.model_dump(), created_by=current_user.id)
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return ch


# ── Messages ──────────────────────────────────────────────────────
@router.get(
    "/channels/{channel_id}/messages",
    response_model=list[MessageOut],
    summary="Get channel message history",
)
def get_messages(
    channel_id: int,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ChatMessage]:
    ch = db.query(Channel).filter(Channel.id == channel_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Channel not found")
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.channel_id == channel_id)
        .order_by(ChatMessage.created_at)
        .limit(limit)
        .all()
    )


@router.post(
    "/channels/{channel_id}/messages",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
    summary="Post a message to a channel",
)
def send_message(
    channel_id: int,
    body: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatMessage:
    ch = db.query(Channel).filter(Channel.id == channel_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Channel not found")
    msg = ChatMessage(
        channel_id=channel_id,
        sender_id=current_user.id,
        content=body.content,
        message_type=body.message_type,
        file_url=body.file_url,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@router.delete(
    "/channels/{channel_id}/messages/{message_id}",
    status_code=204,
    summary="Delete a message (sender only)",
)
def delete_message(
    channel_id: int,
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    msg = db.query(ChatMessage).filter(
        ChatMessage.id == message_id,
        ChatMessage.channel_id == channel_id,
        ChatMessage.sender_id == current_user.id,
    ).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found or not yours")
    db.delete(msg)
    db.commit()
