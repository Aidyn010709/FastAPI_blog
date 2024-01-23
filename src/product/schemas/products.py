from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    title : str
    image : str
    price : float
    description : str
    date : Optional[datetime]

class Product(BaseModel):
    title : str
    image : str
    price : float
    description : str
    date : Optional[datetime]

class ProductRead(Product):
    id : int 
