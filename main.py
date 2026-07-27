from fastapi import FastAPI
from routers.books import router_books
from contextlib import asynccontextmanager
from database import engine, Model
import models.books


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    print("База данных готова к работе")
    yield
    print("Выключение сервера")


app = FastAPI(
    title="MyLibrary",
    description="Учебное приложение для курса по FastAPI",
    version="0.0.1",
    lifespan=lifespan,
)

app.include_router(router_books)
