from fastapi import APIRouter

router = APIRouter(prefix='/orders', tags=['orders'])


@router.get('/')
async def get_orders():
    pass


@router.post('/create')
async def create_order():
    pass
 

@router.patch("/{order_id}/status")
async def update_order_status():
    pass