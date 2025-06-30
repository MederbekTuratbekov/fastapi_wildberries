from fastapi import Depends, HTTPException, APIRouter
from store_app.db.models import Cart, CartItem, Product
from store_app.db.schema import CartCreateSchema, CartSchema # CartItemSchema
from store_app.db.database import SessionLocal
from sqlalchemy.orm import Session


cart_router = APIRouter(prefix='/cart', tags=['Cart'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@cart_router.get('/', response_model=CartSchema)
async def cart_list(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first() # есть ли корзина пользователья (по этому id) в базе данных?
    if not cart:
        raise HTTPException(status_code=404, detail=f'Корзина для пользователя с ID {user_id} не найдена в базе данных')
    return cart

@cart_router.post('/', response_model=CartCreateSchema)
async def cart_add(item_data: CartCreateSchema, user_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first() # корзинасы барбы?
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    product = db.query(Product).filter(Product.id == item_data.product_id).first() # есть ли такой продукт в базе данных?
    if not product:
        raise HTTPException(status_code=404, detail='Мындай продукт жок')
    product_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == item_data.product_id).first() # есть ли в конкретной корзине, определённый продукт?
    if product_item:
        raise HTTPException(status_code=400, detail='Продукт уже в корзине')
    cart_item = CartItem(cart_id=cart.id, product_id=item_data.product_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

@cart_router.delete('/{product_id}', response_model=dict)
async def cart_delete(product_id: int, user_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail='база данныхта корзинасы жок')
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first() # есть ли в конкретной корзине, определённый продукт?
    if not cart_item:
        raise HTTPException(status_code=404, detail='Корзинада мындай продукт жок')
    db.delete(cart_item)
    db.commit()
    return {'message': 'Cart item deleted successfully'}
