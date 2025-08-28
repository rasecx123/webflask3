import os
from dotenv import load_dotenv

load_dotenv() #cargar .env en desarrollo

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "clave_dev_segura")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'