from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Connection String
# Format: mssql+pyodbc://<username>:<password>@<server>/<database>?driver=ODBC+Driver+17+for+SQL+Server
# DATABASE_URL = "mssql+pyodbc://sa:YourPassword123@localhost/ProductDB?driver=ODBC+Driver+17+for+SQL+Server"
DATABASE_URL = "mysql+mysqldb://user:password@127.0.0.1:3306/myproductdb"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()