import streamlit as st
import asyncio
from ..components.header import render_header
from ..components.news_card import render_news_list
from ..utils.api import APIClient

async def fetch_news(query=None, max_results=30):
    """Fetch news from API"""
    try:
        with st.spinner("Fetching news..."):
            response = await APIClient.fetch_news(query=query, max_results=max_results)
            
            # Log the raw response for debugging
            print(f"Fetch news response: {str(response)[:500]}...")
            
            # Handle error responses
            if isinstance(response, dict) and "error" in response:
                st.error(f"Error fetching news: {response['error']}")
                st.session_state.fetched_article_ids = []
                return
            
            # Handle different response formats
            article_ids = []
            if isinstance(response, dict):
                if "data" in response:
                    article_ids = response.get("data", [])
                elif "items" in response:
                    article_ids = response.get("items", [])
                elif "article_ids" in response:
                    article_ids = response.get("article_ids", [])
            elif isinstance(response, list):
                article_ids = response
            
            # Ensure article_ids is a list
            if not isinstance(article_ids, list):
                print(f"Converting article_ids from {type(article_ids)} to list")
                try:
                    article_ids = list(article_ids)
                except Exception as e:
                    print(f"Error converting to list: {str(e)}")
                    article_ids = []
            
            # Store the article IDs in session state
            st.session_state.fetched_article_ids = article_ids
            
            # Log the article IDs for debugging
            print(f"Fetched article IDs type: {type(st.session_state.fetched_article_ids)}")
            print(f"Fetched article IDs: {st.session_state.fetched_article_ids}")
            
            # Show success message
            if article_ids:
                st.success(f"Fetched {len(article_ids)} news articles")
            else:
                st.info("No news articles found matching your query")
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        st.session_state.fetched_article_ids = []
        # Log the exception details for debugging
        import traceback
        print(f"Exception in fetch_news: {traceback.format_exc()}")

async def search_news(query=None, sentiment=None, sectors=None, limit=10, offset=0):
    """Search news from API"""
    try:
        with st.spinner("Searching news..."):
            response = await APIClient.search_news(
                query=query,
                sentiment=sentiment,
                sectors=sectors,
                limit=limit,
                offset=offset
            )
            
            # Log the raw response for debugging
            print(f"News search response: {str(response)[:500]}...")
            
            # Handle error responses
            if isinstance(response, dict) and "error" in response:
                st.error(f"Error searching news: {response['error']}")
                return []
            
            # Handle different response formats
            if isinstance(response, dict):
                # Extract data from dictionary response
                if "data" in response:
                    return response.get("data", [])
                elif "items" in response:
                    return response.get("items", [])
                elif "articles" in response:
                    return response.get("articles", [])
                else:
                    # Single article
                    return [response]
            elif isinstance(response, list):
                # List of articles
                return response
            else:
                # Unknown format
                st.error("Unexpected response format from API")
                return []
    except Exception as e:
        st.error(f"Error searching news: {str(e)}")
        return []

async def analyze_sentiment(article_id):
    """Analyze sentiment for a news article"""
    try:
        with st.spinner("Analyzing sentiment..."):
            response = await APIClient.analyze_article_sentiment(article_id)
            
            # Log the raw response for debugging
            print(f"Sentiment analysis response: {str(response)[:500]}...")
            
            # Handle error responses
            if isinstance(response, dict) and "error" in response:
                st.error(f"Error analyzing sentiment: {response['error']}")
                return None
            
            # Return the updated article
            return response
    except Exception as e:
        st.error(f"Error analyzing sentiment: {str(e)}")
        return None

def render_news_page():
    """Render the news page"""
    render_header()
    
    # Initialize session state variables if they don't exist
    if "fetched_article_ids" not in st.session_state:
        st.session_state.fetched_article_ids = []
    
    if "analyzed_articles" not in st.session_state:
        st.session_state.analyzed_articles = []
    
    st.title("Financial News")
    
    # Create tabs for different news views
    tab1, tab2 = st.tabs(["Search News", "Fetch Latest News"])
    
    with tab1:
        st.subheader("Search News Articles")
        
        # Search form
        with st.form(key="news_search_form"):
            search_query = st.text_input("Search Query", key="news_search_query")
            
            col1, col2 = st.columns(2)
            
            with col1:
                sentiment_options = ["All", "Bullish", "Bearish", "Neutral"]
                selected_sentiment = st.selectbox("Sentiment", sentiment_options, key="news_search_sentiment")
            
            with col2:
                limit_options = [10, 20, 50, 100]
                selected_limit = st.selectbox("Results Limit", limit_options, key="news_search_limit")
            
            submit_button = st.form_submit_button(label="Search")
        
        # Process form submission
        if submit_button:
            # Convert sentiment selection to API parameter
            sentiment_param = None
            if selected_sentiment != "All":
                sentiment_param = selected_sentiment.lower()
            
            # Search news
            search_results = asyncio.run(search_news(
                query=search_query,
                sentiment=sentiment_param,
                limit=selected_limit
            ))
            
            # Store results in session state
            st.session_state.news_search_results = search_results
        
        # Display search results
        if "news_search_results" in st.session_state and st.session_state.news_search_results:
            render_news_list(st.session_state.news_search_results)
        else:
            st.info("Search for news articles to see results here.")
    
    with tab2:
        st.subheader("Fetch Latest News")
        
        # Fetch form
        with st.form(key="news_fetch_form"):
            fetch_query = st.text_input("Topic (optional)", key="news_fetch_query")
            
            max_results_options = [10, 30, 50, 100]
            max_results = st.selectbox("Maximum Results", max_results_options, index=1, key="news_fetch_max")
            
            fetch_button = st.form_submit_button(label="Fetch News")
        
        # Process form submission
        if fetch_button:
            # Fetch news
            asyncio.run(fetch_news(query=fetch_query, max_results=max_results))
        
        # Display fetched article IDs
        if st.session_state.fetched_article_ids:
            st.success(f"Fetched {len(st.session_state.fetched_article_ids)} articles")
            
            # Option to analyze sentiment
            if st.button("Analyze Sentiment for All Articles"):
                # Get the first 10 articles to analyze (to avoid overloading)
                if isinstance(st.session_state.fetched_article_ids, list):
                    article_ids_to_analyze = st.session_state.fetched_article_ids[:10]
                else:
                    # If it's not a list, convert it to a list first
                    try:
                        article_ids_to_analyze = list(st.session_state.fetched_article_ids)[:10]
                    except Exception as e:
                        st.error(f"Error preparing articles for analysis: {str(e)}")
                        article_ids_to_analyze = []
                
                # Log the article IDs for debugging
                print(f"Article IDs to analyze: {article_ids_to_analyze}")
                
                analyzed_articles = []
                for article_id in article_ids_to_analyze:
                    try:
                        with st.spinner(f"Analyzing article {article_ids_to_analyze.index(article_id) + 1}/{len(article_ids_to_analyze)}..."):
                            updated_article = asyncio.run(analyze_sentiment(article_id))
                            if updated_article:
                                analyzed_articles.append(updated_article)
                    except Exception as e:
                        st.error(f"Error analyzing article {article_id}: {str(e)}")
                        continue
                
                # Store analyzed articles in session state
                st.session_state.analyzed_articles = analyzed_articles
                st.success(f"Analyzed sentiment for {len(analyzed_articles)} articles")
            
            # Display analyzed articles if available
            if st.session_state.analyzed_articles:
                render_news_list(st.session_state.analyzed_articles)
            else:
                try:
                    # Search for the fetched articles to display them
                    # Ensure fetched_article_ids is a list before slicing
                    if isinstance(st.session_state.fetched_article_ids, list):
                        article_ids_to_display = st.session_state.fetched_article_ids[:20]  # Limit to 20 for display
                    else:
                        # If it's not a list, convert it to a list first
                        article_ids_to_display = list(st.session_state.fetched_article_ids)[:20]
                    
                    # Log the article IDs for debugging
                    print(f"Article IDs to display: {article_ids_to_display}")
                    
                    # Fetch articles one by one
                    articles_to_display = []
                    for article_id in article_ids_to_display:
                        article = asyncio.run(APIClient.get_news_article(article_id))
                        if article and isinstance(article, dict) and "error" not in article:
                            articles_to_display.append(article)
                    
                    # Display the articles
                    if articles_to_display:
                        render_news_list(articles_to_display)
                    else:
                        st.info("No articles to display. Try fetching news first.")
                except Exception as e:
                    st.error(f"Error displaying articles: {str(e)}")
                    st.info("Please try fetching news again.")
                    # Log the exception details for debugging
                    import traceback
                    print(f"Exception details: {traceback.format_exc()}")
                    print(f"Fetched article IDs type: {type(st.session_state.fetched_article_ids)}")
                    print(f"Fetched article IDs: {st.session_state.fetched_article_ids}")
        else:
            st.info("Fetch news to see articles here.") 