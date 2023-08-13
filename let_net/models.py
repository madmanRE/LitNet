from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_authenticated = Column(Boolean, default=False)

    def __repr__(self):
        return f"User: {self.name}"


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"Author: {self.name}"


class Book(Base):
    __tablename__ = "books"

    BOOK_STATUS = (
        ("WISHING", "wishing"),
        ("IN_COLLECTION", "in_collection"),
        ("HAS_READ", "has_read"),
    )

    GENRE = (
        ("FANTASY", "fantasy"),
        ("SCI_FI", "sci_fi"),
        ("MYSTERY", "mystery"),
        ("THRILLER", "thriller"),
        ("ROMANCE", "romance"),
        ("WESTERNS", "westerns"),
        ("TECHNICAL_LITERATURE", "technical_literature"),
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
    owner_id = Column(Integer, ForeignKey("users.id"))
    genre = Column(ChoiceType(choices=GENRE), default="FANTASY")
    status = Column(ChoiceType(choices=BOOK_STATUS), default="WISHING")

    def __repr__(self):
        return f"BooK: {self.title}"
