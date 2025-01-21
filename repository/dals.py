from typing import Union
from sqlalchemy import select, update, and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User, CategoryType, Categories
from uuid import UUID

from schemas.schemas import CategoryShow


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, name: str, surname: str, email: str, hashed_password: str) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_password
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def update_user(self, user_id: UUID, **kwargs):
        query = select(User).where(User.user_id == user_id)
        result = await self.db_session.execute(query)
        try:
            user = result.scalar_one()
        except NoResultFound:
            return None

        for key, value in kwargs.items():
            if value is not None:
                setattr(user, key, value)

        await self.db_session.commit()
        return user

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = update(User).where(and_(User.user_id == user_id, User.is_active == True)).values(
            is_active=False).returning(User.user_id)
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]


class CategoryDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_default_categories(self, user_id: UUID, name_cat: str, category_type: CategoryType):
        default_category = Categories(user_id=user_id, name_cat=name_cat, type=category_type)
        self.db_session.add(default_category)
        await self.db_session.flush()
        return default_category

    async def create_new_category(self, user_id: UUID, name_cat: str, category_type: CategoryType):
        new_category = Categories(name_cat=name_cat, type=category_type, user_id=user_id)
        self.db_session.add(new_category)
        await self.db_session.flush()
        return new_category

    async def update_category(self, category_id: UUID, **kwargs):
        query = select(Categories).where(Categories.id == category_id)
        result = await self.db_session.execute(query)
        try:
            category = result.scalar_one()
        except NoResultFound:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(category, key, value)

        await self.db_session.commit()
        return category

    async def get_categories_by_user_id(self, user_id: UUID):
        query = select(Categories).where(Categories.user_id == user_id)
        res = await self.db_session.execute(query)
        list_of_categories = res.scalars().all()
        return list_of_categories

    async def delete_category(self, category_id: UUID, user_id: UUID) -> Union[UUID, None]:
        query = (
            select(Categories)
            .where(Categories.id == category_id, Categories.user_id == user_id)
        )
        result = await self.db_session.execute(query)
        category = result.scalar_one_or_none()

        if category is None:
            return None

        await self.db_session.delete(category)
        await self.db_session.commit()

        return category.id
