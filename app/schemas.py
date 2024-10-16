from pydantic import BaseModel
from datetime import datetime

class CreateProduct(BaseModel):
    name: str
    description: str
    price: int
    stock: int
    


class CreateOrder(BaseModel):
    status: str