# DBモデル
from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from app.db.database import Base


class HealthRecord(Base):
    __tablename__ = "health_records"
    
    id = Column(Integer, primary_key=True, index=True)
    height = Column(Float)
    weight = Column(Float)
    bmi = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)