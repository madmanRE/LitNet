from fastapi import APIRouter, status, Depends
from database import SessionLocal, engine

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.get("/")
async def hellow():
    return {"message": "Hellow auth_routers"}