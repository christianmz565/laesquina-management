from sqlalchemy import create_engine, Column, Integer, String, Numeric, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    version = Column(String(50))
    price = Column(Numeric(10, 2))
    file = Column(String(255))

    __table_args__ = (
        Index(
            "ix_title_ngram",
            "title",
            mysql_prefix="FULLTEXT",
            mysql_with_parser="ngram",
        ),
        Index(
            "ix_author_ngram",
            "author",
            mysql_prefix="FULLTEXT",
            mysql_with_parser="ngram",
        ),
    )


def init_db():
    Base.metadata.create_all(bind=engine)


def get_book(db, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def create_book(db, book: Book):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db, book_id: int, updated_data: dict):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        for key, value in updated_data.items():
            setattr(book, key, value)
        db.commit()
        db.refresh(book)
    return book


def delete_book(db, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
    return book


def search_books(
    db, title: str = None, author: str = None, version: str = None, price: float = None
):
    query = db.query(Book)

    if title:
        search_str = f"+{title}*"
        query = query.filter(Book.title.match(search_str, boolean=True))

    if author:
        search_str = f"+{author}*"
        query = query.filter(Book.author.match(search_str, boolean=True))

    if version:
        query = query.filter(Book.version.ilike(f"%{version}%"))

    if price is not None:
        query = query.filter(Book.price == price)

    return query.all()
