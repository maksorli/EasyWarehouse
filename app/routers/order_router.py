from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy import insert, select
from app.schemas import CreateOrder, OrderStatus
from app.backend.db_depends import get_db
from app.models.orders import Order
from sqlalchemy.sql import func
from app.models.products import Product
from app.models.order_item import OrderItem
from typing import List
from sqlalchemy.orm import selectinload


router = APIRouter(prefix='/orders', tags=['orders'])


@router.get('/')
async def get_orders(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.scalars(select(Order).options(selectinload(Order.order_items)))  
    return result.all()

@router.get("/{order_id}")
async def get_order(order_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    order = await db.scalar(
        select(Order).options(selectinload(Order.order_items)).
        where(Order.id == order_id)
    )
    
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Order not found")
    
    return order
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_order(db: Annotated[AsyncSession, Depends(get_db)], 
                       create_order: CreateOrder):
    order = Order(status=create_order.status)
    db.add(order)
    await db.flush()  # Получаем ID заказа

    # Проход по элементам заказа
    for item in create_order.items:
        product = await db.scalar(select(Product).where(Product.id == item.product_id))
        
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        if product.stock < item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough stock")
        
        # Уменьшаем количество на складе
        product.stock -= item.quantity
        db.add(OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity))
                     
    await db.commit()                   
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

 
 
@router.put("/{order_id}/status")
async def update_order_status(order_id: int, 
                              new_status: OrderStatus,  
                              db: Annotated[AsyncSession, Depends(get_db)]):
    order = await db.scalar(select(Order).where(Order.id == order_id))
    
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Order not found")
    
    order.status = new_status
    
    # Сохранение изменений
    await db.commit()
    
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Status updated successfully'
    }