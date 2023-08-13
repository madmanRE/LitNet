from fastapi import APIRouter, status, Depends, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
import models, schemas
from itertools import chain
from typing import List

book_router = APIRouter(
    prefix="/books",
    tags=["Book"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@book_router.get("/")
async def get_all_books(
        skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[schemas.BookOut]:
    return db.query(models.Book).offset(skip).limit(limit).all()


@book_router.get("/{book_title}/")
async def get_book_by_title(title: str, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.title == title).first()
    if book:
        return book
    else:
        return {"message": "There are no book with same title in your collection"}


@book_router.get("/like/{book_title}/")
async def get_similar_books(
        book_title: str, db: Session = Depends(get_db)
) -> List[schemas.BookOut]:
    book = db.query(models.Book).filter(models.Book.title == book_title).first()
    if book:
        result_books_by_genre = (
            db.query(models.Book)
            .filter(models.Book.genre == book.genre)
            .filter(models.Book.id != book.id)
            .limit(10)
            .all()
        )
        result_books_by_author = (
            db.query(models.Book)
            .filter(models.Book.author_id == book.author_id)
            .filter(models.Book.id != book.id)
            .limit(10)
            .all()
        )
        result_books = set(result_books_by_genre + result_books_by_author)
        if result_books:
            return result_books
        else:
            return {"message": "There are no similar books like that!"}
    else:
        return {"message": "Book not found!"}


@book_router.post("/add/")
async def add_book(book: schemas.Book, db: Session = Depends(get_db)):
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@book_router.patch("/update/{book_title}")
async def change_book(book_title: str, updated_book: schemas.Book, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.title == book_title).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in updated_book.dict().items():
        setattr(book, key, value)
    db.commit()
    return {"message": "Book updated successfully"}


@book_router.delete("/delete/")
async def delete_book(db: Session = Depends(get_db), book_id: int = None, book_title: str = None):
    book = None
    if book_id:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
    elif book_title:
        book = db.query(models.Book).filter(models.Book.title == book_title).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": f"Book '{book.title}' has been deleted"}
