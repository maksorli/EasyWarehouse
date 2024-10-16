from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    stock = Column(Integer)
    slug = Column(String, unique=True, index=True)
     
 