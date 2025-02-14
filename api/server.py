from fastapi import FastAPI, Request, UploadFile, File, Depends, HTTPException, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, init_db, search_books
import os

origins = [
    "http://localhost:3000",
]

app = FastAPI()
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


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/books/search")
def search_endpoint(
    title: str = Query(None, description="Search term for book title"),
    author: str = Query(None, description="Search term for book author"),
    version: str = Query(None, description="Partial match for book version"),
    price: float = Query(None, description="Exact price match"),
    db: Session = Depends(get_db),
):
    books = search_books(db, title, author, version, price)

    if not books:
        raise HTTPException(status_code=404, detail="No books found")

    results = []
    for book in books:
        file_content = None
        if book.file and os.path.exists(book.file):
            with open(book.file, "r", encoding="utf-8") as f:
                file_content = f.read()

        results.append(
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "version": book.version,
                "price": float(book.price) if book.price is not None else None,
                "file": book.file,
                "file_content": file_content,
            }
        )

    return results


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
