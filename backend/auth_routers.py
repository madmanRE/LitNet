from fastapi import APIRouter, status, Depends, HTTPException, Request
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models, schemas
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

session = SessionLocal(bind=engine)


@auth_router.post(
    "/signup/", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
async def signup(user: schemas.User):
    db_email = (
        session.query(models.User).filter(models.User.email == user.email).first()
    )

    if db_email is not None:
        raise HTTPException(
            status_code=400, detail="User with the email already exists"
        )

    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=generate_password_hash(user.hashed_password),
    )

    session.add(new_user)
    session.commit()

    return new_user


# login route


@auth_router.post("/login/")
async def login(user: schemas.Login, Authorize: AuthJWT = Depends()):
    db_user = session.query(models.User).filter(models.User.name == user.name).first()

    if db_user and check_password_hash(db_user.hashed_password, user.hashed_password):
        access_token = Authorize.create_access_token(subject=db_user.name)
        refresh_token = Authorize.create_refresh_token(subject=db_user.name)

        response = {"access": access_token, "refresh": refresh_token}

        return jsonable_encoder(response)

    raise HTTPException(status_code=400, detail="Invalid username or password")


# refreshing tokens


@auth_router.get("/refresh/")
async def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

    except Exception as e:
        raise HTTPException(
            status_code=401, detail="Please provide a valid refresh token"
        )

    current_user = Authorize.get_jwt_subject()

    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access": access_token})
