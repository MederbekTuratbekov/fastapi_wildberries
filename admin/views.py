from sqladmin import ModelView
from store_app.db.models import UserProfile, Category, Product, Review


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.first_name, UserProfile.lastname, UserProfile.username, UserProfile.status]
    column_searchable_list = [UserProfile.first_name, UserProfile.lastname, UserProfile.username]
    column_sortable_list = [UserProfile.created_date]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]
    column_searchable_list = [Category.category_name]
    column_sortable_list = [Category.id]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.product_name, Product.price, Product.owner_id, Product.category_id]
    column_searchable_list = [Product.product_name]
    column_sortable_list = [Product.created_date, Product.price]


class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id, Review.author_id, Review.product_id, Review.comment, Review.stars]
    column_sortable_list = [Review.created_date, Review.stars]