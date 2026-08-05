from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from fastapi_wildberries.db.config import settings

engine = create_engine(settings.DB_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
