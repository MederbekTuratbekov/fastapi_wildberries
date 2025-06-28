from .database import Base
from sqlalchemy import (ForeignKey, String, Integer, DateTime, Enum, Text, Boolean, DECIMAL,TIMESTAMP )
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum as PyEnum


class STATUS_CHOICES(str, PyEnum):
    gold = 'gold'
    silver = 'silver'
    bronze = 'bronze'
    simple = 'simple'

class UserProfile(Base):
    __tablename__ = 'userprofile'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32))
    lastname: Mapped[str] = mapped_column(String(32))
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[STATUS_CHOICES] = mapped_column(Enum(STATUS_CHOICES), default=STATUS_CHOICES.simple)
    created_date: Mapped[int] = mapped_column(TIMESTAMP, default=lambda : datetime.now(timezone.utc))

    owner_product: Mapped[List['Product']] = relationship('Product', back_populates='owner', cascade='all, delete-orphan')
    author_review: Mapped[List['Review']] = relationship('Review', back_populates='author', cascade='all, delete-orphan')
    user_token: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user', cascade='all, delete-orphan')
    user_cart: Mapped['Cart'] = relationship('Cart', back_populates='user', cascade='all, delete-orphan', uselist=True)

    def __str__(self):
        return f'{UserProfile.lastname}, {UserProfile.first_name}'

class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[int] = mapped_column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))

    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_token')

    def __str__(self):
        return f'{RefreshToken.token}'

class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_name: Mapped[str] = mapped_column(String, unique=True)

    product_category: Mapped[List['Product']] = relationship('Product', back_populates='category', cascade='all, delete-orphan')

    def __str__(self):
        return f'{Category.category_name}'

class Product(Base):
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    product_name: Mapped[str] = mapped_column(String)
    article_number: Mapped[int] = mapped_column(Integer, unique=True)
    description: Mapped[str] = mapped_column(Text)
    product_type: Mapped[bool] = mapped_column(Boolean)
    product_video: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    created_date: Mapped[int] = mapped_column(TIMESTAMP, default=lambda : datetime.now(timezone.utc))

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship(Category, back_populates='product_category')
    owner_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    owner: Mapped[UserProfile] = relationship(UserProfile, back_populates='owner_product')
    product_review: Mapped[List['Review']] = relationship('Review', back_populates='product', cascade='all, delete-orphan')

    def __str__(self):
        return f'{Product.product_name}'

class Review(Base):
    __tablename__ = 'review'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    stars: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_date: Mapped[int] = mapped_column(TIMESTAMP, default=lambda : datetime.now(timezone.utc))

    author_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    author: Mapped[UserProfile] = relationship(UserProfile, back_populates='author_review')
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped[Product] = relationship(Product, back_populates='product_review')

    def __str__(self):
        return f'{Review.comment}'

class Cart(Base):
    __tablename__ = 'cart'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    created_date: Mapped[int] = mapped_column(TIMESTAMP, default=lambda : datetime.now(timezone.utc))

    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'), unique=True)
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_cart')
    cart_cartitem: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')

    def __str__(self):
        return f'{Cart.id}'

class CartItem(Base):
    __tablename__ = 'cart_item'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    cart: Mapped['Cart'] = relationship('Cart', back_populates='cart_cartitem')
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped['Product'] = relationship('Product')

    def __str__(self):
        return f'{CartItem.quantity}'