import uuid
from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(UserBaseSchema):
    id: uuid.UUID

    class Config:
        from_attributes = True


class UserLoginSchema(UserBaseSchema):
    pass


class AccessTokenSchema(BaseModel):
    access_token: str
    token_type: str


class AccessTokenDataSchema(BaseModel):
    email: str | None = None