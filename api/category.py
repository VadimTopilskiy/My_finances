from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from service.auth import get_current_user_from_token
from service.category import _create_new_category, _update_category, _delete_category, _get_categories_by_user_id
from db.models import User
from db.session import get_db
from schemas.schemas import CategoryCreate, CategoryShow, DeleteCategoryResponse
from uuid import UUID

category_router = APIRouter()


@category_router.post("/categories/", response_model=CategoryShow)
async def create_category(
        body: CategoryCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    return await _create_new_category(body.id, body, db)


@category_router.put("/categories/{category_id}", response_model=CategoryShow)
async def update_category(
        category_id: UUID,
        user_id: UUID,
        category: CategoryCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    return await _update_category(category_id, user_id, category, db)


@category_router.delete("/categories/{category_id}", response_model=DeleteCategoryResponse)
async def delete_category(
        category_id: UUID,
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    deleted_category_id = await _delete_category(category_id, user_id, db)
    if deleted_category_id is None:
        raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found.")
    return DeleteCategoryResponse(deleted_category_id=deleted_category_id)


@category_router.get("/categories/", response_model=List[CategoryShow])
async def get_categories_by_user_id(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)):
    user_id = current_user.id
    categories = await _get_categories_by_user_id(user_id, db)
    return categories

