from schemas.books import SBookAdd
from sqlalchemy.ext.asyncio import AsyncSession
from models.books import BooksModel
from sqlalchemy import select


class BookRepository:
    @classmethod
    async def add_one(cls, session: AsyncSession, data: SBookAdd) -> BooksModel:

        data_dict = data.model_dump()
        book = BooksModel(**data_dict)

        session.add(book)
        await session.commit()
        await session.refresh(book)

        return book

    @classmethod
    async def get_all_books(cls, session: AsyncSession) -> list[BooksModel]:
        query = select(BooksModel)

        result = await session.execute(query)

        return list(result.scalars().all())

    @classmethod
    async def get_book(cls, book_id: int, session: AsyncSession) -> BooksModel | None:
        query = select(BooksModel).where(BooksModel.id == book_id)
        result = await session.execute(query)

        return result.scalars().first()

    @classmethod
    async def get_update_book(
        cls, session: AsyncSession, book_id: int, new_book: SBookAdd
    ) -> BooksModel | None:
        query = select(BooksModel).where(BooksModel.id == book_id)

        result = await session.execute(query)

        book = result.scalars().first()
        if not book:
            return None
        for key, value in new_book.model_dump().items():
            setattr(book, key, value)

        await session.commit()
        return book

    @classmethod
    async def delete_book(cls, session: AsyncSession, book_id: int) -> bool:
        query = select(BooksModel).where(BooksModel.id == book_id)
        result = await session.execute(query)
        book = result.scalars().first()

        if not book:
            return False

        await session.delete(book)
        await session.commit()

        return True
