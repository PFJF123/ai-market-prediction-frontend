import os
import sys
import streamlit as st

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# Set page config
st.set_page_config(
    page_title="AI Market Prediction",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stButton button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Import components
from src.components.sidebar import render_sidebar

# Import pages
from src.pages.home import render_home_page
from src.pages.news import render_news_page
from src.pages.predictions import render_predictions_page
from src.pages.about import render_about_page

# Initialize session state for current page if not exists
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Check if model_insights and recommendations modules exist
try:
    from src.pages.model_insights import render_model_insights_page
    has_model_insights = True
except ImportError:
    has_model_insights = False

try:
    from src.pages.recommendations import render_recommendations_page
    has_recommendations = True
except ImportError:
    has_recommendations = False

def main():
    """Main function to render the application"""
    
    # Render sidebar
    render_sidebar()
    
    # Render the selected page
    if st.session_state.page == "Home":
        render_home_page()
    elif st.session_state.page == "News":
        render_news_page()
    elif st.session_state.page == "Predictions":
        render_predictions_page()
    elif st.session_state.page == "Recommendations" and has_recommendations:
        render_recommendations_page()
    elif st.session_state.page == "Model Insights" and has_model_insights:
        render_model_insights_page()
    elif st.session_state.page == "About":
        render_about_page()
    else:
        st.session_state.page = "Home"
        render_home_page()

if __name__ == "__main__":
    main() 