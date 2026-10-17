from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas

from .database import get_db

router = APIRouter()

@router.post("/categories",status_code=201)
def create_category(data:schemas.CategoryCreate , db: Session = Depends(get_db)):  # noqa: B008
    new_category=crud.add_category(db,data.c_name)
    return {"message": "Category created successfully",
            "c_id":new_category.c_id}

# @router.post("/register", status_code=201,response_model=schemas.RegisterUserResponse)
# def register_user(user:schemas.RegisterUser,db=Depends(get_db)):  
#     new_user=crud.register_user(db,user)
#     return new_user

@router.get("/categories",status_code=200,response_model=list[schemas.AllCategories])
def get_all_categories(db:Session=Depends(get_db)):# noqa: B008
    return crud.get_all_categories(db)

@router.post("/products",status_code=201,response_model=schemas.ProductSchemaFull)
def add_product(product:schemas.ProductSchema,db:Session=Depends(get_db)):# noqa: B008
    new_product = crud.add_product(product,db)
    return new_product

@router.get("/products",status_code=200,response_model=list[schemas.ProductSchemaFull])
def get_products(product_name: str | None = None,db: Session = Depends(get_db)):  # noqa: B008)
    if product_name:
        return crud.get_product_by_name(product_name, db)
    return crud.get_product(db)



@router.get("/products/{p_id}",status_code=200,response_model=schemas.ProductSchemaFull)
def get_product(p_id :int,db:Session= Depends(get_db)):
    return crud.get_product(p_id,db)


@router.patch("/products/{p_id}",status_code=200,response_model=schemas.ProductSchemaFull)
def update_product(product:schemas.ProductSchemaUpdate, p_id:int, db:Session= Depends(get_db)):
    updated_product=crud.update_product(p_id,product,db)
    if updated_product is None:
        return HTTPException(404,"Product Not Found ")
    return updated_product

    

