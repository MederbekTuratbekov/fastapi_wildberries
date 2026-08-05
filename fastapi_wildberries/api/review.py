from fastapi import Depends, HTTPException, APIRouter
from fastapi_wildberries.db.models import Review
from fastapi_wildberries.db.schema import ReviewGetSchema, ReviewCreateSchema
from fastapi_wildberries.db.database import SessionLocal
from typing import List
from sqlalchemy.orm import Session

review_router = APIRouter(prefix='/review', tags=['Review'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@review_router.post('/', response_model=ReviewGetSchema)
async def review_create(review: ReviewCreateSchema, db: Session = Depends(get_db)):
    review_db = Review(**review.model_dump())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.get('/', response_model=List[ReviewGetSchema])
async def review_list(db: Session = Depends(get_db)):
    return db.query(Review).all()

@review_router.get('/{review_id}', response_model=ReviewGetSchema)
async def review_detail(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=404, detail='Review Not Found')
    return review_db

@review_router.put('/{review_id}', response_model=ReviewGetSchema)
async def review_update(review_id: int, review: ReviewCreateSchema, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=404, detail='Review Not Found')
    for review_key, review_value in review.dict().items():
        setattr(review_db, review_key, review_value)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.delete('/{review_id}', response_model=dict)
async def review_delete(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=404, detail='Review Not Found')
    db.delete(review_db)
    db.commit()
    return {'message': 'Review deleted successfully'}
