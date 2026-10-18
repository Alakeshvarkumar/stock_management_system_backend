from pwdlib import PasswordHash
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models
from datetime import timedelta,timezone,datetime
import jwt
import os
from dotenv import load_dotenv

password_hash=PasswordHash.recommended()
DUMMY_HASED_PASSWORD=password_hash.hash("mydummypasswordtoconfusehacker")
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def get_hash_password(password:str)->str:
    return password_hash.hash(password)

def verify_hash_password(password:str,hash_password:str):
    return password_hash.verify(password,hash_password)

def get_user(user_email:str,db:Session):
    stmt=select(models.User).where(models.User.email==user_email)
    return db.scalars(stmt).first()
   
def authenticate(email:str,password:str,db:Session)->models.User:
    db_user=get_user(email,db)
    if not db_user:
        verify_hash_password(password,DUMMY_HASED_PASSWORD)
        return False
    if not verify_hash_password(password,db_user.password):
        return False
    return db_user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) +( expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
