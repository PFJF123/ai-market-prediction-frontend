import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests
from ..utils.config import THEME_PRIMARY_COLOR

def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def render_header():
    """Render the application header"""
    
    # Use columns for layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Load and display Lottie animation
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_qp1q7mct.json"  # Market/finance animation
        lottie_json = load_lottie_url(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, speed=1, height=120, key="header_animation")
        else:
            st.image("https://img.icons8.com/color/96/000000/stocks.png", width=80)
    
    with col2:
        st.title("AI Market Prediction")
        st.markdown(
            """
            <div style="margin-top: -20px;">
                <p style="font-size: 1.2rem; color: #666;">
                    Analyze financial news and predict market movements with AI
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Add a divider
    st.markdown(f"<hr style='height:2px;border:none;color:{THEME_PRIMARY_COLOR};background-color:{THEME_PRIMARY_COLOR};margin-bottom:20px;'/>", unsafe_allow_html=True)

def render_footer():
    """Render the application footer"""
    
    st.markdown(f"<hr style='height:1px;border:none;color:#ccc;background-color:#ccc;margin-top:30px;'/>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(
            """
            <div style="font-size: 0.8rem; color: #666;">
                <p>AI Market Prediction MVP | Powered by GPT-4o and XGBoost</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div style="font-size: 0.8rem; color: #666; text-align: right;">
                <p>© 2023</p>
            </div>
            """, 
            unsafe_allow_html=True
        ) 