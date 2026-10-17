from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

user = 'root'
password = "Alakesh%4018"
host = "localhost"
port = 3306
database = "stock_mgmt_db"

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
        print("DB Connection")
    finally:
        db.close()