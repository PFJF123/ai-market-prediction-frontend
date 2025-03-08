import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from ..utils.config import THEME_PRIMARY_COLOR

def format_date(date_str):
    """Format date string for display"""
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date_obj.strftime("%b %d, %Y %H:%M")
    except:
        return date_str

def get_sentiment_color(sentiment):
    """Get color based on sentiment"""
    if sentiment == "bullish":
        return "#4CAF50"  # Green
    elif sentiment == "bearish":
        return "#F44336"  # Red
    else:
        return "#9E9E9E"  # Gray

def get_sentiment_icon(sentiment):
    """Get icon based on sentiment"""
    if sentiment == "bullish":
        return "↑"  # Up arrow
    elif sentiment == "bearish":
        return "↓"  # Down arrow
    else:
        return "→"  # Right arrow

def render_news_card(article):
    """
    Render a news article card
    
    Args:
        article: News article data
    """
    # Create a card with border
    with st.container():
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
                <h3 style="margin-top: 0;">{article.get('title', 'No Title')}</h3>
                <p style="color: #666; font-size: 0.8rem;">
                    {article.get('source', 'Unknown Source')} | {format_date(article.get('published_at', ''))}
                </p>
            """,
            unsafe_allow_html=True
        )
        
        # Display sentiment if available
        sentiment = article.get('sentiment')
        if sentiment:
            sentiment_color = get_sentiment_color(sentiment)
            sentiment_icon = get_sentiment_icon(sentiment)
            sentiment_score = article.get('sentiment_score', 0.5)
            
            # Create a sentiment gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=sentiment_score * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"Sentiment: {sentiment.capitalize()} {sentiment_icon}"},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1},
                    'bar': {'color': sentiment_color},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "#FFFFFF",
                    'steps': [
                        {'range': [0, 33], 'color': '#ffcdd2'},
                        {'range': [33, 66], 'color': '#ffecb3'},
                        {'range': [66, 100], 'color': '#c8e6c9'}
                    ],
                }
            ))
            
            fig.update_layout(
                height=150,
                margin=dict(l=10, r=10, t=50, b=10),
                paper_bgcolor="white",
                font={'size': 12}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display sectors if available
            sectors = article.get('sectors', [])
            if sectors:
                st.markdown(f"**Sectors:** {', '.join(sectors)}")
            
            # Display keywords if available
            keywords = article.get('keywords', [])
            if keywords:
                st.markdown(f"**Keywords:** {', '.join(keywords)}")
        
        # Display summary if available
        summary = article.get('summary')
        if summary:
            st.markdown(f"**Summary:** {summary}")
        
        # Display content preview if available
        content = article.get('content')
        if content:
            # Truncate content if too long
            if len(content) > 300:
                content = content[:300] + "..."
            st.markdown(f"**Content:** {content}")
        
        # Add link to original article
        url = article.get('url')
        if url:
            st.markdown(f"[Read full article]({url})")
        
        # Close the card div
        st.markdown("</div>", unsafe_allow_html=True)

def render_news_list(articles, show_sentiment_filter=True):
    """
    Render a list of news articles with optional filtering
    
    Args:
        articles: List of news articles
        show_sentiment_filter: Whether to show sentiment filter
    """
    if not articles:
        st.info("No news articles found.")
        return
    
    # Add sentiment filter if requested
    selected_sentiment = None
    if show_sentiment_filter:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("All", key="filter_all", use_container_width=True):
                selected_sentiment = None
        
        with col2:
            if st.button("Bullish", key="filter_bullish", use_container_width=True):
                selected_sentiment = "bullish"
        
        with col3:
            if st.button("Bearish", key="filter_bearish", use_container_width=True):
                selected_sentiment = "bearish"
        
        # Store selected sentiment in session state
        if selected_sentiment is not None:
            st.session_state.selected_sentiment = selected_sentiment
        
        # Get selected sentiment from session state
        if "selected_sentiment" in st.session_state:
            selected_sentiment = st.session_state.selected_sentiment
    
    # Filter articles by sentiment if selected
    filtered_articles = articles
    if selected_sentiment:
        filtered_articles = [a for a in articles if a.get('sentiment') == selected_sentiment]
    
    # Display count
    st.markdown(f"**Showing {len(filtered_articles)} of {len(articles)} articles**")
    
    # Render each article
    for article in filtered_articles:
        render_news_card(article) 