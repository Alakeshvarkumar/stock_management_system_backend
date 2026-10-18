from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CategoryCreate(BaseModel):
    c_name: str = Field(min_length=1, max_length=25)


class RegisterUser(BaseModel):
    email: EmailStr
    name: str
    password: str
    phone: str
    role: Literal["customer", "staff", "admin", "supplier"]


class RegisterUserResponse(BaseModel):
    email: EmailStr
    name: str
    phone: str
    role: Literal["customer", "staff", "admin", "supplier"]

    model_config = ConfigDict(from_attributes=True)


class AllCategories(BaseModel):
    c_id: int
    c_name: str

    model_config = ConfigDict(from_attributes=True)


class ProductSchema(BaseModel):
    p_name: str = Field(min_length=1, max_length=100)
    quantity: int = Field(default=0, ge=0)
    price: Decimal = Field(ge=0)
    min_stock_level: int = Field(default=0, ge=0)
    c_id: int


class ProductSchemaFull(ProductSchema):
    p_id: int
    created_at: datetime
    modified_at: datetime
    category : AllCategories
    model_config = ConfigDict(from_attributes=True)


class ProductSchemaUpdate(BaseModel):
    p_name: str | None = Field(default=None, min_length=1, max_length=100)
    quantity: int | None = Field(default=None, ge=0)
    price: Decimal | None = Field(default=None, ge=0)
    min_stock_level: int | None = Field(default=None, ge=0)
    c_id: int | None = None