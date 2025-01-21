from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import CategoryType
from schemas.schemas import UserCreate, ShowUser, UserUpdate
from repository.dals import UserDAL, CategoryDAL
from uuid import UUID
from fastapi import HTTPException
from repository.hashing import Hasher


async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db.begin():
        user_dal = UserDAL(db)
        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password)
        )
        default_categories = [
            {"name_cat": "Транспорт", "type": CategoryType.expense},
            {"name_cat": "Еда", "type": CategoryType.expense},
            {"name_cat": "Развлечения", "type": CategoryType.expense},
            {"name_cat": "Образовательные услуги", "type": CategoryType.expense},
            {"name_cat": "ЖКХ", "type": CategoryType.expense},
            {"name_cat": "Одежда", "type": CategoryType.expense},
            {"name_cat": "Здоровье", "type": CategoryType.expense},
            {"name_cat": "Зарплата", "type": CategoryType.income},
        ]

        category_dal = CategoryDAL(db)
        for category in default_categories:
            await category_dal.create_default_categories(
                user_id=user.id,
                name_cat=category["name_cat"],
                category_type=category["type"],
            )
        return ShowUser(
            user_id=user.id,
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
                user_id=user.id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )
