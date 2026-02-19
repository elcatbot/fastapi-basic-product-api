from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.crud.crud_product import product_crud
from app.schemas.product_dto import ProductReadDto, ProductCreateDto

router = APIRouter()

@router.get("/products", response_model=List[ProductReadDto])
def read_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return product_crud.get_all(db, skip = 0, limit = 100)

@router.get("/products/{id}", response_model=ProductReadDto)
def read_product(id: int, db: Session = Depends(get_db)):
    product = product_crud.get_by_id(db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product 

@router.post("/products", status_code=status.HTTP_201_CREATED, response_model=ProductReadDto)
def create_product(product_in: ProductCreateDto, db: Session = Depends(get_db)):
    return product_crud.create(db, obj_in=product_in)

@router.put("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_product(id: int, product_dto: ProductCreateDto, db: Session = Depends(get_db)):
    product = product_crud.get_by_id(db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.name = product_dto.name
    product.price = product_dto.price
    product.description = product_dto.description
    product_crud.update(db, product)
    return 

@router.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    product_crud.delete(db, product_id=id)
    return 

