from typing import Union

from sqlalchemy import select, update, and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from uuid import UUID

from repository.hashing import Hasher


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
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]
