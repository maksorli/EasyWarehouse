from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy import insert, select
from slugify import slugify
from app.schemas import CreateOrder
from app.backend.db_depends import get_db
from app.models.orders import Order
from sqlalchemy.sql import func

router = APIRouter(prefix='/orders', tags=['orders'])


@router.get('/')
async def get_orders(db: Annotated[AsyncSession, Depends(get_db)]):
    orders = await db.scalars(select(Order))
    return orders.all()
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_order(db: Annotated[AsyncSession, Depends(get_db)], 
                       create_order: CreateOrder):
    await db.execute(
        insert(Order).values(status=create_order.status)
    )
                                        
    await db.commit()                   
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

 

@router.patch("/{order_id}/status")
async def update_order_status():
    pass