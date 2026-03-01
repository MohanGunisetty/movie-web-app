import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
    
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 500))
    ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS", "mp4,mkv,avi").split(","))

settings = Settings()
