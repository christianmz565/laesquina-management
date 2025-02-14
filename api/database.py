from sqlalchemy import create_engine, Column, Integer, String, Numeric, Index, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import env

DATABASE_URL = env.DATABASE_URL

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


def get_book(db: Session, book_id: int):
    return db.execute(select(Book).where(Book.id == book_id)).first()


def create_book_orm(db: Session, book: Book):
    db.add(book)
    db.commit()
    db.refresh(book)


def update_book_orm(db: Session, book_id: int, updated_data: dict):
    book = get_book(db, book_id)
    if book:
        for key, value in updated_data.items():
            setattr(book, key, value)
        db.commit()
        db.refresh(book)
    return book


def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if book:
        db.delete(book)
        db.commit()
    return book


def search_books_orm(db: Session, title: str = None, author: str = None):
    query = select(Book)

    if title:
        query = query.where(Book.title.match(f"+{title}*", boolean=True))
    if author:
        query = query.where(Book.author.match(f"+{author}*", boolean=True))

    return db.execute(query).all()
