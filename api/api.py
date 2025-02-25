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
from .env import FILES_PATH, PC_NAME


class BookPublic(BaseModel):
    id: int
    title: str
    price: float | None
    category_id: int


class CategoryPublic(BaseModel):
    id: int
    name: str


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
    title: Annotated[Optional[str], Form()] = None,
    category_id: Annotated[Optional[int], Form()] = None,
    db: Session = Depends(get_db),
):
    return search_books_orm(db, title, category_id)


@api_app.get("/books/{book_id}/download")
def download_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    book = get_book_orm(db, book_id)
    print(book)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book.file.replace("/app", f"file://///{PC_NAME}")


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
    price: Annotated[Optional[float], Form()] = None,
    category_id: Annotated[Optional[int], Form()] = None,
    file: Annotated[Optional[UploadFile], File()] = None,
    db: Session = Depends(get_db),
):
    book = get_book_orm(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    updated_data = {}
    if price:
        updated_data["price"] = price
    if title:
        updated_data["title"] = title
    if category_id:
        updated_data["category_id"] = category_id
    if file:
        os.remove(book.file)
        with open(book.file, "wb") as f:
            f.write(file.file.read())

    updated_book = update_book_orm(db, book, updated_data)

    return updated_book


@api_app.post("/books/create", response_model=BookPublic)
def create_book(
    file: Annotated[UploadFile, File()],
    title: Annotated[Optional[str], Form()],
    category_id: Annotated[Optional[int], Form()],
    price: Annotated[Optional[float], Form()] = None,
    db: Session = Depends(get_db),
):
    book_inst = Book(title=title, category_id=category_id)
    if price:
        book_inst.price = price

    new_book = create_book_orm(
        db,
        book_inst,
    )
    book_id = new_book.id
    ext = file.filename.split(".")[-1]
    full_path = os.path.join(FILES_PATH, str(book_id) + "." + ext)
    with open(full_path, "wb") as f:
        f.write(file.file.read())

    new_book.file = full_path
    db.commit()
    db.refresh(new_book)

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
