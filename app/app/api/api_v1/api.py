from fastapi import APIRouter

from app.api.api_v1.endpoints import accounts, clients, login  # utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
