import streamlit as st
import asyncio
import json
from ..components.header import render_header
from ..utils.api import APIClient
from ..utils.config import THEME_PRIMARY_COLOR, API_BASE_URL

async def load_recent_predictions():
    """Load recent predictions from API"""
    try:
        # Clear any previous errors
        if "prediction_load_error" in st.session_state:
            del st.session_state.prediction_load_error
            
        # Get recent predictions from API
        predictions = await APIClient.get_recent_predictions(limit=5)
        
        # Log the raw response for debugging
        print(f"Raw recent predictions response: {json.dumps(predictions, default=str)[:500]}...")
        
        # Handle error responses
        if isinstance(predictions, dict) and "error" in predictions:
            st.session_state.prediction_load_error = predictions.get("error", "Unknown error")
            st.session_state.recent_predictions = []
            print(f"Error loading predictions: {predictions.get('error')}")
            return
            
        # If we got an empty list or None, show a message about backend issues
        if not predictions:
            st.session_state.prediction_load_error = "The backend API returned no predictions. This may be due to a backend issue."
            st.session_state.recent_predictions = []
            print("No predictions returned from API")
            return
            
        # Handle different response formats
        if isinstance(predictions, dict):
            # Extract data from dictionary response
            if "data" in predictions:
                st.session_state.recent_predictions = predictions.get("data", [])
            elif "items" in predictions:
                st.session_state.recent_predictions = predictions.get("items", [])
            else:
                # Single prediction
                st.session_state.recent_predictions = [predictions]
        elif isinstance(predictions, list):
            # List of predictions
            st.session_state.recent_predictions = predictions
        else:
            # Unknown format
            st.session_state.prediction_load_error = "Unexpected response format"
            st.session_state.recent_predictions = []
            
        # Ensure we have a list
        if not isinstance(st.session_state.recent_predictions, list):
            st.session_state.recent_predictions = []
            
        # Log the processed predictions for debugging
        print(f"Processed recent predictions: {len(st.session_state.recent_predictions)} items")
        if st.session_state.recent_predictions:
            print(f"First prediction: {json.dumps(st.session_state.recent_predictions[0], default=str)[:500]}...")
    except Exception as e:
        st.session_state.prediction_load_error = str(e)
        st.session_state.recent_predictions = []
        print(f"Exception loading recent predictions: {str(e)}")

def render_home_page():
    """Render the home page"""
    render_header()
    
    # Check if API is connected
    if "api_connected" in st.session_state and not st.session_state.api_connected:
        st.warning("⚠️ Backend API is not connected")
        st.info(f"The application is currently unable to connect to the backend API at {API_BASE_URL}. Some features may not work properly.")
        st.markdown("""
        ### Troubleshooting Steps:
        1. Ensure the backend API is running
        2. Check that the API URL in the configuration is correct
        3. Verify network connectivity between the frontend and backend
        """)
        
        if st.button("Retry Connection", key="home_retry_connection"):
            asyncio.run(APIClient.health_check())
            st.experimental_rerun()
            
        st.markdown("---")
    
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
        button_disabled = "api_connected" in st.session_state and not st.session_state.api_connected
        if st.button("Generate Prediction", key="home_search_button", use_container_width=True, disabled=button_disabled):
            if search_query:
                # Store the search query in session state and navigate to predictions page
                st.session_state.search_query = search_query
                st.session_state.page = "Predictions"
                st.experimental_rerun()
            else:
                st.warning("Please enter a search query")
                
        if button_disabled:
            st.info("Prediction generation is disabled because the backend API is not connected")
    
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
    st.markdown("## Recent Market Predictions")
    
    # Check if we have an error loading predictions
    if "prediction_load_error" in st.session_state:
        st.error(f"Error loading predictions: {st.session_state.prediction_load_error}")
        if st.button("Retry Loading Predictions", key="retry_predictions"):
            asyncio.run(load_recent_predictions())
            st.experimental_rerun()
    
    # Get recent predictions from session state
    recent_predictions = st.session_state.get("recent_predictions", [])
    
    if not recent_predictions:
        st.info("No recent predictions available. Try generating a new prediction!")
    else:
        try:
            # Create a grid layout for predictions
            cols = st.columns(min(len(recent_predictions), 3))
            
            for i, prediction in enumerate(recent_predictions[:min(len(recent_predictions), 3)]):
                if not isinstance(prediction, dict):
                    continue
                    
                # Safely extract prediction data
                query = prediction.get('query', 'Unknown Query')
                created_at = prediction.get('created_at', 'Unknown')
                sectors = prediction.get('sectors_of_interest', prediction.get('sectors', []))
                trade_ideas = prediction.get('trade_ideas', [])
                prediction_id = prediction.get('id', 'unknown')
                market_sentiment = prediction.get('market_sentiment', 'neutral')
                
                # Determine sentiment color
                sentiment_color = "#FFA500"  # Default orange
                if market_sentiment and isinstance(market_sentiment, str):
                    market_sentiment = market_sentiment.lower()
                    if "bullish" in market_sentiment:
                        sentiment_color = "#4CAF50"  # Green
                    elif "bearish" in market_sentiment:
                        sentiment_color = "#F44336"  # Red
                    elif "neutral" in market_sentiment:
                        sentiment_color = "#FFA500"  # Orange
                
                # Create a card for each prediction
                with cols[i % 3]:
                    st.markdown(
                        f"""
                        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px; height: 200px; position: relative; overflow: hidden;">
                            <div style="position: absolute; top: 0; right: 0; width: 10px; height: 100%; background-color: {sentiment_color};"></div>
                            <h3 style="margin-top: 0;">{query[:50] + '...' if len(query) > 50 else query}</h3>
                            <p style="color: #666; font-size: 0.8em;">
                                Created: {created_at.split('T')[0] if 'T' in str(created_at) else created_at}
                            </p>
                            <p>
                                <span style="background-color: {sentiment_color}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;">
                                    {market_sentiment.title() if market_sentiment else 'Neutral'}
                                </span>
                            </p>
                            <p style="font-size: 0.9em;">
                                Sectors: {len(sectors)} | Trade Ideas: {len(trade_ideas)}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Add a button to view the prediction
                    if st.button(f"View Details", key=f"view_{prediction_id}"):
                        # Store the prediction ID in session state and navigate to predictions page
                        st.session_state.prediction_id = prediction_id
                        st.session_state.page = "Predictions"
                        st.experimental_rerun()
            
            # Add a "View All" button if there are more than 3 predictions
            if len(recent_predictions) > 3:
                st.markdown("<div style='text-align: center; margin-top: 10px;'>", unsafe_allow_html=True)
                if st.button("View All Predictions", key="view_all_predictions"):
                    st.session_state.page = "Predictions"
                    st.experimental_rerun()
                st.markdown("</div>", unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error displaying predictions: {str(e)}")
            st.info("Please try refreshing the page or generating a new prediction.")
    
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