from pydantic import BaseModel
from typing import Optional


class Author(BaseModel):
    id: int
    name: str


class Genre(BaseModel):
    id: int
    title: str


class Book(BaseModel):
    id: int
    title: str
    description: Optional[str]
    author: Author
    genre: Optional[Genre]
    status: Optional[str] = "WISHING"

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "The Dark Tower",
                "author": "Stephen King",
            }
        }


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    is_authenticated: bool = True
