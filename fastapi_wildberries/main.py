from fastapi import FastAPI
import uvicorn
from fastapi_wildberries.api import category, product, review, auth, social_auth, cart, favorite
from starlette.middleware.sessions import SessionMiddleware
from fastapi_wildberries.admin.setup import setup_admin
from fastapi_wildberries.db.config import SECRET_KEY


online_store = FastAPI()
online_store.include_router(category.category_router)
online_store.include_router(product.product_router)
online_store.include_router(review.review_router)
online_store.include_router(auth.auth_router)
online_store.include_router(social_auth.social_router)
online_store.include_router(cart.cart_router)
online_store.include_router(favorite.favorite_router)
online_store.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
setup_admin(online_store)

if __name__ == '__main__':
    uvicorn.run(online_store, host='127.0.0.1', port=8000)
