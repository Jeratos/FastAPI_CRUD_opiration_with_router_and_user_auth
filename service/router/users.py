from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schema import UserSchema,UserLogin
from typing import List
from ..hashing import Hash
from jose import jwt
from datetime import datetime, timedelta
from ..auth import get_current_user

router= APIRouter(
    prefix="/user",
    tags=["User"])


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60

#Create User
@router.post("/userregister", status_code=status.HTTP_201_CREATED, )
def create_user(body: UserSchema, db: Session = Depends(get_db)):

    try:
        hashpass = Hash.bcrypt(body.password)

        new_user = models.User(
            username=body.username,
            email=body.email,
            password=hashpass,
            is_admin=False
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "username": new_user.username,
            "email": new_user.email
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# login

@router.post("/userlogin", status_code=status.HTTP_200_OK)
def login_user(body: UserLogin, db: Session = Depends(get_db)):
    try:
        user= db.query(models.User).filter(models.User.email== body.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not Hash.verifypassword(body.password,user.password):        
            raise HTTPException(status_code=400, detail="Incorrect password")
        expire= datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)    

        to_encoded={
            "sub":str(user.id),
            "username":user.username,
            "email":user.email,
            "exp":expire
            }
        access_token = jwt.encode(
            to_encoded,
            SECRET_KEY, 
            algorithm=ALGORITHM
            )
        return {
            "message": "Login successful",
            "token": access_token,
            "token_type": "Bearer"
            } 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/me")
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user
