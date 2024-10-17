from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy import insert, select, update, delete
from slugify import slugify
from app.schemas import CreateProduct
from app.backend.db_depends import get_db
from app.models.products import Product
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def get_products(db: Annotated[AsyncSession, Depends(get_db)]):
    products = await db.scalars(select(Product))
    return products.all()

@router.get('/{product_id}')
async def get_product(db: Annotated[AsyncSession, Depends(get_db)], 
                      product_id: int):
    product = await db.scalar(select(Product).
                              where(Product.id == product_id))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    
    return product
 
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[AsyncSession, Depends(get_db)],
                         create_product: CreateProduct):
    await db.execute(insert(Product).values(name=create_product.name,
                                       stock=create_product.stock,
                                       description=create_product.description,
                                       price=create_product.price))
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put('/{product_id}')
async def update_product(db: Annotated[AsyncSession, Depends(get_db)], 
                         product_id: int,
                         update_product_model: CreateProduct):
    product_update = await db.scalar(select(Product).
                                     where(Product.id == product_id))
    if product_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )
    await db.execute(
                update(Product).where(Product.id == product_id)
                .values(name=update_product_model.name,
                        description=update_product_model.description,
                        price=update_product_model.price,
                        stock=update_product_model.stock,
                        slug=slugify(update_product_model.name)))
    await db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product update is successful'
    }



@router.delete('/{product_id}')
async def delete_product(db: Annotated[AsyncSession, Depends(get_db)], 
                         product_id: int):
   
    product_delete = await db.scalar(select(Product).
                                     where(Product.id == product_id))
    if product_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )
    await db.execute(delete(Product).where(Product.id == product_id) )
    await db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product delete is successful'
    }