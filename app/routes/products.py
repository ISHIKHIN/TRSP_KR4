from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from app.database import get_db
from app.models import Product
from app.exceptions import ProductNotFoundException, CustomExceptionA

router = APIRouter(prefix="/products", tags=["products"])


# Pydantic schemas
class ProductCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., gt=0)
    count: int = Field(..., ge=0)
    description: str = Field(default="", max_length=1000)


class ProductUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    price: Optional[float] = Field(None, gt=0)
    count: Optional[int] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=1000)


class ProductResponse(BaseModel):
    id: int
    title: str
    price: float
    count: int
    description: str

    class Config:
        from_attributes = True


# API Endpoints
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    if product.price < 0:
        raise CustomExceptionA("Price cannot be negative")

    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/", response_model=List[ProductResponse])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ProductNotFoundException(product_id)
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ProductNotFoundException(product_id)

    for key, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ProductNotFoundException(product_id)

    db.delete(product)
    db.commit()
    return None