from app.db.entities.product import ProductEntity
from app.schemas.product_dto import ProductCreateDto
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

class CRUDProduct:

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        query = select(ProductEntity).offset(skip).limit(limit)
        return db.execute(query).scalars().all()

    def get_by_id(self, db: Session, id: int):
        return db.get(ProductEntity, id)

    def create(self, db: Session, obj_in: ProductCreateDto):
        obj_in = ProductEntity(
            name=obj_in.name,
            price=obj_in.price,
            description=obj_in.description
        )
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def update(self, db: Session, obj_in: ProductEntity):
        product = db.merge(obj_in)
        db.commit()
        db.refresh(product)
        return product

    def delete(self, db: Session, product_id: int):
        product = db.get(ProductEntity, product_id)
        if product:
            db.delete(product)
            db.commit()
        return product
    
product_crud = CRUDProduct()