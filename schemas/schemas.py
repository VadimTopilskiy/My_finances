import re
import uuid
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator, Field
from enum import Enum

from sqlalchemy import Numeric

from db.models import CategoryType

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
LETTER_MATCH_PATTERN_for_category = re.compile(r"^[а-яА-Я]+$")


def _validate_name(value):
    if value and not LETTER_MATCH_PATTERN.match(value):
        raise HTTPException(
            status_code=422, detail="Name should contains only letters"
        )
    return value


def _validate_surname(value):
    if value and not LETTER_MATCH_PATTERN.match(value):
        raise HTTPException(
            status_code=422, detail="Surname should contains only letters"
        )
    return value


def _validate_name_category(value):
    if value and not LETTER_MATCH_PATTERN_for_category.match(value):
        raise HTTPException(
            status_code=422, detail="Name should contains only letters"
        )
    return value


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        from_attributes = True


class ShowUser(TunedModel):
    id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str

    @field_validator("name")
    def validate_new_name(cls, value):
        return _validate_name(value)

    @field_validator("surname")
    def validate_new_surname(cls, value):
        return _validate_surname(value)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator("name")
    def validate_new_name(cls, value):
        return _validate_name(value)

    @field_validator("surname")
    def validate_new_surname(cls, value):
        return _validate_surname(value)


class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class CategoryCreate(TunedModel):
    id: uuid.UUID
    name_cat: str
    type: CategoryType

    @field_validator("name_cat")
    def validate_name_category(cls, value):
        return _validate_name_category(value)


class CategoryShow(TunedModel):
    id: uuid.UUID
    name_cat: str
    type: CategoryType
    user_id: uuid.UUID


class CategoryUpdate(BaseModel):
    id: uuid.UUID
    name_cat: str
    type: CategoryType

    @field_validator("name_cat")
    def validate_name_category(cls, value):
        return _validate_name_category(value)


class DeleteCategoryResponse(BaseModel):
    deleted_category_id: uuid.UUID


class TransactionsCreate(BaseModel):
    category_id: uuid.UUID
    amount: float = Field(..., gt=0)
    type_of_operation: CategoryType


class FinanceShow(BaseModel):
    id: uuid.UUID
    u_cat_id: uuid.UUID
    amount: float
    type_of_operation: CategoryType
    date: str


class CurrentBalanceResponse(BaseModel):
    current_balance: float


class ConvertedBalances(BaseModel):
    balances: dict[str, float]