from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.database import Base

# class dummy(Base):
#     __tablename__ = "dummy"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     author = Column(String)
#     description = Column(String)
#     rating = Column(Integer)

class clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name  = Column(String)
    email = Column(String)
    
    users = relationship("users", back_populates="client")

class users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    password = Column(String)
    birthday = Column(String)
    is_admin = Column(Boolean)
    is_super_admin = Column(Boolean)
    photo = Column(String)
    client_id = Column(Integer, ForeignKey("clients.id"))

    client = relationship("clients", back_populates="users")


    