import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Enum,
    Numeric)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String, nullable=False)

    finances = relationship("Finances", back_populates="users")


class CategoryType(enum.Enum):
    income = "income"
    expense = "expense"


class Finances(Base):
    __tablename__ = "finances"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    u_cat_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    balance = Column(Numeric(10, 2), nullable=False)
    type_of_operation = Column(Enum(CategoryType), nullable=False)
    date = Column(DateTime, default=datetime.now(timezone.utc))

    users = relationship("User", back_populates="finances")
    categories = relationship("Categories", back_populates="finances")


class Categories(Base):
    __tablename__ = "user_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_cat = Column(String, unique=True, nullable=False)
    type = Column(Enum(CategoryType), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    finances = relationship("Finances", back_populates="categories")
