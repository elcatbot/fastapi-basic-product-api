from pydantic import BaseModel

# DTO for incoming data
class ProductDto(BaseModel):
    name: str
    price: float

# DTO for incoming data
class ProductCreateDto(BaseModel):
    name: str
    price: float