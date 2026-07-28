from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from typing import Annotated
from fastapi import Depends

DATABASE_URL = "sqlite+aiosqlite:////app/data/library.db"

engine = create_async_engine(DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(MappedAsDataclass, DeclarativeBase):
    pass


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
