from pydantic import BaseModel
from typing import Optional


class Author(BaseModel):
    id: int
    name: str


class Book(BaseModel):
    title: str
    description: Optional[str] = ""
    author_id: int
    owner_id: Optional[int]
    genre: Optional[str] = "FANTASY"
    status: Optional[str] = "WISHING"

    class Config:
        from_attributes = True


class BookOut(BaseModel):
    id: int
    title: str
    author_id: int

    class Config:
        from_attributes = True


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
