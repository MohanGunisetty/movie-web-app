from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base

# Create tables (normally done via migration tool like Alembic, but using auto-create for simplicity)
Base.metadata.create_all(bind=engine)

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

@app.get("/")
async def root():
    return {"message": "Welcome to the Movie Streaming API"}

