import httpx
import json
import time
from typing import Dict, Any, List, Optional
import streamlit as st
from .config import API_BASE_URL

class APIClient:
    """Client for interacting with the backend API"""
    
    @classmethod
    async def _make_request(
        cls, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a request to the API
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request data
            
        Returns:
            API response
        """
        # IMPORTANT: Always add trailing slash to prevent redirects
        if not endpoint.endswith('/'):
            endpoint = f"{endpoint}/"
            
        # Always use HTTP instead of HTTPS to avoid protocol redirects
        url = API_BASE_URL.replace("https://", "http://") + endpoint
        
        print(f"Making {method} request to {url}")
        if params:
            print(f"With params: {json.dumps(params, default=str)}")
        
        try:
            # Use a longer timeout and follow redirects
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                if method == "GET":
                    response = await client.get(url, params=params)
                elif method == "POST":
                    response = await client.post(url, json=data, params=params)
                else:
                    return {"error": f"Unsupported method: {method}"}
                
                print(f"Response status: {response.status_code}")
                
                # Check if we got redirected
                if len(response.history) > 0:
                    original_url = str(response.history[0].url)
                    final_url = str(response.url)
                    print(f"Request was redirected: {original_url} -> {final_url}")
                
                if response.status_code == 200:
                    try:
                        json_response = response.json()
                        print(f"Response JSON: {json.dumps(json_response, default=str)[:500]}...")
                        return json_response
                    except Exception as e:
                        print(f"Error parsing JSON response: {str(e)}")
                        print(f"Response text: {response.text[:500]}...")
                        return {"error": "Invalid JSON response", "raw_response": response.text[:500]}
                else:
                    print(f"API error: {response.status_code} - {response.text[:500]}")
                    return {
                        "error": f"API error: {response.status_code}",
                        "details": response.text[:500],
                        "status": "error"
                    }
        except httpx.RequestError as e:
            print(f"Request error: {str(e)}")
            return {"connection_error": str(e), "status": "error"}
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return {"error": str(e), "status": "error"}
    
    @classmethod
    async def search_news(cls, query: str = None, sentiment: str = None, sectors: List[str] = None, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """
        Search for news articles
        
        Args:
            query: Text search query
            sentiment: Filter by sentiment (bullish, bearish, neutral)
            sectors: Filter by sectors
            limit: Maximum number of results to return
            offset: Number of results to skip
            
        Returns:
            News search results
        """
        print(f"Searching news with query={query}, sentiment={sentiment}, sectors={sectors}, limit={limit}, offset={offset}")
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if query:
            params["query"] = query
            
        if sentiment:
            params["sentiment"] = sentiment
            
        if sectors:
            params["sectors"] = sectors
            
        # Use endpoint with trailing slash
        return await cls._make_request("GET", "/news", params=params)
    
    @classmethod
    async def fetch_news(cls, query: str = None, max_results: int = 30) -> List[str]:
        """
        Fetch and store news articles
        
        Args:
            query: Search query for news
            max_results: Maximum number of results to fetch
            
        Returns:
            List of article IDs
        """
        print(f"Fetching news with query={query}, max_results={max_results}")
        
        data = {
            "max_results": max_results
        }
        
        if query:
            data["query"] = query
            
        # Use endpoint with trailing slash
        return await cls._make_request("POST", "/news/fetch", data=data)
    
    @classmethod
    async def get_news_article(cls, article_id: str) -> Dict[str, Any]:
        """
        Get a specific news article by ID
        
        Args:
            article_id: ID of the article to retrieve
            
        Returns:
            News article
        """
        print(f"Getting news article with ID={article_id}")
        
        # Use endpoint with trailing slash
        return await cls._make_request("GET", f"/news/{article_id}")
    
    @classmethod
    async def analyze_article_sentiment(cls, article_id: str) -> Dict[str, Any]:
        """
        Analyze sentiment for a news article
        
        Args:
            article_id: ID of the article to analyze
            
        Returns:
            Updated news article with sentiment
        """
        print(f"Analyzing sentiment for article with ID={article_id}")
        
        # Use endpoint with trailing slash
        return await cls._make_request("POST", f"/news/{article_id}/analyze")
    
    @classmethod
    async def generate_prediction(cls, query: str, time_frame: str = "medium_term", sectors_of_interest: List[str] = None, max_trade_ideas: int = 5) -> Dict[str, Any]:
        """
        Generate a market prediction
        
        Args:
            query: Search query for prediction
            time_frame: Time frame for prediction (short_term, medium_term, long_term)
            sectors_of_interest: List of sectors to focus on
            max_trade_ideas: Maximum number of trade ideas to generate
            
        Returns:
            Market prediction
        """
        print(f"Generating prediction with query={query}, time_frame={time_frame}, sectors_of_interest={sectors_of_interest}, max_trade_ideas={max_trade_ideas}")
        
        data = {
            "query": query,
            "time_frame": time_frame,
            "max_trade_ideas": max_trade_ideas
        }
        
        if sectors_of_interest:
            data["sectors_of_interest"] = sectors_of_interest
            
        # Use endpoint with trailing slash
        return await cls._make_request("POST", "/predictions", data=data)
    
    @classmethod
    async def get_prediction(cls, prediction_id: str) -> Dict[str, Any]:
        """
        Get a specific market prediction by ID
        
        Args:
            prediction_id: ID of the prediction to retrieve
            
        Returns:
            Market prediction
        """
        print(f"Getting prediction with ID={prediction_id}")
        
        # Use endpoint with trailing slash
        return await cls._make_request("GET", f"/predictions/{prediction_id}")
    
    @classmethod
    async def get_recent_predictions(cls, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get recent market predictions
        
        Args:
            limit: Maximum number of predictions to return
            offset: Number of predictions to skip
            
        Returns:
            List of market predictions
        """
        print(f"Getting recent predictions with limit={limit}, offset={offset}")
        
        # Use endpoint with trailing slash
        endpoint = "/predictions"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        response = await cls._make_request("GET", endpoint, params=params)
        
        # Log the response for debugging
        print(f"Recent predictions API response type: {type(response)}")
        if response:
            print(f"Recent predictions API response: {json.dumps(response, default=str)[:500]}...")
        
        # If the response is a dictionary with 'data' field, extract the data
        if isinstance(response, dict) and "data" in response and "error" not in response:
            return response["data"]
        
        # If the response is a dictionary with 'items' field, extract the items
        if isinstance(response, dict) and "items" in response and "error" not in response:
            return response["items"]
        
        # If the response is already a list, return it
        if isinstance(response, list):
            return response
            
        # If there's an error, return an empty list
        if isinstance(response, dict) and "error" in response:
            print(f"Error in get_recent_predictions: {response['error']}")
            return []
            
        # If there's an unexpected response, return it as is
        return response
    
    @classmethod
    async def health_check(cls) -> Dict[str, Any]:
        """
        Check the health of the API
        
        Returns:
            Health check response
        """
        try:
            print(f"Checking API health at {API_BASE_URL}/health")
            
            # Use endpoint with trailing slash
            response = await cls._make_request("GET", "/health")
            
            # Update connection status in session state
            if "api_connected" not in st.session_state:
                st.session_state.api_connected = False
                
            if "error" not in response and "connection_error" not in response and "redirect_error" not in response:
                st.session_state.api_connected = True
                print(f"API health check successful: {json.dumps(response, default=str)}")
            else:
                st.session_state.api_connected = False
                print(f"API health check failed: {json.dumps(response, default=str)}")
                
            return response
        except Exception as e:
            print(f"API health check exception: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            if "api_connected" in st.session_state:
                st.session_state.api_connected = False
            return {"error": str(e), "status": "error"} 