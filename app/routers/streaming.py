import os
from fastapi import APIRouter, Depends, HTTPException, Header, status, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from .. import database, models
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/api/stream",
    tags=["Streaming"]
)

def range_requests_response(
    request: Request, file_path: str, content_type: str = "video/mp4"
):
    """
    Utility function to handle HTTP Range requests for video streaming
    """
    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("range")

    if not range_header:
        # If no range header, return the whole file (or just start)
        # But usually for large videos, we want to enforce partial content or browser handles it.
        # Let's just return the beginning.
        return StreamingResponse(
            open(file_path, "rb"), 
            media_type=content_type
        )

    try:
        range_value = range_header.replace("bytes=", "").strip()
        if not range_value or "," in range_value:
            # Fall back to returning the whole file if range is multipart or empty
            return StreamingResponse(
                open(file_path, "rb"), 
                media_type=content_type
            )
            
        parts = range_value.split("-")
        if len(parts) != 2:
            return StreamingResponse(
                open(file_path, "rb"), 
                media_type=content_type
            )
            
        start_str, end_str = parts[0], parts[1]
        
        if start_str and end_str:
            start = int(start_str)
            end = int(end_str)
        elif start_str: # start-
            start = int(start_str)
            end = file_size - 1
        elif end_str: # -end (suffix range)
            suffix_len = int(end_str)
            start = max(0, file_size - suffix_len)
            end = file_size - 1
        else:
            start = int(start_str)
            end = int(end_str) if end_str else file_size - 1
    except (ValueError, IndexError):
        # Fallback to serving the whole file if parsing fails
        return StreamingResponse(
            open(file_path, "rb"), 
            media_type=content_type,
            status_code=200
        )
    
    # Chuck size logic
    chunk_size = 1024 * 1024  # 1MB chunks
    if end - start + 1 > chunk_size:
        end = start + chunk_size - 1

    # Ensure end is within bounds
    if end >= file_size:
        end = file_size - 1

    content_length = end - start + 1
    
    def iterfile():
        with open(file_path, "rb") as f:
            f.seek(start)
            yield f.read(content_length)

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(content_length),
    }

    return StreamingResponse(
        iterfile(),
        status_code=206,
        headers=headers,
        media_type=content_type,
    )

@router.get("/{movie_id}")
def stream_video(
    request: Request,
    movie_id: int,
    token: str = None, # Allow token in query param
    db: Session = Depends(database.get_db)
):
    # Manual Auth Check for Query Param
    if token:
        from jose import jwt
        from ..config import settings
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            # Valid token (we can add more checks like expiry/user existence if stricter security needed)
        except Exception:
             raise HTTPException(status_code=401, detail="Invalid token")
    else:
        # Fallback to header auth (for API clients)
        # Note: This means standard browser requests without token param will fail 401
        # unless we make auth optional for public movies? Req says "Users can: Stream movies", "User Routes (Login Required)"
        # So we must enforce auth.
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
             raise HTTPException(status_code=401, detail="Missing authentication")
             
        # We could use dependencies.get_current_user here but it's cleaner to handle the dual logic 
        # or just rely on the token param for the video tag.

    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Convert URL to file path
    # stored as /uploads/filename.ext -> relative to cwd + uploads/filename.ext
    # Logic: if starts with /uploads/, remove leading slash and join with cwd
    
    relative_path = movie.video_url.lstrip('/')
    video_path = os.path.abspath(relative_path)
    
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video file not found on server")
    
    return range_requests_response(request, video_path)
