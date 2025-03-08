import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Settings
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")

# Full API base URL
API_BASE_URL = f"{API_URL}{API_V1_PREFIX}"

# UI Settings
THEME_PRIMARY_COLOR = os.getenv("STREAMLIT_THEME_PRIMARY_COLOR", "#1E88E5")
THEME_BACKGROUND_COLOR = os.getenv("STREAMLIT_THEME_BACKGROUND_COLOR", "#FFFFFF")
THEME_TEXT_COLOR = os.getenv("STREAMLIT_THEME_TEXT_COLOR", "#262730")
THEME_FONT = os.getenv("STREAMLIT_THEME_FONT", "sans serif")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development") 