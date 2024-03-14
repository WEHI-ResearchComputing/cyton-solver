from fastapi import APIRouter

from cyton.api.endpoints import root

def test_api():
    """
    Tests that the API backend runs without errors
    """
    api_router = APIRouter()
    api_router.include_router(root.router, tags=["root"])
