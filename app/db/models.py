# DBモデル
from sqlalchemy import Column, Integer, Float, DateTime, String
from datetime import datetime
from app.db.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    

class HealthRecord(Base):
    __tablename__ = "health_records"
    
    id = Column(Integer, primary_key=True, index=True)
    height = Column(Float)
    weight = Column(Float)
    bmi = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)