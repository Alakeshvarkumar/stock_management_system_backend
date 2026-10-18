from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime,timezone,timedelta
from app import crud, schemas,auth
import jwt
from .database import get_db
from jwt import InvalidTokenError
router = APIRouter()

#--------------dependencies---------------
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
Oauth2_tokenD=Annotated[str,Depends(oauth2_scheme)]
Oauth2_formD=Annotated[OAuth2PasswordRequestForm,Depends()]
DbSession=Annotated[Session,Depends(get_db)]
credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_user_from_token(token:Oauth2_tokenD,db:DbSession):
    try:
        payload=jwt.decode(token,auth.SECRET_KEY,[auth.ALGORITHM])
        username=payload.get("sub")
        role=payload.get("role")
        if username is None:
            raise credentials_exception
        token_data=schemas.TokenData(username=username,role=role) 
    except InvalidTokenError:
        raise credentials_exception
    user=auth.get_user(token_data.username,db)     #this username is emailid  since outh expects username but we use emailid
    if user is None:
        raise credentials_exception
    return user

Current_userD=Annotated[schemas.UserSchema,Depends(get_user_from_token)]


#-----------user routes-----------------
@router.post("/register", status_code=201,response_model=schemas.RegisterUserResponse)
def register_user(user:schemas.RegisterUser,db=Depends(get_db)):  
    new_user=crud.register_user(db,user)
    if new_user:
        return new_user
    else:
        raise HTTPException(status_code=409,detail="Email already present! use another email")

@router.post("/login")
def login_to_get_access_token(form_data:Oauth2_formD,db:Session=Depends(get_db))->schemas.Token:
    auth_user=auth.authenticate(form_data.username,form_data.password,db)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": auth_user.email,"role":auth_user.role})
    return schemas.Token(access_token=access_token, token_type="bearer")


#--------------categories routes-----------
@router.post("/categories",status_code=201)
def create_category(data:schemas.CategoryCreate , db: Session = Depends(get_db)):  # noqa: B008
    new_category=crud.add_category(db,data.c_name)
    return {"message": "Category created successfully",
            "c_id":new_category.c_id}


@router.get("/categories",status_code=200,response_model=list[schemas.AllCategories])
def get_all_categories(db:Session=Depends(get_db)):# noqa: B008
    return crud.get_all_categories(db)


#------------add products ----------------
@router.post("/products",status_code=201,response_model=schemas.ProductSchemaFull)
def add_product(product:schemas.ProductSchema,user:Current_userD,db:Session=Depends(get_db)):# noqa: B008
    new_product = crud.add_product(product,user,db)
    #-------use user
    return new_product


#-----------PRODUCTS FETCH 
@router.get("/products",status_code=200,response_model=list[schemas.ProductSchemaFull])
def get_products(product_name: str | None = None,db: Session = Depends(get_db)):   # noqa: B008
    if product_name:
        return crud.get_product_by_name(product_name, db)
    return crud.get_product(db)

@router.get("/products/{p_id}",status_code=200,response_model=schemas.ProductSchemaFull)
def get_product(p_id :int,db:Session= Depends(get_db)):# noqa: B008
    return crud.get_product(product_id=p_id,db=db)


#----------products update-------------
@router.patch("/products/{p_id}",status_code=200,response_model=schemas.ProductSchemaFull)
def update_product(product:schemas.ProductSchemaUpdate, p_id:int, db:Session= Depends(get_db)):# noqa: B008
    updated_product=crud.update_product(p_id,product,db)
    if updated_product is None:
        return HTTPException(404,"Product Not Found ")
    return updated_product

#------
# @router.post("/stockIn/")
# def stockIn(stock_data:schemas.StockTransactionRequest,db:DbSession):

            

    

