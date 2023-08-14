from fastapi import FastAPI, Request
from auth_routers import auth_router
from book_routers import book_router
from fastapi_jwt_auth import AuthJWT
import schemas

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return schemas.Settings()


app.include_router(auth_router)
app.include_router(book_router)
