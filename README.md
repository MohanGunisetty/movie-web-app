# Movie Streaming Platform

A detailed full-stack movie streaming application built with FastAPI and Vanilla JS.

## Features
- **Role-Based Access**: User and Admin roles with strict authorization.
- **Admin Panel**: Upload movies, manage users, and categories.
- **Video Streaming**: Secure, ranged-based video streaming.
- **Authentication**: JWT-based auth with password hashing.
- **UI**: Modern, dark-themed responsive interface.

## Quick Start (Local)

1. **Prerequisites**
   - Python 3.9+
   - PostgreSQL installed and running.

2. **Setup**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Create .env file (already created)
   # Check .env and update DATABASE_URL if needed
   ```

3. **Initialize Database**
   ```bash
   python init_db.py
   ```

4. **Run Application**
   ```bash
   uvicorn app.main:app --reload
   ```
   Or use the `run_app.bat` script.

5. **Access**
   - **Frontend**: http://localhost:8000/static/index.html
   - **API Docs**: http://localhost:8000/docs

## Default Credentials
- **Admin**: `admin@example.com` / `admin123`
- **User**: Register a new account

## Security Notes
- Change `SECRET_KEY` in `.env` for production.
- Update `MAX_FILE_SIZE_MB` as needed.
- In production, serving static files should be handled by Nginx/Apache.
