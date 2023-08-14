from database import engine, Base
from models import User, Author, Book

Base.metadata.create_all(bind=engine)
