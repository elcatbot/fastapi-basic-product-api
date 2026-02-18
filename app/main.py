from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from repository import ProductRepository
from models import ProductEntity
from pydantic import BaseModel
from productdto import ProductDto, ProductCreateDto

# Create tables on startup (Like EnsureCreated)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    product = repo.get_all()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product 

@app.get("/products/{id}", response_model=ProductDto)
def get_product(id: int,db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    product = repo.get_by_id(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product 

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product_dto: ProductCreateDto, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    new_product = ProductEntity(name=product_dto.name, price=product_dto.price)
    return repo.add(new_product)

@app.put("/products/{id}", status_code=status.HTTP_201_CREATED)
def update_product(id: int, product_dto: ProductCreateDto, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    product = repo.get_by_id(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.name = product_dto.name
    product.price = product_dto.price
    return repo.update(product)

@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    return repo.delete(id)

