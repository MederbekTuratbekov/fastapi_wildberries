from fastapi import FastAPI
from sqladmin import Admin
from fastapi_wildberries.db.database import engine
from fastapi_wildberries.admin.views import UserProfileAdmin, CategoryAdmin, ProductAdmin, ReviewAdmin

def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ReviewAdmin)
