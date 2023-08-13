from fastapi import FastAPI
from auth_routers import auth_router
from book_routers import book_router


app = FastAPI()


app.include_router(auth_router)
app.include_router(book_router)
