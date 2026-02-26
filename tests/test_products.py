import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.db.session import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base

# Setup a separate test database (SQLite is fast for tests)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Tell FastAPI to use our test DB instead of the real MySQL DB
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# This creates a 'client' that we can use in our tests
# It acts like the HttpClient
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_create_product(client):
    # Arrange & Act
    response = client.post(
        "/api/v1/products/",
        json={"name": "Test Mouse", "price": 25.0, "description": "Gaming mouse"}
    )
    
    # Assert (Fluent and simple)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Mouse"
    assert "id" in data

def test_get_product_not_found(client):
    # Act
    response = client.get("/api/v1/products/9999")
    
    # Assert
    assert response.status_code == 404
    assert response.json()["error"] == "Resource Not Found"