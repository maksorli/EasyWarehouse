# EasyWarehouse
### API для управления складом


![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat&logo=python)
![Docker](https://img.shields.io/badge/Docker-20.10-blue?style=flat&logo=docker)
![alembic](https://img.shields.io/badge/alembic-1.13.3-green?style=flat&logo=python)
![fastapi-slim](https://img.shields.io/badge/fastapi--slim-0.115.2-blue?style=flat&logo=python)
![pydantic](https://img.shields.io/badge/pydantic-2.9.2-blue?style=flat&logo=python)
![pytest](https://img.shields.io/badge/pytest-8.3.3-green?style=flat&logo=python)
![pytest-asyncio](https://img.shields.io/badge/pytest--asyncio-0.24.0-blue?style=flat&logo=python)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.36-orange?style=flat&logo=python)
![aiosqlite](https://img.shields.io/badge/aiosqlite-0.20.0-blue?style=flat&logo=python)
 

## Описание проекта
Данный проект представляет собой REST API для управления процессами на складе, разработанный с использованием FastAPI. API позволяет управлять товарами, складскими запасами и заказами

## Основные возможности
### Управление товарами:
Создание, просмотр, обновление и удаление товаров.
### Управление заказами:
Создание заказов с проверкой наличия товаров на складе.

Обновление статуса заказов.
Просмотр списка заказов и деталей конкретного заказа.
### Бизнес-логика:
Проверка наличия достаточного количества товара при создании заказа.

Обновление количества товара на складе при оформлении заказа.

#### Документация API:
Использование встроенной документации FastAPI (Swagger/OpenAPI).

#### Асинхронные запросы:
Использование асинхронного взаимодействия для повышения производительности.

### Миграции базы данных:
Управление схемой базы данных с помощью Alembic

 
 ## Установка и запуск
С использованием Docker
1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/maksorli/EasyWarehouse.git
2. Проверьте версию Docker и Docker Compose, либо установите:
    ```bash
    docker --version
    docker-compose --version
3. Создайте файл .env  с переменными окружения (пример: .env.example)
    ```bash
        # Параметры подключения к базе данных
    POSTGRES_USER=easywarehouse
    POSTGRES_PASSWORD=qwertyu
    POSTGRES_DB=easywarehouse
    POSTGRES_HOST=db
    POSTGRES_PORT=5432

    # Строка подключения к базе данных
    DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
    PYTHONPATH=.
4. Запустите проект с помощью Docker Compose:
   ```bash
   docker-compose up --build