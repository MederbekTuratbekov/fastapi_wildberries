from fastapi import Depends, HTTPException, APIRouter
from fastapi_wildberries.db.models import Product
from fastapi_wildberries.db.schema import ProductCreateSchema, ProductListSchema
from fastapi_wildberries.db.database import SessionLocal
from typing import List
from sqlalchemy.orm import Session

product_router = APIRouter(prefix='/product', tags=['Product'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_router.post('/', response_model=ProductListSchema)
async def product_create(product: ProductCreateSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.model_dump())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db

@product_router.get('/', response_model=List[ProductListSchema])
async def product_list(db: Session = Depends(get_db)):
    return db.query(Product).all()

@product_router.get('/{product_id}', response_model=ProductListSchema)
async def product_detail(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Product Not Found')
    return product_db

@product_router.put('/{product_id}', response_model=dict)
async def product_update(product: ProductCreateSchema, product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Product Not Found')
    for product_key, product_value in product.dict().items():
        setattr(product_db, product_key, product_value)
    db.commit()
    db.refresh(product_db)
    return {'message': 'Update'}

@product_router.delete('/{product_id}', response_model=dict)
async def product_delete(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Product Not Found')
    db.delete(product_db)
    db.commit()
    return {'message': 'Deleted'}
