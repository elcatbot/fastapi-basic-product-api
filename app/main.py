from fastapi import FastAPI
from app.api.v1.endpoints import products
from app.db.session import engine, Base
from app.core.exceptions import global_exception_handler, sqlalchemy_integrity_handler, entity_not_found_handler, EntityNotFoundError
from sqlalchemy.exc import IntegrityError

# Create tables on Startup (In production, use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Production API")

# Register the global handler for all Exception types
app.add_exception_handler(Exception, global_exception_handler)

# Catch specific SQL errors (The specialized handler)
app.add_exception_handler(IntegrityError, sqlalchemy_integrity_handler)

# Catch EntityNotFound error
app.add_exception_handler(EntityNotFoundError, entity_not_found_handler)

# Include all routes from the v1 module
app.include_router(products.router, prefix="/api/v1", tags=["products"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Python Product API"}