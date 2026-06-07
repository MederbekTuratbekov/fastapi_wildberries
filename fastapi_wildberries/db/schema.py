from pydantic import BaseModel, EmailStr
from datetime import datetime
from .models import STATUS_CHOICES
from typing import List, Optional


class UserProfileLoginSchema(BaseModel):
    username: str
    password: str

class UserProfileCreateSchema(BaseModel):
    first_name: str
    lastname: str
    username: str
    email: EmailStr
    age: Optional[int] = None
    phone_number: Optional[str] = None
    password: str
    status: STATUS_CHOICES

    class Config:
        from_attributes = True

class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    lastname: str
    username: str
    email: EmailStr
    age: Optional[int] = None
    phone_number: Optional[str] = None
    created_date: datetime
    status: STATUS_CHOICES

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    id: int
    category_name: str

    class Config:
        from_attributes = True


class ProductGreateSchema(BaseModel):
    category_id: int
    product_name: str
    owner_id: int
    article_number: int
    description: str
    product_type: bool
    product_video: Optional[str] = None
    price: float

    class Config:
        from_attributes = True

class ProductListSchema(BaseModel):
    id: int
    category_id: int
    product_name: str
    owner_id: int
    article_number: int
    description: str
    product_type: bool
    product_video: Optional[str] = None
    price: float
    created_date: datetime

    class Config:
        from_attributes = True


class ReviewCreateSchema(BaseModel):
    author_id: int
    product_id: int
    comment: str
    stars: int

    class Config:
        from_attributes = True

class ReviewGetSchema(BaseModel):
    id: int
    author_id: int
    product_id: int
    comment: Optional[str] = None
    stars: Optional[int] = None
    created_date: datetime

    class Config:
        from_attributes = True


class CartItemSchema(BaseModel):
    id: int
    product_id: int
    quantity: Optional[int] = 1

    class Config:
        from_attributes = True

class CartSchema(BaseModel):
    id: int
    user_id: int
    created_date: datetime
    cart_item: List[CartItemSchema] = []

    class Config:
        from_attributes = True

class CartCreateSchema(BaseModel):
    product_id: int
    quantity: Optional[int] = 1

    class Config:
        from_attributes = True


class FavoriteItemSchema(BaseModel):
    id: int
    favorite_item: int
    product_id: int

    class Config:
        from_attributes = True

class FavoriteSchema(BaseModel):
    id: int
    created_date: datetime
    user_id: int
    favorite_items: List[FavoriteItemSchema] = []

    class Config:
        from_attributes = True

class FavoriteCreateSchema(BaseModel):
    product_id: int

    class Config:
        from_attributes = True