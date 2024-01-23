from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.products import ProductCreate, ProductRead
from database import get_db
from typing import List
from ..models.products import product_table
from ..crud.products import (
    crud_create_product,
    crud_get_product,
    crud_get_all_products,
    crud_update_product,
    crud_delete_product,
)

product_router = APIRouter(
    tags=['products']
)
@product_router.get("/products/", response_model=List[ProductRead])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(product_table).offset(skip).limit(limit).all()

@product_router.post("/products/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    created_product = crud_create_product(db, product)
    return created_product

@product_router.get("/products/{product_id}", response_model=ProductRead)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@product_router.put("/products/{product_id}")
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    updated_product = crud_update_product(db, product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@product_router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted_product = crud_delete_product(db, product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product
