from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cyton.api.api import api_router

# Initializes a FastAPI instance
app = FastAPI()

# CORS Middleware Config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initializes API Endpoints
app.include_router(api_router)
