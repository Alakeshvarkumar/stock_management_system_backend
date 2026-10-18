
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from  app import schemas
from app.auth import get_hash_password
def add_category(db:Session, c_name : str):
    new_category=models.Category(c_name = c_name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

def register_user(db:Session, user_obj:schemas.RegisterUser):
    stmt=select(models.User).where(models.User.email==user_obj.email)
    if not db.scalars(stmt).first():
        user_obj.password=get_hash_password(user_obj.password)
        new_user = models.User(**user_obj.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user  

def get_all_categories(db:Session):
    stmt = select(models.Category)
    return db.scalars(stmt).all()


#-----------products crud --------------------------------------------------
def add_product(product:schemas.ProductSchema,user:models.User, db:Session):
    product=models.Product(**product.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    stock_obj=models.StockTransaction(p_id=product.p_id,u_id=user.email,t_type="IN",quantity=product.quantity)
    db.add(stock_obj)
    db.commit()
    db.refresh(stock_obj)
    return product

def get_product(db:Session,product_id:int|None=None):
    if product_id:
        stmt= select(models.Product).where(models.Product.p_id==product_id)
        return db.scalars(stmt).first()
    stmt= select(models.Product)
    return db.scalars(stmt).all()    

def get_product_by_name(product_name:str,db:Session):
    
    stmt= select(models.Product).where(models.Product.p_name==product_name)
    return db.scalars(stmt).all() 

def update_product(p_id:int,product:schemas.ProductSchemaUpdate, db:Session)->models.Product| None:
    db_product= get_product(p_id,db)

    if db_product is None:
        return
    update_product_data = product.model_dump(exclude_unset=True)

    for key,value in update_product_data.items():
        setattr(db_product,key,value)

    db.commit()
    db.refresh(db_product)

    return db_product

#-----------------stock section-----------------------

def handle_stock_transaction(stock_data,db):
    pass