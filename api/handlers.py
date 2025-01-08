from typing import Union
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import UserCreate, ShowUser, UserUpdate, DeleteUserResponse
from repository.dals import UserDAL
from db.session import get_db
from uuid import UUID
from fastapi import HTTPException
from repository.hashing import Hasher

auth_router = APIRouter()
new_router = APIRouter()


async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db.begin():
        user_dal = UserDAL(db)
        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password)
        )
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )


async def _update_active_user(user_id: UUID, body: UserUpdate, db: AsyncSession) -> ShowUser:
    async with db.begin():
        user_dal = UserDAL(db)
        updated_user = await user_dal.update_user(
            user_id=user_id,
            name=body.name,
            surname=body.surname,
            email=body.email,
        )
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")

        return ShowUser(
            user_id=updated_user.user_id,
            name=updated_user.name,
            surname=updated_user.surname,
            email=updated_user.email,
            is_active=updated_user.is_active,
        )


async def _delete_user(user_id, db) -> Union[UUID, None]:
    async with db.begin():
        user_dal = UserDAL(db)
        deleted_user_id = await user_dal.delete_user(
            user_id=user_id,
        )
        return deleted_user_id


async def _get_user_by_id(user_id, db) -> Union[ShowUser, None]:
    async with db.begin():
        user_dal = UserDAL(db)
        user = await user_dal.get_user_by_id(
            user_id=user_id,
        )
        if user is not None:
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )


@auth_router.post("/", response_model=ShowUser)
async def create_user(
        body: UserCreate,
        db: AsyncSession = Depends(get_db)):
    return await _create_new_user(body, db)


@auth_router.patch("/{user_id}", response_model=ShowUser)
async def update_user(
        user_id: UUID,
        body: UserUpdate,
        db: AsyncSession = Depends(get_db)):
    return await _update_active_user(user_id, body, db)


@auth_router.delete("/{user_id}", response_model=DeleteUserResponse)
async def delete_user(
        user_id: UUID,
        db: AsyncSession = Depends(get_db)):
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@auth_router.get("/{user_id}", response_model=ShowUser)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return user
