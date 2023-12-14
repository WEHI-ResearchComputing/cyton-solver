import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api import api_router

# Initializes a FastAPI instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# =====================
#  Run server:
# =====================
if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=9999, reload=True)