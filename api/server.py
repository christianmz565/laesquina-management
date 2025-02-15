from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import (
    Book,
    Category,
    SessionLocal,
    create_category_orm,
    get_categories_orm,
    init_db,
    search_books_orm,
    create_book_orm,
    update_book_orm,
    get_book_orm,
    delete_book_orm,
)
import os
import env

origins = [
    "http://localhost:3000",
]

FILES_LOCATION = env.FILES_PATH


class BookBase(BaseModel):
    title: str
    author: str
    version: str
    price: float


class BookCreate(BookBase):
    file: str


class BookUpdate(BookBase):
    title: str = None
    author: str = None
    version: str = None
    price: float = None
    file: str = None


class BookPublic(BookBase):
    id: int
    file: bytes = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(FILES_LOCATION, exist_ok=True)
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/books/search", response_model=list[BookPublic])
def search_book(
    title: str = Query(None),
    author: str = Query(None),
    db: Session = Depends(get_db),
):
    books = search_books_orm(db, title, author)

    results = []
    for book in books:
        file_content = None
        if book.file and os.path.exists(book.file):
            with open(book.file, "r", encoding="utf-8") as f:
                file_content = f.read()

        results.append(
            BookPublic(
                id=book.id,
                title=book.title,
                author=book.author,
                version=book.version,
                price=float(book.price) if book.price is not None else None,
                file=file_content,
            )
        )

    return results


@app.post("/categories/create")
def create_category(
    name: str = Form(...),
    db: Session = Depends(get_db),
):
    new_category = create_category_orm(db, Category(name=name))
    return new_category


@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = get_categories_orm(db)
    return categories


@app.get("/books/{book_id}", response_model=BookPublic)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    book = get_book_orm(db, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    file_content = None
    if book.file and os.path.exists(book.file):
        with open(book.file, "r") as f:
            file_content = f.read()

    return BookPublic(
        id=book.id,
        title=book.title,
        author=book.author,
        version=book.version,
        price=float(book.price) if book.price is not None else None,
        file=file_content,
    )


@app.post("/books/{book_id}/update")
def update_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
):
    updated_data = book.model_dump(exclude_unset=True)
    updated_book = update_book_orm(db, book_id, updated_data)

    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return updated_book


@app.post("/books/{book_id}/delete")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    deleted_book = delete_book_orm(db, book_id)

    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return deleted_book


@app.post("/books/create")
def create_book(
    title: Annotated[str, Form()],
    author: Annotated[str, Form()],
    version: Annotated[str, Form()],
    price: Annotated[float, Form()],
    file: Annotated[UploadFile, File()],
    db: Session = Depends(get_db),
):
    ext = file.filename.split(".")[-1]
    full_path = os.path.join(FILES_LOCATION, f"{title}_{author}_{version}.{ext}")
    with open(full_path, "wb") as f:
        f.write(file.file.read())

    new_book = create_book_orm(
        db,
        Book(title=title, author=author, version=version, price=price, file=full_path),
    )

    return new_book


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
