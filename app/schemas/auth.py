from pydantic import BaseModel


class LoginRequest(BaseModel):
    username_or_email: str
    password: str
