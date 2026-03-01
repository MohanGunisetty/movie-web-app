from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base

# Tables are created via init_db.py instead of auto-creation here to prevent uWSGI fork deadlocks
app = FastAPI(title="Movie Streaming App")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files
# Serve static assets (css, js, images)
app.mount("/static", StaticFiles(directory="static"), name="static")
# Serve uploaded files (mostly for development, in prod use web server/CDN)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

from .routers import auth, users, categories, movies, streaming
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(movies.router)
app.include_router(streaming.router)

from fastapi.responses import RedirectResponse

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

