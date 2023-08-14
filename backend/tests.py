from main import app
from fastapi import status, Depends, HTTPException, Request
import models, schemas
from fastapi.testclient import TestClient
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
import pydantic
from fastapi.encoders import jsonable_encoder

session = SessionLocal(bind=engine)

client = TestClient(app)


# Auth tests


def test_signup_ok():
    user_data = {
        "name": "Rengar",
        "email": "rengar@mail.com",
        "hashed_password": "rengar",
    }
    response = client.post("/auth/signup/", json=user_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "message": f"New user {user_data['name']} has been created successfully"
    }


def test_signup_mistake():
    user_data = {
        "name": "John",
        "email": "john@mail.com",
        "hashed_password": "john",
    }
    response = client.post("/auth/signup/", json=user_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "User with the email already exists"}


def test_login_successful_ok():
    login_data = {"name": "Rengar", "hashed_password": "rengar"}

    response = client.post("/auth/login/", json=login_data)

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.json()
    assert "refresh" in response.json()


def test_login_successful_mistake():
    login_data = {"name": "Reggar", "hashed_password": "rengar"}

    response = client.post("/auth/login/", json=login_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}


def test_login_successful_mistake2():
    login_data = {"name": "Rengar", "hashed_password": "reggar"}

    response = client.post("/auth/login/", json=login_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}


# Book tests


def test_get_all_books_ok():
    user = session.query(models.User).filter(models.User.name == "Rengar").first()
    book_data = [
        {"title": "Book 1", "owner_id": user.id},
        {"title": "Book 2", "owner_id": user.id},
        {"title": "Book 3", "owner_id": user.id},
    ]
    for book in book_data:
        session.add(models.Book(**book))
    session.commit()

    authorize = AuthJWT()
    access_token = authorize.create_access_token(subject=user.name)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/books/", headers=headers)

    try:
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == len(book_data)
        for book in response.json():
            assert "title" in book
    except pydantic.error_wrappers.ValidationError as validation_error:
        print("Validation errors:", validation_error.errors_json())


def test_get_all_books_mistake():
    response = client.get("/books/")

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid Token"}


# //TODO: функции test_get_book_by_title и test_add_book отрабатывают некорректно. Нужно разобраться.
def test_get_book_by_title():
    user = session.query(models.User).filter(models.User.name == "Rengar").first()

    book_title = "Book 3"

    authorize = AuthJWT()
    access_token = authorize.create_access_token(subject=user.name)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"/books/{book_title}/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == jsonable_encoder(response)


def test_add_book():
    user = session.query(models.User).filter(models.User.name == "Rengar").first()

    book = {
        "title": "Book 4",
        "owner_id": user.id,
    }

    authorize = AuthJWT()
    access_token = authorize.create_access_token(subject=user.name)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/books/add/", json=book, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "The book has been added successfully"}


def test_delete_book():
    user = session.query(models.User).filter(models.User.name == "Rengar").first()

    book_title = "Book 1"

    authorize = AuthJWT()
    access_token = authorize.create_access_token(subject=user.name)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete(f"/books/delete/?book_title=Book 1", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Book 'Book 1' has been deleted"}

    deleted_book = (
        session.query(models.Book).filter(models.Book.title == "Book 1").first()
    )
    assert deleted_book is None
