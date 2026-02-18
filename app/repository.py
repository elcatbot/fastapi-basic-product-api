from models import ProductEntity
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.execute(select(ProductEntity)).scalars().all()

    def get_by_id(self, id: int):
        return self.db.get(ProductEntity, id)

    def add(self, product: ProductEntity):
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: ProductEntity):
        product = self.db.merge(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product_id: int):
        product = self.db.get(ProductEntity, product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
        return product