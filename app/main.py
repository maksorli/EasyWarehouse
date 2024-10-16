from fastapi import FastAPI
from app.routers import order_router, product_router

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "EasyWarehouse  app"}


app.include_router(product_router.router)
app.include_router(order_router.router)