from fastapi import APIRouter
from cyton.api.endpoints import root

# Create an APIRouter instance
api_router = APIRouter(
)

api_router.include_router(root.router, prefix="/api", tags=["root"])
