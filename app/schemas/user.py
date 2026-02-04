from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    is_subscribed: bool = False


class UserRead(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_subscribed: bool


class PasswordChangeRequest(BaseModel):
    old_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class UsernameChangeRequest(BaseModel):
    new_username: str = Field(min_length=3, max_length=50)


class SubscriptionUpdateRequest(BaseModel):
    is_subscribed: bool


class AccountDeleteRequest(BaseModel):
    password: str = Field(min_length=8, max_length=128)
