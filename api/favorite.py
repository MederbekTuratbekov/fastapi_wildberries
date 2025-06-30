from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from store_app.db.database import SessionLocal
from store_app.db.models import Favorite, FavoriteItem, Product
from store_app.db.schema import FavoriteSchema, FavoriteCreateSchema # FavoriteItemSchema


favorite_router = APIRouter(prefix='/favorite', tags=['Favorite'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@favorite_router.get('/', response_model=FavoriteSchema)
async def favorite_list(user_id:int, db:Session=Depends(get_db)):
    favorite_db = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if favorite_db is None:
        raise HTTPException(status_code=404, detail='Обьект для хранение избранных товаров не нашлось')
    return favorite_db

@favorite_router.post('/', response_model=FavoriteCreateSchema)
async def cart_add(item_data: FavoriteCreateSchema, user_id: int, db: Session = Depends(get_db)):
    favorite_db = db.query(Favorite).filter(Favorite.user_id == user_id).first() # избранный сакталуучу жай барбы?
    if not favorite_db:
        favorite_new = Favorite(user_id=user_id)
        db.add(favorite_new)
        db.commit()
        db.refresh(favorite_new)
    product = db.query(Product).filter(Product.id == item_data.product_id).first() # есть ли такой продукт в базе данных?
    if not product:
        raise HTTPException(status_code=404, detail='Мындай продукт жок')
    product_item = db.query(FavoriteItem).filter(FavoriteItem.favorite_item == favorite_db.id, FavoriteItem.product_id == item_data.product_id).first() # есть ли в конкретной корзине, определённый продукт?
    if product_item:
        raise HTTPException(status_code=400, detail='Продукт уже в корзине')
    favorite_item = FavoriteItem(favorite_id=favorite_db.id, product_id=item_data.product_id)
    db.add(favorite_item)
    db.commit()
    db.refresh(favorite_item)
    return favorite_item

@favorite_router.delete('/{product_id}', response_model=dict)
async def favorite_delete(product_id: int, user_id: int, db: Session = Depends(get_db)):
    favorite_db = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if not favorite_db:
        raise HTTPException(status_code=404, detail='база данныхта корзинасы жок')
    favorite_item = db.query(FavoriteItem).filter(FavoriteItem.favorite_item == favorite_db.id, FavoriteItem.product_id == product_id).first() # есть ли в конкретной корзине, определённый продукт?
    if not favorite_item:
        raise HTTPException(status_code=404, detail='Корзинада мындай продукт жок')
    db.delete(favorite_item)
    db.commit()
    return {'message': 'Cart item deleted successfully'}
