from pydantic import BaseModel
from typing import Optional

# product schema
class Product(BaseModel):
    id: int
    name: str
    price: int
    approve: bool= False

# service schema
class ServiceSchema(BaseModel):
    title: str
    description: str
    productimage: str
    isapprove: bool = False 
    more_data: Optional[dict] = None

class ServiceTitleData(BaseModel):
    title: str
    description: str
    class Config():
        orm_mode = True

# user register schema
class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    # is_admin: bool = False

class UserLogin(BaseModel):
    email: str
    password: str
