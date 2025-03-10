from fastapi import FastAPI
from routes import router  # Import the router containing all API endpoints
from dotenv import load_dotenv
import os

# Load environment variables from a .env file (if applicable)
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Include the router to register all API routes defined in router.py
app.include_router(router)  # This ensures all API endpoints are accessible