from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
import config
from api.auth import authenticate_user, get_current_user_from_token
from db.models import User
from db.session import get_db
from schemas.schemas import Token
from sqlalchemy.ext.asyncio import AsyncSession
from security import create_access_token

login_router = APIRouter()


@login_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "other_custom_data": ['data']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@login_router.get("/auth_endpoint")
async def sample_endpoint_under_jwt(current_user: User = Depends(get_current_user_from_token), ):
    current_user = current_user.__dict__.copy()
    current_user.pop('_sa_instance_state', None)
    current_user.pop('hashed_password', None)
    return {"Success": True, "current_user": current_user}
