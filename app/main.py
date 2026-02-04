from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.routers import auth, newsletter, users
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.rate_limit import limiter

configure_logging()

app = FastAPI(title=settings.app_name)
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Too many requests."},
    )


app.add_middleware(SlowAPIMiddleware)

app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(users.router, prefix=settings.api_v1_prefix)
app.include_router(newsletter.router, prefix=settings.api_v1_prefix)
