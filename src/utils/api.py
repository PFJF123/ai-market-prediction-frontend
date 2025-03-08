import httpx
import json
import time
from typing import Dict, Any, List, Optional
import streamlit as st
from .config import API_BASE_URL

class APIClient:
    """Client for interacting with the backend API"""
    
    @staticmethod
    async def _make_request(method: str, endpoint: str, params: Dict[str, Any] = None, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a request to the API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body
            
        Returns:
            API response
        """
        url = f"{API_BASE_URL}{endpoint}"
        
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient() as client:
                if method == "GET":
                    response = await client.get(url, params=params, timeout=30.0)
                elif method == "POST":
                    response = await client.post(url, json=data, params=params, timeout=30.0)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                elapsed_time = time.time() - start_time
                
                # Check if the request was successful
                response.raise_for_status()
                
                # Parse the response
                result = response.json()
                
                # Log the request
                print(f"API Request: {method} {endpoint} - {response.status_code} - {elapsed_time:.2f}s")
                
                return result
                
        except httpx.HTTPStatusError as e:
            elapsed_time = time.time() - start_time
            print(f"API Error: {method} {endpoint} - {e.response.status_code} - {elapsed_time:.2f}s")
            
            # Try to parse the error response
            try:
                error_detail = e.response.json().get("detail", str(e))
            except:
                error_detail = str(e)
                
            # Show error in Streamlit
            st.error(f"API Error: {error_detail}")
            
            return {"error": error_detail}
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"API Error: {method} {endpoint} - {str(e)} - {elapsed_time:.2f}s")
            
            # Show error in Streamlit
            st.error(f"API Error: {str(e)}")
            
            return {"error": str(e)}
    
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
            
        return await cls._make_request("GET", "/news", params=params)
    
    @classmethod
    async def fetch_news(cls, query: str = None, max_results: int = 30) -> List[str]:
        """
        Fetch and store news articles
        
        Args:
            query: Search query for news
            max_results: Maximum number of results to fetch per source
            
        Returns:
            List of article IDs
        """
        params = {}
        
        if query:
            params["query"] = query
            
        if max_results:
            params["max_results"] = max_results
            
        return await cls._make_request("GET", "/news/fetch", params=params)
    
    @classmethod
    async def get_news_article(cls, article_id: str) -> Dict[str, Any]:
        """
        Get a specific news article by ID
        
        Args:
            article_id: ID of the article to retrieve
            
        Returns:
            News article
        """
        return await cls._make_request("GET", f"/news/{article_id}")
    
    @classmethod
    async def analyze_article_sentiment(cls, article_id: str) -> Dict[str, Any]:
        """
        Analyze sentiment for a specific news article
        
        Args:
            article_id: ID of the article to analyze
            
        Returns:
            Updated news article with sentiment analysis
        """
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
        data = {
            "query": query,
            "time_frame": time_frame,
            "max_trade_ideas": max_trade_ideas
        }
        
        if sectors_of_interest:
            data["sectors_of_interest"] = sectors_of_interest
            
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
        params = {
            "limit": limit,
            "offset": offset
        }
        
        return await cls._make_request("GET", "/predictions", params=params)
    
    @classmethod
    async def health_check(cls) -> Dict[str, Any]:
        """
        Check the health of the API
        
        Returns:
            Health check response
        """
        return await cls._make_request("GET", "/health") 