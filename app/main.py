from fastapi import FastAPI
from app.api.v1.endpoints import products
from app.db.session import engine, Base


# Create tables on Startup (In production, use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Production API")

# Include all routes from the v1 module
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Python Product API"}