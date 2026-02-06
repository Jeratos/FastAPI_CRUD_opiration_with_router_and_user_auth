from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schema import UserSchema,UserLogin
from typing import List
from ..hashing import Hash
router= APIRouter(
    prefix="/user",
    tags=["User"])



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
   user= db.query(models.User).filter(models.User.email== body.email).first()
   if not user:
       raise HTTPException(status_code=404, detail="User not found")
   if not Hash.verifypassword(body.password,user.password):        
       raise HTTPException(status_code=400, detail="Incorrect password")
   return {"message": "Login successful"}
