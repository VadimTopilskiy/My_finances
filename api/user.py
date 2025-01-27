from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from service.auth import get_current_user_from_token
from service.user import _create_new_user, _update_active_user, _delete_user
from db.models import User
from schemas.schemas import UserCreate, ShowUser, UserUpdate, DeleteUserResponse
from db.session import get_db
from uuid import UUID
from fastapi import HTTPException

auth_router = APIRouter()


@auth_router.post("/", response_model=ShowUser)
async def create_user(
        body: UserCreate,
        db: AsyncSession = Depends(get_db)):
    return await _create_new_user(body, db)


@auth_router.patch("/{user_id}", response_model=ShowUser)
async def update_user(
        user_id: UUID,
        body: UserUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)):
    return await _update_active_user(user_id, body, db)


@auth_router.delete("/{user_id}", response_model=DeleteUserResponse)
async def delete_user(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)):
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@auth_router.get("/", response_model=ShowUser)
async def get_user_by_id(
        # user_id: UUID, db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)):
    # user = await _get_user_by_id(user_id, db)
    # if user is None:
    #     raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return current_user
