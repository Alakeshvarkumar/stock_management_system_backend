from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    text,
)

from .database import Base


class Category(Base):
    __tablename__ = "category"

    c_id = Column(Integer,primary_key=True,autoincrement=True)
    c_name = Column(String(25),nullable=False)

class User(Base):
    __tablename__ = "users"
    email = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    password = Column( String(255), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    role = Column(
        Enum("customer", "staff", "admin", "supplier"),
        nullable=False,
    )

class Product(Base):
    __tablename__ = "products"
    p_id = Column(Integer, primary_key=True, autoincrement=True)
    p_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False,default=0)
    price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    modified_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    minimal_stock_level = Column(Integer, nullable=False, default=0)
    c_id = Column(Integer, ForeignKey("category.c_id"), nullable=False)


class StockTransaction(Base):
    __tablename__ = "transaction"

    t_id = Column(Integer, primary_key=True)
    p_id = Column(Integer, ForeignKey("products.p_id"))
    u_id = Column(String(50), ForeignKey("users.email"))
    t_type = Column(Enum("IN", "OUT"))
    quantity = Column(Integer, nullable=False)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )

