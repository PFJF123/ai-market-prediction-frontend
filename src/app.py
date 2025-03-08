import streamlit as st
import asyncio
from components.sidebar import render_sidebar
from components.header import render_footer
from pages.home import render_home_page
from pages.news import render_news_page
from pages.predictions import render_predictions_page
from pages.about import render_about_page
from utils.api import APIClient
from utils.config import THEME_PRIMARY_COLOR

# Configure the page
st.set_page_config(
    page_title="AI Market Prediction",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        max-width: 1200px;
        margin: 0 auto;
    }}
    .stButton>button {{
        background-color: {THEME_PRIMARY_COLOR};
        color: white;
    }}
    .stProgress .st-bo {{
        background-color: {THEME_PRIMARY_COLOR};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Home"

async def check_api_health():
    """Check the health of the API"""
    try:
        health = await APIClient.health_check()
        st.session_state.api_health = health
    except Exception as e:
        st.session_state.api_health = {"status": "unhealthy", "error": str(e)}

def main():
    """Main application entry point"""
    # Check API health
    asyncio.run(check_api_health())
    
    # Render sidebar
    render_sidebar()
    
    # Render the selected page
    if st.session_state.page == "Home":
        render_home_page()
    elif st.session_state.page == "News":
        render_news_page()
    elif st.session_state.page == "Predictions":
        render_predictions_page()
    elif st.session_state.page == "About":
        render_about_page()
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main() 