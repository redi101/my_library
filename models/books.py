from database import Model
from sqlalchemy.orm import Mapped, mapped_column


class BooksModel(Model):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    title: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    pages: Mapped[int] = mapped_column()
    is_read: Mapped[bool] = mapped_column(default=False)
