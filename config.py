# config.py
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
RADIO_POR_DEFECTO = 2000  # metros
MIN_CALIFICACION = 4.0
