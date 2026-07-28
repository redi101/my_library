from fastapi import APIRouter, status, HTTPException
from schemas.books import SBook, SBookAdd
from database import SessionDep
from repository import BookRepository

router_books = APIRouter(prefix="/books", tags=["books"])


@router_books.post("/", status_code=status.HTTP_201_CREATED)
async def post_book(session: SessionDep, book: SBookAdd) -> SBook:
    result = await BookRepository.add_one(session, book)

    return SBook.model_validate(result)


@router_books.get("/", status_code=status.HTTP_200_OK, response_model=list[SBook])
async def get_books(session: SessionDep):
    result = await BookRepository.get_all_books(session)

    return result


@router_books.get("/{book_id}", status_code=status.HTTP_200_OK, response_model=SBook)
async def get_book(session: SessionDep, book_id: int):
    book = await BookRepository.get_book(book_id, session)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book


@router_books.put("/{book_id}", status_code=status.HTTP_200_OK, response_model=SBook)
async def update_book(session: SessionDep, book_id: int, book: SBookAdd):
    result = await BookRepository.get_update_book(session, book_id, book)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return result


@router_books.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(session: SessionDep, book_id: int):
    result = await BookRepository.delete_book(session, book_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
