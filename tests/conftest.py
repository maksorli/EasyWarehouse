import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.backend.db import Base
from httpx import AsyncClient
from app.main import app
from dotenv import load_dotenv
import os
import pytest_asyncio

# Загрузка переменных окружения
load_dotenv()

# Создаем асинхронный движок для in-memory базы данных SQLite
@pytest_asyncio.fixture
async def test_db():
    # Создаем движок базы данных SQLite (или укажите другой движок)
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)

    # Создаем асинхронную сессию
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    # Создаем таблицы в базе данных
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Открываем сессию и возвращаем её для тестов
    async with async_session() as session:
        yield session

    # Закрываем движок после завершения тестов
    await engine.dispose()

# Фикстура для асинхронного HTTP клиента
@pytest_asyncio.fixture
async def async_client(test_db):
    from app.backend.db_depends import get_db  # Убедитесь, что путь к get_db правильный

    # Переопределяем зависимость get_db
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    # Очищаем переопределения после завершения тестов
    app.dependency_overrides.clear()