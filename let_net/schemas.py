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
    name: str
    email: str | None = None
    hashed_password: str

    class Config:
        from_attributes = True


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "d306a0d0774cb8f74d772e38c26213a6e707b709c33061a616ded3b7fc5ca922"
    )


class Login(BaseModel):
    name: str
    hashed_password: str
