# db.py
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()  # type: ignore


# models
class Computation(Base):
    __tablename__ = "computations"
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String)
    input = Column(String)
    result = Column(String)
    cached = Column(Boolean)
    api_key = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class DeletedItem(Base):
    __tablename__ = "deleted_items"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, index=True)
    value = Column(Text)
    reason = Column(String, default="manual delete")
    operation = Column(String, default="unknown")
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
