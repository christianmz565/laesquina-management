from typing import Annotated, Optional
from fastapi import FastAPI, Depends, HTTPException, UploadFile, Form, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import (
    Book,
    Category,
    SessionLocal,
    create_category_orm,
    get_categories_orm,
    search_books_orm,
    create_book_orm,
    update_book_orm,
    get_book_orm,
    delete_book_orm,
)
import os
from .env import FILES_PATH


class BookBase(BaseModel):
    title: str
    author: str
    edition: str
    price: float
    category_id: int


class BookCreate(BookBase):
    file: str


class BookUpdate(BookBase):
    title: str = None
    author: str = None
    edition: str = None
    price: float = None
    file: str = None


class BookPublic(BookBase):
    id: int


class CategoryBase(BaseModel):
    name: str


class CategoryPublic(CategoryBase):
    id: int


api_app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@api_app.post("/categories/create", response_model=CategoryPublic)
def create_category(
    name: str = Form(),
    db: Session = Depends(get_db),
):
    new_category = create_category_orm(db, Category(name=name))
    return new_category


@api_app.get("/categories", response_model=list[CategoryPublic])
def get_categories(db: Session = Depends(get_db)):
    return get_categories_orm(db)


@api_app.post("/books/search", response_model=list[BookPublic])
def search_book(
    query: Annotated[str, Form()],
    db: Session = Depends(get_db),
):
    return search_books_orm(db, query, query, add_or=True)


@api_app.post("/books/complete-search", response_model=list[BookPublic])
def search_book_complete(
    title: Annotated[Optional[str], Form()] = None,
    author: Annotated[Optional[str], Form()] = None,
    db: Session = Depends(get_db),
):
    return search_books_orm(db, title, author)


@api_app.get("/books/{book_id}/download")
def download_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    book = get_book_orm(db, book_id)
    print(book)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return FileResponse(book.file, media_type="application/pdf")


@api_app.get("/books/{book_id}", response_model=BookPublic)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    book = get_book_orm(db, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@api_app.put("/books/{book_id}", response_model=BookPublic)
def update_book(
    book_id: int,
    title: Annotated[Optional[str], Form()] = None,
    author: Annotated[Optional[str], Form()] = None,
    edition: Annotated[Optional[str], Form()] = None,
    price: Annotated[Optional[float], Form()] = None,
    category_id: Annotated[Optional[int], Form()] = None,
    file: Annotated[Optional[UploadFile], File()] = None,
    db: Session = Depends(get_db),
):
    book = get_book_orm(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    updated_data = {}
    if title:
        title = title.replace(" ", "-").lower().strip()
        updated_data["title"] = title
    if author:
        author = author.replace(" ", "-").lower().strip()
        updated_data["author"] = author
    if edition:
        updated_data["edition"] = edition
    if price:
        updated_data["price"] = price
    if category_id:
        updated_data["category_id"] = category_id

    ext = file.filename.split(".")[-1] if file else book.file.split(".")[-1]
    b_title = title if title else book.title
    b_author = author if author else book.author
    b_edition = edition if edition else book.edition
    full_path = os.path.join(FILES_PATH, f"{b_title}_{b_author}_{b_edition}.{ext}")
    if file:
        os.remove(book.file)
        with open(full_path, "wb") as f:
            f.write(file.file.read())
    else:
        os.rename(book.file, full_path)
    updated_data["file"] = full_path

    updated_book = update_book_orm(db, book, updated_data)

    return updated_book


@api_app.post("/books/create", response_model=BookPublic)
def create_book(
    title: Annotated[str, Form()],
    author: Annotated[str, Form()],
    edition: Annotated[str, Form()],
    price: Annotated[float, Form()],
    category_id: Annotated[int, Form()],
    file: Annotated[UploadFile, File()],
    db: Session = Depends(get_db),
):
    ext = file.filename.split(".")[-1]
    title = title.replace(" ", "-").lower().strip()
    author = author.replace(" ", "-").lower().strip()
    full_path = os.path.join(FILES_PATH, f"{title}_{author}_{edition}.{ext}")
    with open(full_path, "wb") as f:
        f.write(file.file.read())

    new_book = create_book_orm(
        db,
        Book(
            title=title,
            author=author,
            edition=edition,
            price=price,
            category_id=category_id,
            file=full_path,
        ),
    )

    return new_book


@api_app.delete("/books/{book_id}", response_model=BookPublic)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    deleted_book = delete_book_orm(db, book_id)
    os.remove(deleted_book.file)

    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return deleted_book
