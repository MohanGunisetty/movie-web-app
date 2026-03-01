# PythonAnywhere WSGI Configuration File
# Place this file path in PythonAnywhere's WSGI config field:
# /var/www/<yourusername>_pythonanywhere_com_wsgi.py
#
# Or configure PythonAnywhere to point to this file.

import sys
import os

# Add your project directory to sys.path
# Replace <yourusername> with your actual PythonAnywhere username
project_home = '/home/<yourusername>/movie'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import the FastAPI app and wrap with ASGI middleware
from app.main import app as application

# PythonAnywhere uses WSGI, so we need to wrap the ASGI app
from asgiref.wsgi import WsgiToAsgi

# Note: For PythonAnywhere free tier, use the WSGI wrapper
# If you have a paid plan with ASGI support, you can use the app directly
application = application
