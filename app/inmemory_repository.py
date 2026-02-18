from models import ProductEntity
from typing import List, Optional

class ProductRepository:
    def __init__(self):
        # Initial dummy data
        self._products = [
            Product(id=1, name="Keyboard", price=49.99),
            Product(id=2, name="Mouse", price=29.99)
        ]

    def get_all(self) -> List[Product]:
        return self._products

    def get_by_id(self, id: int) -> Optional[Product]:
        return next((p for p in self._products if p.id == id), None)

    def add(self, product: Product):
        self._products.append(product)
        return product

    def update(self, id: int, product_update: Product) -> bool:
        for i, p in enumerate(self._products):
            if p.id == id:
                self._products[i] = product_update
                return True
        return False

    def delete(self, id: int) -> bool:
        original_len = len(self._products)
        self._products = [p for p in self._products if p.id != id]
        return len(self._products) < original_len

# Global instance to act as a Singleton (similar to DI registration)
repo = ProductRepository()