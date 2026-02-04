from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.rate_limit import limiter
from app.core.security import hash_password, verify_password
from app.db.session import get_db_session
from app.models import User
from app.schemas import (
    AccountDeleteRequest,
    PasswordChangeRequest,
    SubscriptionUpdateRequest,
    UsernameChangeRequest,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/me/password", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def change_password(
    request: Request,
    payload: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    if current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin credentials can only be changed in .env file",
        )
    
    if not verify_password(payload.old_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")

    current_user.hashed_password = hash_password(payload.new_password)
    session.add(current_user)
    await session.commit()
    return {"message": "Password updated"}


@router.patch("/me/username", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def change_username(
    request: Request,
    payload: UsernameChangeRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    if current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin credentials can only be changed in .env file",
        )
    
    if payload.new_username == current_user.username:
        return {"message": "Username updated"}

    exists_query = select(User).where(User.username == payload.new_username)
    result = await session.execute(exists_query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already taken"
        )

    current_user.username = payload.new_username
    session.add(current_user)
    await session.commit()
    return {"message": "Username updated"}


@router.patch("/me/subscription", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def update_subscription(
    request: Request,
    payload: SubscriptionUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    current_user.is_subscribed = payload.is_subscribed
    session.add(current_user)
    await session.commit()
    status_text = "subscribed to" if payload.is_subscribed else "unsubscribed from"
    return {
        "message": f"Successfully {status_text} newsletter",
        "is_subscribed": payload.is_subscribed,
    }


@router.delete("/me", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def delete_account(
    request: Request,
    payload: AccountDeleteRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    if current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account cannot be deleted via API",
        )
    
    if not verify_password(payload.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password",
        )
    
    await session.delete(current_user)
    await session.commit()
    return {"message": "Account deleted successfully"}
