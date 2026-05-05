from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False, default=0)
    description = Column(String(1000), nullable=False, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())