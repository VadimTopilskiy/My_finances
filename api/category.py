from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from repository.dals import CategoryDAL
from schemas.schemas import CategoryCreate, CategoryUpdate


async def _create_new_category(user_id: UUID, body: CategoryCreate, db: AsyncSession):
    async with db.begin():
        category_dal = CategoryDAL(db)
        category = await category_dal.create_new_category(
            user_id=user_id,
            name_cat=body.name_cat,
            category_type=body.type
        )
        return category


async def _update_category(category_id: UUID, user_id: UUID, body: CategoryUpdate, db: AsyncSession):
    async with db.begin():
        category_dal = CategoryDAL(db)
        updated_category = await category_dal.update_category(
            category_id=category_id,
            name=body.name_cat,
            type=body.type,
            user_id=user_id,
        )
        if not updated_category:
            raise HTTPException(status_code=404, detail="category not found")
        return updated_category


async def _get_categories_by_user_id(user_id: UUID, db: AsyncSession):
    async with db.begin():
        category_dal = CategoryDAL(db)
        categories = await category_dal.get_categories_by_user_id(
            user_id=user_id)
        return categories


async def _delete_category(category_id: UUID, user_id: UUID, db: AsyncSession):
    async with db.begin():
        category_dal = CategoryDAL(db)
        deleted_category_id = await category_dal.delete_category(
            category_id=category_id,
            user_id=user_id,
        )
        if not deleted_category_id:
            raise HTTPException(status_code=404, detail="Category not found or not authorized")
        return deleted_category_id
