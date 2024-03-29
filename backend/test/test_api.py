from fastapi import APIRouter

from cyton.api.api import router
from cyton.api.app import app

def test_routes():
    """
    Tests that the API backend runs without errors
    """
    api_router = APIRouter()
    api_router.include_router(router, tags=["root"])

def test_openapi():
    app.openapi()
