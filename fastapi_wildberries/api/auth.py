from fastapi import Depends, HTTPException, APIRouter
from store_app.db.database import SessionLocal
from typing import List, Optional
from sqlalchemy.orm import Session
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
from store_app.db.models import UserProfile, RefreshToken, Cart
from store_app.db.schema import UserProfileSchema, UserProfileLoginSchema, UserProfileCreateSchema
from store_app.db.config import (ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS)


auth_router = APIRouter(prefix='/auth', tags=['Auth'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# register ----------------------------------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@auth_router.post('/', response_model=dict)
async def auth_register(user: UserProfileCreateSchema  = Depends(), db: Session = Depends(get_db)):
    check_username = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    check_email = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if check_username:
        raise HTTPException(status_code=404, detail='User already exists')
    elif check_email:
        raise HTTPException(status_code=404, detail='Email already exists')
    hash_password = get_password_hash(user.password)
    user_db = UserProfile (
        first_name=user.first_name,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        age=user.age,
        phone_number=user.phone_number,
        status=user.status,
        password=hash_password
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    new_cart = Cart(user_id=user_db.id)
    db.add(new_cart)
    db.commit()
    return {'message': 'Account created'}

# login -----------------------------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode =  data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode( to_encode, SECRET_KEY, algorithm=ALGORITHM)
def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

@auth_router.post('/login')
async def login(form_data: UserProfileLoginSchema = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401,  detail="Маалымат туура эмес")
    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})
    new_token = RefreshToken(user_id=user.id, token=refresh_token)
    db.add(new_token)
    db.commit()
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}

# logout ----------------------------------------------------------------------------------------

@auth_router.post('/logout')
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=401, detail="Маалымат туура эмес")
    db.delete(stored_token)
    db.commit()
    return {'message': 'Вышли'}

# refresh -----------------------------------------------------------------------------------------

@auth_router.post('/refresh')
async def refresh(refresh_token: str, db: Session = Depends((get_db))):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=401, detail="Маалымат туура эмес")
    access_token = create_access_token({"sub": stored_token.id})
    return {'access_token': access_token,  'token_type': 'bearer'}