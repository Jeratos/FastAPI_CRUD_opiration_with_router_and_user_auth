from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship


class Service(Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    productimage = Column(String)
    isapprove = Column(Boolean)
    more_data = Column(JSON)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="services")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String,unique=True)
    password = Column(String)
    # default value
    is_admin = Column(Boolean, default=False)

    services = relationship("Service", back_populates="user")