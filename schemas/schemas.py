import re
import uuid
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        from_attributes = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


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
