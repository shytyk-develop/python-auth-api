from pydantic import BaseModel, Field


class NewsletterSendRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)
