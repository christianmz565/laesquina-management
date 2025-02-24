from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Numeric,
    Index,
    select,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import match
from sqlalchemy.orm import sessionmaker, Session
from .env import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    authors = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2))
    category_id = Column(Integer, index=True)
    file = Column(String(255))

    __table_args__ = (
        Index(
            "ix_title_ngram",
            "title",
            mysql_prefix="FULLTEXT",
            mysql_with_parser="ngram",
        ),
        Index(
            "ix_authors_ngram",
            "authors",
            mysql_prefix="FULLTEXT",
            mysql_with_parser="ngram",
        ),
    )


def init_db():
    Base.metadata.create_all(bind=engine)


def get_book_orm(db: Session, book_id: int):
    return db.execute(select(Book).where(Book.id == book_id)).first()[0]


def create_book_orm(db: Session, book: Book):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book_orm(db: Session, book: Book, updated_data: dict):
    if book:
        for key, value in updated_data.items():
            setattr(book, key, value)
        db.commit()
        db.refresh(book)
    return book


def delete_book_orm(db: Session, book_id: int):
    book = get_book_orm(db, book_id)
    if book:
        db.delete(book)
        db.commit()
    return book


def create_category_orm(db: Session, category: Category):
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories_orm(db: Session):
    return [category[0] for category in db.execute(select(Category)).all()]


def get_category_orm(db: Session, category_id: int):
    return db.execute(select(Category).where(Category.id == category_id)).first()[0]


def search_books_orm(
    db: Session, title: str = None, authors: str = None, category_id: int = None
):
    query = select(Book)
    if category_id:
        query = query.where(Book.category_id == category_id)
    if title:
        query = query.where(match(Book.title, against=title).in_natural_language_mode())
    if authors:
        query = query.where(match(Book.authors, against=authors).in_natural_language_mode())

    return [result[0] for result in db.execute(query).all()]
