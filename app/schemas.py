from pydantic import BaseModel
from typing import List
from enum import Enum

class OrderStatus(str, Enum):
    IN_PROCESS = "в процессе"
    SHIPPED = "отправлен"
    DELIVERED = "доставлен"
    CANCELLED = "отменён"

class OrderUpdateStatus(BaseModel):
    status: OrderStatus

class CreateProduct(BaseModel):
    name: str
    description: str
    price: int
    stock: int
    
class OrderItemCreate(BaseModel):
    product_id: int   
    quantity: int    

class CreateOrder(BaseModel):
    status: OrderStatus = OrderStatus.IN_PROCESS
    items: List[OrderItemCreate]

