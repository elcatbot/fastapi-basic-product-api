from pydantic import BaseModel
from typing import Optional

# DTO for incoming data
class ProductDto(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

# DTO for incoming data
class ProductCreateDto(ProductDto):
    pass  # Used for POST requests

class ProductReadDto(ProductDto):
    id: int

    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy models
