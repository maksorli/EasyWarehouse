# tests/test_orders.py
import pytest
from app.models.products import Product
from app.models.orders import Order
from app.schemas import OrderStatus

# Тест на создание заказа
@pytest.mark.asyncio
async def test_create_order(async_client, test_db):
    # Добавляем продукт для создания заказа
    product = Product(name="Product 2", stock=10)
    test_db.add(product)
    await test_db.commit()
    await test_db.refresh(product)  # Обновляем объект, чтобы получить ID

     
    create_order_data = {
        "status": "в процессе",  
        "items": [{"product_id": product.id, "quantity": 5}]
    }

    # Отправляем POST запрос для создания заказа
    response = await async_client.post("/orders/", json=create_order_data)
    assert response.status_code == 201
    assert response.json()["transaction"] == "Successful"

    # Проверяем, что количество на складе обновлено
    updated_product = await test_db.get(Product, product.id)
    assert updated_product.stock == 5


@pytest.mark.asyncio
async def test_get_orders(async_client, test_db):
    # Создаем заказ
    order = Order(status=OrderStatus.IN_PROCESS.value)
    test_db.add(order)
    await test_db.commit()
    await test_db.refresh(order)

    # Выполняем запрос для получения заказов
    response = await async_client.get("/orders/")
    assert response.status_code == 200

    orders = response.json()
    assert len(orders) == 1
    assert orders[0]["id"] == order.id
    assert orders[0]["status"] == order.status


# Тест на создание заказа с несуществующим продуктом
@pytest.mark.asyncio
async def test_create_order_product_not_found(async_client, test_db):
    create_order_data = {
        "status": OrderStatus.IN_PROCESS.value,
        "items": [{"product_id": 999, "quantity": 1}]
    }

    response = await async_client.post("/orders/", json=create_order_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


# Тест на получение несуществующего заказа
@pytest.mark.asyncio
async def test_get_nonexistent_order(async_client, test_db):
    response = await async_client.get("/orders/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"

 
# Тест на создание заказа с недостаточным количеством товара
@pytest.mark.asyncio
async def test_create_order_insufficient_stock(async_client, test_db):
    # Создаем продукт с ограниченным количеством на складе
    product = Product(name="Product 1", stock=2)
    test_db.add(product)
    await test_db.commit()
    await test_db.refresh(product)

    # Пытаемся создать заказ с количеством, превышающим доступное
    create_order_data = {
        "status": OrderStatus.IN_PROCESS.value,
        "items": [{"product_id": product.id, "quantity": 5}]
    }

    response = await async_client.post("/orders/", json=create_order_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough stock"



