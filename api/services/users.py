import jwt
from fastapi import HTTPException, status
from fastapi.params import Depends
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from api.core.config import ALGORITHM, SECRET_KEY
from api.models.users import Users
from api.schemas.users import AccessTokenDataSchema, UserLoginSchema
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def verify_password(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)

def get_hashed_password(password):
    return pwd_context.hash(password)

async def authenticate_user(db: AsyncSession, user: UserLoginSchema):
    try:
        result = await db.execute(select(Users).where(Users.email == user.email))
        db_user = result.scalar_one_or_none()
    
        if not user:
            return False
        
        if not verify_password(user.password, db_user.password):
            return False
    
        return db_user
    except Exception as e:
        return False

async def authenticate_user_by_oath2(db: AsyncSession, email: str, password: str):
    return await authenticate_user(db, UserLoginSchema(email=email, password=password))

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')
        
        if email is None:
            raise credentials_exception
        return AccessTokenDataSchema(email=email)
    except InvalidTokenError:
        raise credentials_exception
    
