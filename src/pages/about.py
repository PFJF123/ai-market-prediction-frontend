import streamlit as st
from ..components.header import render_header
from ..utils.config import THEME_PRIMARY_COLOR

def render_about_page():
    """Render the about page"""
    render_header()
    
    st.title("About AI Market Prediction")
    
    st.markdown(
        """
        AI Market Prediction is an advanced system that analyzes real-time financial and geopolitical news 
        to predict sector movements and generate trade recommendations using artificial intelligence.
        """
    )
    
    # How it works section
    st.header("How It Works")
    
    st.markdown(
        f"""
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 20px; margin-bottom: 20px;">
            <h3 style="color: {THEME_PRIMARY_COLOR};">1. News Scraping & Processing</h3>
            <p>
                Our system continuously collects financial and geopolitical news from multiple sources:
                <ul>
                    <li><strong>Google News RSS</strong>: Real-time news from various publishers</li>
                    <li><strong>NewsAPI.org</strong>: Curated financial news articles</li>
                </ul>
                All news articles are stored in a MongoDB database and processed for sentiment analysis.
            </p>
        </div>
        
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 20px; margin-bottom: 20px;">
            <h3 style="color: {THEME_PRIMARY_COLOR};">2. AI Sentiment Analysis</h3>
            <p>
                We use OpenAI's GPT-4o to analyze the sentiment of each news article:
                <ul>
                    <li><strong>Sentiment Classification</strong>: Bullish, Bearish, or Neutral</li>
                    <li><strong>Sector Identification</strong>: Which market sectors are affected</li>
                    <li><strong>Keyword Extraction</strong>: Important entities and concepts</li>
                </ul>
                This provides a structured view of how news might impact different market sectors.
            </p>
        </div>
        
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 20px; margin-bottom: 20px;">
            <h3 style="color: {THEME_PRIMARY_COLOR};">3. Market Prediction</h3>
            <p>
                Our prediction engine combines GPT-4o with XGBoost to generate actionable insights:
                <ul>
                    <li><strong>Sector Movement Detection</strong>: Predicting which sectors will move and by how much</li>
                    <li><strong>Trade Idea Generation</strong>: Specific buy/sell recommendations with confidence scores</li>
                    <li><strong>Time Frame Analysis</strong>: Short-term, medium-term, and long-term predictions</li>
                </ul>
                All predictions are backed by relevant news articles and AI reasoning.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Tech stack section
    st.header("Technology Stack")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 20px; height: 100%;">
                <h3 style="color: {THEME_PRIMARY_COLOR};">Backend</h3>
                <ul>
                    <li><strong>FastAPI</strong>: High-performance API framework</li>
                    <li><strong>MongoDB</strong>: News article storage</li>
                    <li><strong>PostgreSQL</strong>: Prediction data and logs</li>
                    <li><strong>OpenAI GPT-4o</strong>: Sentiment analysis and reasoning</li>
                    <li><strong>XGBoost</strong>: Machine learning for predictions</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 20px; height: 100%;">
                <h3 style="color: {THEME_PRIMARY_COLOR};">Frontend</h3>
                <ul>
                    <li><strong>Streamlit</strong>: Interactive web application</li>
                    <li><strong>Plotly</strong>: Interactive data visualizations</li>
                    <li><strong>Pandas</strong>: Data manipulation and analysis</li>
                    <li><strong>HTTPX</strong>: Asynchronous HTTP client</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Deployment section
    st.header("Deployment")
    
    st.markdown(
        f"""
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 20px; margin-bottom: 20px;">
            <p>
                The AI Market Prediction system is deployed using modern cloud infrastructure:
                <ul>
                    <li><strong>Backend API</strong>: Hosted on Railway</li>
                    <li><strong>Databases</strong>: MongoDB and PostgreSQL on Railway</li>
                    <li><strong>Frontend</strong>: Deployed on Vercel</li>
                    <li><strong>Source Code</strong>: Managed on GitHub</li>
                </ul>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Disclaimer
    st.header("Disclaimer")
    
    st.markdown(
        """
        <div style="border: 1px solid #f44336; border-radius: 5px; padding: 20px; margin-bottom: 20px; background-color: #ffebee;">
            <p>
                <strong>Important:</strong> AI Market Prediction is a demonstration project and should not be used as the sole basis for investment decisions. The predictions and trade ideas generated by this system are based on AI analysis of news and may not accurately reflect market movements. Always consult with a qualified financial advisor before making investment decisions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Contact information
    st.header("Contact")
    
    st.markdown(
        """
        For more information about this project, please contact us at:
        
        - Email: info@aimarketprediction.com
        - GitHub: [github.com/yourusername/ai-market-prediction](https://github.com/yourusername/ai-market-prediction)
        """
    ) 