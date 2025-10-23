from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware

from app.routers import categories, products, users, reviews


app = FastAPI(
    title="FastAPI Интернет-магазин",
    version="0.1.0",
)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],           # Разрешенные домены
        allow_credentials=True,                  # Разрешить куки и авторизацию
        allow_methods=["*"],                     # Разрешить все HTTP методы
        allow_headers=["*"],                     # Разрешить все заголовки
        expose_headers=["*"],                    # Какие заголовки доступны клиенту
        max_age=600,                            # Кэшировать preflight запросы на 10 минут
)

# Создаём приложение FastAPI


# Подключаем маршруты категорий
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(reviews.router)

# Корневой эндпоинт для проверки
@app.get("/")
async def root():
    """
    Корневой маршрут, подтверждающий, что API работает.
    """
    return {"message": "Добро пожаловать в API интернет-магазина!"}
