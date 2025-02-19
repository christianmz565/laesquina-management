from typing import Annotated, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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


@app.post("/categories/create", response_model=CategoryPublic)
def create_category(
    name: str = Form(),
    db: Session = Depends(get_db),
):
    new_category = create_category_orm(db, Category(name=name))
    return new_category


@app.get("/categories", response_model=list[CategoryPublic])
def get_categories(db: Session = Depends(get_db)):
    return get_categories_orm(db)


@app.post("/books/search", response_model=list[BookPublic])
def search_book(
    query: Annotated[str, Form()],
    db: Session = Depends(get_db),
):
    return search_books_orm(db, query, query, add_or=True)


@app.post("/books/complete-search", response_model=list[BookPublic])
def search_book_complete(
    title: Annotated[Optional[str], Form()] = None,
    author: Annotated[Optional[str], Form()] = None,
    db: Session = Depends(get_db),
):
    return search_books_orm(db, title, author)


@app.post("/books/{book_id}/download")
def download_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    book = get_book_orm(db, book_id)
    print(book)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return FileResponse(book.file, media_type="application/pdf")


@app.get("/books/{book_id}", response_model=BookPublic)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    book = get_book_orm(db, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book

@app.post("/books/{book_id}/update", response_model=BookPublic)
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
        title = title.replace(" ", "-")
        updated_data["title"] = title
    if author:
        author = author.replace(" ", "-")
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
    full_path = os.path.join(FILES_LOCATION, f"{b_title}_{b_author}_{b_edition}.{ext}")
    if file:
        os.remove(book.file)
        with open(full_path, "wb") as f:
            f.write(file.file.read())
    else:
        os.rename(book.file, full_path)
    updated_data["file"] = full_path

    updated_book = update_book_orm(db, book, updated_data)

    return updated_book




@app.post("/books/create", response_model=BookPublic)
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
    title = title.replace(" ", "-")
    author = author.replace(" ", "-")
    full_path = os.path.join(FILES_LOCATION, f"{title}_{author}_{edition}.{ext}")
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

@app.post("/books/{book_id}/delete", response_model=BookPublic)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    deleted_book = delete_book_orm(db, book_id)
    os.remove(deleted_book.file)

    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return deleted_book

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
