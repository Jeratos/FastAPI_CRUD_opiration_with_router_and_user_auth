from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .schema import UserLogin
from .hashing import Hash

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(
    #token url
    tokenUrl="/user/userlogin")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }