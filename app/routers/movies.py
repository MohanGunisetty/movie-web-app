import shutil
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import database, models, schemas
from ..dependencies import get_current_user, require_admin
from ..config import settings

router = APIRouter(
    prefix="/api",
    tags=["Movies"]
)

def save_upload_file(upload_file: UploadFile) -> str:
    filename = str(uuid.uuid4()) + "_" + upload_file.filename
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    # Return relative path for URL construction
    return f"/uploads/{filename}"

@router.get("/movies", response_model=List[schemas.MovieResponse])
def get_movies(
    category_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Movie)
    if category_id:
        query = query.filter(models.Movie.category_id == category_id)
    return query.offset(skip).limit(limit).all()

@router.get("/movies/{movie_id}", response_model=schemas.MovieResponse)
def get_movie(
    movie_id: int, 
    current_user: models.User = Depends(get_current_user), # Require login to view details
    db: Session = Depends(database.get_db)
):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/admin/movies", response_model=schemas.MovieResponse)
def create_movie(
    title: str = Form(...),
    description: str = Form(None),
    category_id: int = Form(...),
    video_file: UploadFile = File(...),
    thumbnail_file: Optional[UploadFile] = File(None),
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(database.get_db)
):
    # Validate video extension
    ext = video_file.filename.split('.')[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file format. Allowed: {settings.ALLOWED_EXTENSIONS}")
    
    # Save video
    video_url = save_upload_file(video_file)
    
    # Save thumbnail if provided
    thumbnail_url = None
    if thumbnail_file:
        thumbnail_url = save_upload_file(thumbnail_file)
    
    new_movie = models.Movie(
        title=title,
        description=description,
        category_id=category_id,
        video_url=video_url,
        thumbnail_url=thumbnail_url,
        uploaded_by=current_user.id
    )
    
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

@router.delete("/admin/movies/{movie_id}")
def delete_movie(
    movie_id: int,
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(database.get_db)
):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Delete files from disk
    # Note: In production, consider if you want to keep files or soft delete
    try:
        if movie.video_url:
            video_path = os.path.join(os.getcwd(), movie.video_url.lstrip('/'))
            if os.path.exists(video_path):
                os.remove(video_path)
        
        if movie.thumbnail_url:
            thumb_path = os.path.join(os.getcwd(), movie.thumbnail_url.lstrip('/'))
            if os.path.exists(thumb_path):
                os.remove(thumb_path)
    except Exception as e:
        print(f"Error deleting files: {e}")

    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted successfully"}
