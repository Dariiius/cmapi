from datetime import timedelta
from fastapi import APIRouter, Form
from fastapi.params import Depends
from api.core.config import ACCESS_TOKEN_EXPIRE
from api.core.db import get_db
from api.schemas.users import AccessTokenSchema, UserLoginSchema
from fastapi import HTTPException, status
from api.services.users import authenticate_user, create_access_token
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/auth',  tags=['Users'])


@router.post('/login', response_model=AccessTokenSchema)
async def login_for_access_token(
    username: str = Form(..., description='Email address is used as username'),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, UserLoginSchema(email=username, password=password))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Incorrect username or password.', 
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE))
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )
    return AccessTokenSchema(access_token=access_token, token_type='bearer')
