from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.core.config import settings
from app.core.rate_limit import limiter
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db_session
from app.models import User
from app.schemas import LoginRequest, UserCreate, UserRead
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
async def register_user(
    request: Request, payload: UserCreate, session: AsyncSession = Depends(get_db_session)
) -> UserRead:
    exists_query = select(User).where(
        or_(User.email == payload.email, User.username == payload.username)
    )
    result = await session.execute(exists_query)
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        is_subscribed=payload.is_subscribed,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return UserRead(
        id=str(user.id),
        username=user.username,
        email=user.email,
        is_subscribed=user.is_subscribed,
    )


@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
async def login_user(
    request: Request,
    payload: LoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    if payload.username_or_email == settings.admin_username:
        if payload.password != settings.admin_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        
        admin_query = select(User).where(User.username == settings.admin_username)
        admin_result = await session.execute(admin_query)
        user = admin_result.scalar_one_or_none()
        
        if not user:
            user = User(
                username=settings.admin_username,
                email=f"{settings.admin_username}@admin.local",
                hashed_password=hash_password(settings.admin_password),
                is_admin=True,
                is_subscribed=False,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        else:
            user.is_admin = True
            user.hashed_password = hash_password(settings.admin_password)
            session.add(user)
            await session.commit()
            
    else:
        query = select(User).where(
            or_(User.username == payload.username_or_email, User.email == payload.username_or_email)
        )
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token(subject=str(user.id))
    
    response.set_cookie(
        key=settings.cookie_name,
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.jwt_access_token_exp_minutes * 60,
        path="/",
    )

    if user.is_admin:
        message = "Logged in as admin"
    else:
        message = "Logged in"

    return {"message": message}


@router.post("/logout", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
async def logout_user(request: Request, response: Response) -> dict:
    response.delete_cookie(key=settings.cookie_name, path="/")
    return {"message": "Logged out"}
