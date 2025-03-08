import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to get settings from Streamlit secrets first, then fall back to environment variables
try:
    # API Settings from Streamlit secrets
    API_URL = st.secrets.get("api", {}).get("base_url", os.getenv("API_URL", "http://localhost:8000"))
    API_V1_PREFIX = st.secrets.get("api", {}).get("api_v1_prefix", os.getenv("API_V1_PREFIX", "/api/v1"))
    
    print(f"Using API URL from secrets: {API_URL}")
except Exception as e:
    # Fall back to environment variables if secrets are not available
    print(f"Secrets not available, using environment variables: {str(e)}")
    API_URL = os.getenv("API_URL", "http://localhost:8000")
    API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")

# Full API base URL
API_BASE_URL = f"{API_URL}{API_V1_PREFIX}"
print(f"API Base URL: {API_BASE_URL}")

# UI Settings
THEME_PRIMARY_COLOR = os.getenv("STREAMLIT_THEME_PRIMARY_COLOR", "#1E88E5")
THEME_BACKGROUND_COLOR = os.getenv("STREAMLIT_THEME_BACKGROUND_COLOR", "#FFFFFF")
THEME_TEXT_COLOR = os.getenv("STREAMLIT_THEME_TEXT_COLOR", "#262730")
THEME_FONT = os.getenv("STREAMLIT_THEME_FONT", "sans serif")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development") 