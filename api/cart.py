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
    cart_db = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart_db:
        raise HTTPException(status_code=404, detail='Cart Not Found')
    return cart_db

@cart_router.post('/', response_model=CartCreateSchema)
async def cart_add(item_data: CartCreateSchema, user_id: int, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart_db:
        cart_db = Cart(user_id=user_id)
        db.add(cart_db)
        db.commit()
        db.refresh(cart_db)
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product Not Found')
    product_item = db.query(CartItem).filter(CartItem.cart_id == cart_db.id, CartItem.product_id == item_data.product_id).first()
    if product_item:
        raise HTTPException(status_code=400, detail='Продукт уже в корзине')
    cart_item = CartItem(cart_id=cart_db.id, product_id=item_data.product_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

@cart_router.delete('/{product_id}', response_model=dict)
async def cart_delete(product_id: int, user_id: int, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart_db:
        raise HTTPException(status_code=404, detail='Cart Not Found')
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart_db.id, CartItem.product_id == product_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail='Product Not Found in Cart')
    db.delete(cart_item)
    db.commit()
    return {'message': 'Cart item deleted successfully'}