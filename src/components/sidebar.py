import streamlit as st
from streamlit_option_menu import option_menu
from ..utils.config import THEME_PRIMARY_COLOR, API_BASE_URL
import asyncio
from ..utils.api import APIClient

async def check_api_health():
    """Check the health of the API and update session state"""
    if "api_health_checking" not in st.session_state or not st.session_state.api_health_checking:
        st.session_state.api_health_checking = True
        health_response = await APIClient.health_check()
        st.session_state.api_health = health_response
        st.session_state.api_health_checking = False

def render_sidebar():
    """Render the application sidebar"""
    
    # Run API health check asynchronously
    if "api_health" not in st.session_state:
        st.session_state.api_health = {"status": "unknown"}
        asyncio.run(check_api_health())
    
    with st.sidebar:
        # App logo/title
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: {THEME_PRIMARY_COLOR};">AI Market</h1>
                <p style="margin-top: -15px; font-size: 1.2rem;">Prediction</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Navigation menu
        selected = option_menu(
            menu_title=None,
            options=["Home", "News", "Predictions", "About"],
            icons=["house", "newspaper", "graph-up", "info-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": THEME_PRIMARY_COLOR, "font-size": "14px"}, 
                "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": THEME_PRIMARY_COLOR},
            }
        )
        
        # Store the selected page in session state
        st.session_state.page = selected
        
        # Divider
        st.markdown("<hr/>", unsafe_allow_html=True)
        
        # API Status indicator
        st.markdown("### Backend Connection")
        
        if "api_connected" in st.session_state and st.session_state.api_connected:
            st.success(f"API: Connected to {API_BASE_URL}")
        else:
            st.error(f"API: Disconnected from {API_BASE_URL}")
            st.info("Please ensure the backend API is running and accessible.")
            if st.button("Retry Connection"):
                asyncio.run(check_api_health())
                st.experimental_rerun()
        
        # Additional sidebar content
        st.markdown("<hr/>", unsafe_allow_html=True)
        
        # Quick search
        st.subheader("Quick Search")
        quick_search = st.text_input("Search market trends", key="sidebar_search")
        if st.button("Search", key="sidebar_search_button"):
            # Store the search query in session state and navigate to predictions page
            st.session_state.search_query = quick_search
            st.session_state.page = "Predictions"
            st.experimental_rerun()
        
        # Predefined market trends
        st.markdown("### Trending Topics")
        trends = [
            "AI chip demand",
            "Federal Reserve interest rates",
            "Renewable energy investments",
            "Cybersecurity threats",
            "Healthcare innovation"
        ]
        
        for trend in trends:
            if st.button(trend, key=f"trend_{trend}"):
                # Store the trend in session state and navigate to predictions page
                st.session_state.search_query = trend
                st.session_state.page = "Predictions"
                st.experimental_rerun()
        
        # Footer
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size: 0.8rem; color: #666; text-align: center;">
                <p>Powered by GPT-4o & XGBoost</p>
            </div>
            """, 
            unsafe_allow_html=True
        ) 