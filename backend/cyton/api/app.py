from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from cyton.api.endpoints.root import router
from fastapi.staticfiles import StaticFiles

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

@app.get("/")
async def index_redirect():
    return RedirectResponse(url='/index.html')

# Serve the API at /api
app.include_router(router, prefix="/api")

# Serve static files everywhere else
app.mount("/", StaticFiles(packages=[("cyton.api", "static")], html=True), name="static")
