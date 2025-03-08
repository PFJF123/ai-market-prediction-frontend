import streamlit as st
import asyncio
import time
import json
from ..components.header import render_header
from ..components.prediction_card import render_prediction
from ..utils.api import APIClient
from ..utils.config import API_BASE_URL

async def generate_prediction(query, time_frame="medium_term", sectors_of_interest=None, max_trade_ideas=5):
    """Generate a market prediction"""
    try:
        with st.spinner(f"Generating prediction for '{query}'..."):
            # Log the request for debugging
            print(f"Generating prediction for query: '{query}', time_frame: {time_frame}, sectors: {sectors_of_interest}, max_trade_ideas: {max_trade_ideas}")
            
            # Make the API request
            response = await APIClient.generate_prediction(
                query=query,
                time_frame=time_frame,
                sectors_of_interest=sectors_of_interest,
                max_trade_ideas=max_trade_ideas
            )
            
            # Log the response for debugging
            print(f"Generate prediction response type: {type(response)}")
            if response:
                print(f"Generate prediction response: {json.dumps(response, default=str)[:500]}...")
            
            # Handle error responses
            if isinstance(response, dict) and "error" in response:
                error_msg = response["error"]
                st.error(f"Error generating prediction: {error_msg}")
                
                # If it's a connection error, provide troubleshooting steps
                if "connection_error" in response:
                    st.info("""
                    Unable to connect to the API. Please check:
                    1. The backend API is running
                    2. Your network connection is working
                    3. The API URL in the configuration is correct
                    """)
                # If it's a backend error, show a more specific message
                else:
                    st.warning("""
                    The backend API returned an error. This may be due to:
                    1. A temporary issue with the backend service
                    2. A configuration issue with the OpenAI service
                    3. A database connection problem
                    
                    Please try again later or contact the administrator.
                    """)
                return None
            
            # Extract the prediction from the response
            prediction = None
            processing_time = 0
            
            if isinstance(response, dict):
                prediction = response.get("prediction", response)
                processing_time = response.get("processing_time", 0)
            else:
                prediction = response
            
            if prediction:
                st.success(f"Prediction generated in {processing_time:.2f} seconds")
            else:
                st.warning("No prediction data returned from the API")
            
            return prediction
    except Exception as e:
        st.error(f"Error generating prediction: {str(e)}")
        return None

async def get_prediction(prediction_id):
    """Get a specific prediction by ID"""
    try:
        with st.spinner("Loading prediction..."):
            # Log the request for debugging
            print(f"Getting prediction with ID: {prediction_id}")
            
            # Make the API request
            prediction = await APIClient.get_prediction(prediction_id)
            
            # Log the response for debugging
            print(f"Get prediction response type: {type(prediction)}")
            if prediction:
                print(f"Get prediction response: {json.dumps(prediction, default=str)[:500]}...")
            
            # Handle error responses
            if isinstance(prediction, dict) and "error" in prediction:
                error_msg = prediction["error"]
                st.error(f"Error loading prediction: {error_msg}")
                
                # If it's a connection error, provide troubleshooting steps
                if "connection_error" in prediction:
                    st.info("""
                    Unable to connect to the API. Please check:
                    1. The backend API is running
                    2. Your network connection is working
                    3. The API URL in the configuration is correct
                    """)
                return None
            
            return prediction
    except Exception as e:
        st.error(f"Error loading prediction: {str(e)}")
        return None

async def get_recent_predictions(limit=5):
    """Get recent predictions"""
    try:
        with st.spinner("Loading recent predictions..."):
            # Log the API request for debugging
            print(f"Requesting recent predictions with limit={limit}")
            
            # Make the API request - the API client now ensures trailing slashes
            predictions = await APIClient.get_recent_predictions(limit=limit)
            
            # Log the response for debugging
            print(f"Recent predictions response type: {type(predictions)}")
            if predictions:
                print(f"Recent predictions response: {json.dumps(predictions, default=str)[:500]}...")
            
            # Handle error responses
            if isinstance(predictions, dict) and "error" in predictions:
                error_msg = predictions["error"]
                st.error(f"Error loading recent predictions: {error_msg}")
                
                # If it's a connection error, provide troubleshooting steps
                if "connection_error" in predictions:
                    st.info("""
                    Unable to connect to the API. Please check:
                    1. The backend API is running
                    2. Your network connection is working
                    3. The API URL in the configuration is correct
                    """)
                # If it's a backend error, show a more specific message
                else:
                    st.warning("""
                    The backend API returned an error. This may be due to:
                    1. A temporary issue with the backend service
                    2. A configuration issue with the OpenAI service
                    3. A database connection problem
                    
                    Please try again later or contact the administrator.
                    """)
                return []
            
            # If we got an empty list or None, show a message about backend issues
            if not predictions:
                st.warning("""
                No predictions were returned from the backend. This may be due to:
                1. No predictions have been generated yet
                2. A backend service issue
                
                Try generating a new prediction or check back later.
                """)
                return []
            
            # Return the predictions
            return predictions
    except Exception as e:
        st.error(f"Error loading recent predictions: {str(e)}")
        return []

def render_predictions_page():
    """Render the predictions page"""
    render_header()
    
    st.title("Market Predictions")
    
    # Create tabs for different prediction views
    tab1, tab2 = st.tabs(["Generate Prediction", "Recent Predictions"])
    
    with tab1:
        st.subheader("Generate New Prediction")
        
        # Prediction form
        with st.form(key="prediction_form"):
            # Check if there's a search query in session state
            default_query = ""
            if "search_query" in st.session_state:
                default_query = st.session_state.search_query
                # Clear the search query from session state
                st.session_state.search_query = ""
            
            query = st.text_input("Market Trend or Topic", value=default_query, key="prediction_query")
            
            col1, col2 = st.columns(2)
            
            with col1:
                time_frame_options = ["short_term", "medium_term", "long_term"]
                time_frame_labels = ["Short Term (Days to Weeks)", "Medium Term (Weeks to Months)", "Long Term (Months to Years)"]
                selected_time_frame = st.selectbox(
                    "Time Frame", 
                    options=time_frame_options,
                    format_func=lambda x: time_frame_labels[time_frame_options.index(x)],
                    index=1,
                    key="prediction_time_frame"
                )
            
            with col2:
                max_ideas_options = [3, 5, 10]
                max_ideas = st.selectbox("Maximum Trade Ideas", max_ideas_options, index=1, key="prediction_max_ideas")
            
            # Optional sectors of interest
            sectors_input = st.text_input(
                "Sectors of Interest (comma-separated, optional)", 
                key="prediction_sectors"
            )
            
            # Convert sectors input to list
            sectors_of_interest = None
            if sectors_input:
                sectors_of_interest = [s.strip() for s in sectors_input.split(",") if s.strip()]
            
            submit_button = st.form_submit_button(label="Generate Prediction")
        
        # Process form submission
        if submit_button:
            if not query:
                st.warning("Please enter a market trend or topic")
            else:
                # Generate prediction
                prediction = asyncio.run(generate_prediction(
                    query=query,
                    time_frame=selected_time_frame,
                    sectors_of_interest=sectors_of_interest,
                    max_trade_ideas=max_ideas
                ))
                
                # Store prediction in session state
                if prediction:
                    st.session_state.current_prediction = prediction
        
        # Check if there's a prediction ID in session state
        elif "prediction_id" in st.session_state and st.session_state.prediction_id:
            # Load the prediction
            prediction = asyncio.run(get_prediction(st.session_state.prediction_id))
            
            # Store prediction in session state and clear the ID
            if prediction:
                st.session_state.current_prediction = prediction
                st.session_state.prediction_id = None
        
        # Display current prediction
        if "current_prediction" in st.session_state and st.session_state.current_prediction:
            render_prediction(st.session_state.current_prediction)
    
    with tab2:
        st.subheader("Recent Predictions")
        
        # Refresh button
        if st.button("Refresh", key="refresh_predictions"):
            # Clear recent predictions from session state
            if "recent_predictions_list" in st.session_state:
                del st.session_state.recent_predictions_list
        
        # Load recent predictions if not already loaded
        if "recent_predictions_list" not in st.session_state:
            recent_predictions = asyncio.run(get_recent_predictions())
            st.session_state.recent_predictions_list = recent_predictions
        
        # Display recent predictions
        recent_predictions = st.session_state.get("recent_predictions_list", [])
        
        if not recent_predictions:
            st.info("No recent predictions available.")
        else:
            for i, prediction in enumerate(recent_predictions):
                # Create an expander for each prediction
                with st.expander(f"{prediction.get('query', 'Unknown Query')} - {len(prediction.get('trade_ideas', []))} Trade Ideas"):
                    # Display the prediction
                    render_prediction(prediction, show_header=False)
                    
                    # Add a button to set as current prediction
                    if st.button("View Full Prediction", key=f"view_full_{i}"):
                        st.session_state.current_prediction = prediction
                        st.session_state.page = "Predictions"  # Stay on the same page
                        st.experimental_rerun() 