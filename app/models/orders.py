from app.backend.db import Base
from sqlalchemy import Column, ForeignKey,Enum as SqlEnum, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum

class OrderStatus(str, Enum):
    IN_PROCESS = "в процессе"
    SHIPPED = "отправлен"
    DELIVERED = "доставлен"
    CANCELLED = "отменён"

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    created_at =  Column(DateTime, server_default=func.now()) 
    status = Column(SqlEnum(OrderStatus), default=OrderStatus.IN_PROCESS)
    order_items = relationship("OrderItem", back_populates="order")