import streamlit as st
import asyncio
from ..components.header import render_header
from ..utils.api import APIClient
from ..utils.config import THEME_PRIMARY_COLOR

async def load_recent_predictions():
    """Load recent predictions from API"""
    try:
        predictions = await APIClient.get_recent_predictions(limit=3)
        st.session_state.recent_predictions = predictions
    except Exception as e:
        st.error(f"Error loading recent predictions: {str(e)}")
        st.session_state.recent_predictions = []

def render_home_page():
    """Render the home page"""
    render_header()
    
    # Hero section
    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px 0 40px 0;">
            <h1 style="font-size: 2.5rem; margin-bottom: 10px;">AI-Powered Market Predictions</h1>
            <p style="font-size: 1.2rem; color: #666; margin-bottom: 30px;">
                Analyze real-time financial news and generate trade recommendations with AI
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Search box
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 40px;">
            <h2>Search Market Trends</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    search_query = st.text_input("Enter a market trend or topic", key="home_search")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Generate Prediction", key="home_search_button", use_container_width=True):
            if search_query:
                # Store the search query in session state and navigate to predictions page
                st.session_state.search_query = search_query
                st.session_state.page = "Predictions"
                st.experimental_rerun()
            else:
                st.warning("Please enter a search query")
    
    # Features section
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; margin: 30px 0;">
            <h2>How It Works</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px; border-radius: 5px; border: 1px solid #ddd;">
                <h3 style="color: {THEME_PRIMARY_COLOR};">1. News Analysis</h3>
                <p>We collect and analyze real-time financial and geopolitical news from multiple sources.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px; border-radius: 5px; border: 1px solid #ddd;">
                <h3 style="color: {THEME_PRIMARY_COLOR};">2. AI Processing</h3>
                <p>Our AI models (GPT-4o + XGBoost) analyze sentiment and predict market movements.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px; border-radius: 5px; border: 1px solid #ddd;">
                <h3 style="color: {THEME_PRIMARY_COLOR};">3. Trade Recommendations</h3>
                <p>Get actionable insights with sector predictions and specific trade ideas.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Recent predictions section
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; margin: 30px 0;">
            <h2>Recent Predictions</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load recent predictions if not already loaded
    if "recent_predictions" not in st.session_state:
        asyncio.run(load_recent_predictions())
    
    # Display recent predictions
    recent_predictions = st.session_state.get("recent_predictions", [])
    
    if not recent_predictions:
        st.info("No recent predictions available. Try generating a new prediction!")
    else:
        for prediction in recent_predictions:
            # Create a clickable card for each prediction
            with st.container():
                st.markdown(
                    f"""
                    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
                        <h3>{prediction.get('query', 'Unknown Query')}</h3>
                        <p style="color: #666;">
                            Created: {prediction.get('created_at', 'Unknown')} | 
                            Sectors: {len(prediction.get('sectors', []))} | 
                            Trade Ideas: {len(prediction.get('trade_ideas', []))}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Add a button to view the prediction
                if st.button(f"View Prediction", key=f"view_{prediction.get('id', 'unknown')}"):
                    # Store the prediction ID in session state and navigate to predictions page
                    st.session_state.prediction_id = prediction.get('id')
                    st.session_state.page = "Predictions"
                    st.experimental_rerun()
    
    # Call to action
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; margin: 30px 0;">
            <h2>Ready to Get Started?</h2>
            <p style="font-size: 1.2rem; color: #666; margin-bottom: 20px;">
                Generate your first market prediction now!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Go to Predictions", key="cta_button", use_container_width=True):
            st.session_state.page = "Predictions"
            st.experimental_rerun() 