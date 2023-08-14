from fastapi import APIRouter, status, Depends, HTTPException
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models, schemas
from itertools import chain
from typing import List
from fastapi_jwt_auth import AuthJWT

book_router = APIRouter(
    prefix="/books",
    tags=["Book"],
)

session = SessionLocal(bind=engine)


@book_router.get("/")
async def get_all_books(
    Authorize: AuthJWT = Depends(), skip: int = 0, limit: int = 10
) -> List[schemas.BookOut]:
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
    current_user = Authorize.get_jwt_subject()

    user = session.query(models.User).filter(models.User.name == current_user).first()

    return (
        session.query(models.Book)
        .filter(models.Book.owner_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@book_router.get("/{book_title}/")
async def get_book_by_title(title: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
    current_user = Authorize.get_jwt_subject()

    user = (
        session.query(models.User).models.User(models.User.name == current_user).first()
    )

    book = (
        session.query(models.Book)
        .filter(models.Book.title == title)
        .filter(models.Book.owner_id == user.id)
        .first()
    )
    if book:
        return book
    else:
        return {"message": "There are no book with same title in your collection"}


@book_router.post("/add/")
async def add_book(book: schemas.Book, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
    current_user = Authorize.get_jwt_subject()

    user = (
        session.query(models.User).models.User(models.User.name == current_user).first()
    )

    new_book = models.Book(**book.dict())
    new_book.owner_id = user.id
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book


@book_router.patch("/update/{book_title}")
async def change_book(
    book_title: str, updated_book: schemas.Book, Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
    current_user = Authorize.get_jwt_subject()

    user = (
        session.query(models.User).models.User(models.User.name == current_user).first()
    )

    book = (
        session.query(models.Book)
        .filter(models.Book.title == book_title)
        .filter(models.Book.owner_id == user.id)
        .first()
    )
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in updated_book.dict().items():
        setattr(book, key, value)
    session.commit()
    return {"message": "Book updated successfully"}


@book_router.delete("/delete/")
async def delete_book(
    book_id: int = None, book_title: str = None, Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
    current_user = Authorize.get_jwt_subject()

    user = (
        session.query(models.User).models.User(models.User.name == current_user).first()
    )

    book = None
    if book_id:
        book = (
            session.query(models.Book)
            .filter(models.Book.id == book_id)
            .filter(models.Book.owner_id == user.id)
            .first()
        )
    elif book_title:
        book = (
            session.query(models.Book)
            .filter(models.Book.title == book_title)
            .filter(models.Book.owner_id == user.id)
            .first()
        )
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"message": f"Book '{book.title}' has been deleted"}
