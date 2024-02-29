from fastapi import APIRouter
from api.endpoints import root

# Create an APIRouter instance
api_router = APIRouter()

api_router.include_router(root.router, tags=["root"])