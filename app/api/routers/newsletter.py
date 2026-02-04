import logging

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_admin_user
from app.core.email import send_email
from app.core.rate_limit import limiter
from app.db.session import get_db_session
from app.models import User
from app.schemas import NewsletterSendRequest

router = APIRouter(prefix="/newsletter", tags=["newsletter"])

logger = logging.getLogger(__name__)


@router.post("/send", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def send_newsletter(
    request: Request,
    payload: NewsletterSendRequest,
    _: User = Depends(get_admin_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    result = await session.execute(select(User).where(User.is_subscribed.is_(True)))
    subscribers = result.scalars().all()

    sent_count = 0
    failed_count = 0
    
    for user in subscribers:
        success = await send_email(
            to_email=user.email,
            subject="Newsletter Update",
            body=payload.message,
            body_html=f"<html><body><p>{payload.message}</p></body></html>",
        )
        if success:
            sent_count += 1
        else:
            failed_count += 1

    return {
        "sent": sent_count,
        "failed": failed_count,
        "total_subscribers": len(subscribers),
    }
