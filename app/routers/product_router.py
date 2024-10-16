from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert
from slugify import slugify
from app.schemas import CreateProduct
from app.backend.db_depends import get_db
from app.models.products import Product

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def get_products():
    pass

@router.get('/{product_id}')
async def get_products():
    pass


 
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[Session, Depends(get_db)], create_product: CreateProduct):
    await db.execute(insert(Product).values(name=create_product.name,
                                       slug=slugify(create_product.name)))
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put('/')
async def update_product():
    pass


@router.delete('/{product_id}')
async def delete_product():
    pass