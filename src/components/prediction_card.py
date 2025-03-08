import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
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

def get_time_frame_label(time_frame):
    """Get human-readable time frame label"""
    if time_frame == "short_term":
        return "Short Term (Days to Weeks)"
    elif time_frame == "medium_term":
        return "Medium Term (Weeks to Months)"
    elif time_frame == "long_term":
        return "Long Term (Months to Years)"
    else:
        return time_frame.replace("_", " ").title()

def render_sector_predictions(sectors):
    """
    Render sector predictions
    
    Args:
        sectors: List of sector predictions
    """
    if not sectors:
        st.info("No sector predictions available.")
        return
    
    st.subheader("Sector Predictions")
    
    # Create a DataFrame for the sectors
    sector_data = []
    for sector in sectors:
        sector_data.append({
            "Sector": sector.get("sector", "Unknown"),
            "Sentiment": sector.get("sentiment", "neutral"),
            "Confidence": sector.get("confidence", 0.5),
            "Predicted Movement": sector.get("predicted_movement", 0.0),
            "Time Frame": get_time_frame_label(sector.get("time_frame", "medium_term"))
        })
    
    df = pd.DataFrame(sector_data)
    
    # Create a bar chart for predicted movements
    fig = px.bar(
        df,
        x="Sector",
        y="Predicted Movement",
        color="Sentiment",
        color_discrete_map={
            "bullish": "#4CAF50",
            "bearish": "#F44336",
            "neutral": "#9E9E9E"
        },
        text="Predicted Movement",
        title="Predicted Sector Movements (%)",
        height=400
    )
    
    fig.update_layout(
        xaxis_title="Sector",
        yaxis_title="Predicted Movement (%)",
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display sector details in a table
    st.markdown("### Sector Details")
    
    # Format the DataFrame for display
    display_df = df.copy()
    display_df["Confidence"] = display_df["Confidence"].apply(lambda x: f"{x:.1%}")
    display_df["Predicted Movement"] = display_df["Predicted Movement"].apply(lambda x: f"{x:.1f}%")
    
    # Display the table
    st.dataframe(display_df, use_container_width=True)

def render_trade_ideas(trade_ideas):
    """
    Render trade ideas
    
    Args:
        trade_ideas: List of trade ideas
    """
    if not trade_ideas:
        st.info("No trade ideas available.")
        return
    
    st.subheader("Trade Ideas")
    
    # Create cards for each trade idea
    for idea in trade_ideas:
        # Get trade side and color
        side = idea.get("side", "hold")
        if side == "buy":
            side_color = "#4CAF50"  # Green
            side_icon = "↑"  # Up arrow
        elif side == "sell":
            side_color = "#F44336"  # Red
            side_icon = "↓"  # Down arrow
        else:
            side_color = "#9E9E9E"  # Gray
            side_icon = "→"  # Right arrow
        
        # Create a card with border
        with st.container():
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0;">{idea.get('symbol', 'Unknown')} - {idea.get('company_name', 'Unknown Company')}</h3>
                        <span style="background-color: {side_color}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">
                            {side.upper()} {side_icon}
                        </span>
                    </div>
                    <p style="color: #666; margin-top: 5px;">
                        Sector: {idea.get('sector', 'Unknown')} | 
                        Confidence: {idea.get('confidence', 0.5):.1%} | 
                        Time Frame: {get_time_frame_label(idea.get('time_frame', 'medium_term'))}
                    </p>
                """,
                unsafe_allow_html=True
            )
            
            # Display price information if available
            current_price = idea.get('current_price')
            price_target = idea.get('price_target')
            
            if current_price is not None and price_target is not None:
                price_change = ((price_target - current_price) / current_price) * 100
                price_change_color = "#4CAF50" if price_change >= 0 else "#F44336"
                
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                        <div>
                            <span style="font-weight: bold;">Current Price:</span> ${current_price:.2f}
                        </div>
                        <div>
                            <span style="font-weight: bold;">Target Price:</span> ${price_target:.2f}
                        </div>
                        <div>
                            <span style="font-weight: bold; color: {price_change_color};">
                                Potential: {price_change:+.1f}%
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Display reasoning
            reasoning = idea.get('reasoning')
            if reasoning:
                st.markdown(f"**Reasoning:** {reasoning}")
            
            # Close the card div
            st.markdown("</div>", unsafe_allow_html=True)

def render_prediction(prediction, show_header=True):
    """
    Render a market prediction
    
    Args:
        prediction: Market prediction data
        show_header: Whether to show the prediction header
    """
    if not prediction:
        st.info("No prediction data available.")
        return
    
    # Show header if requested
    if show_header:
        st.header(f"Market Prediction: {prediction.get('query', 'Unknown Query')}")
        
        # Show metadata
        col1, col2 = st.columns(2)
        
        with col1:
            created_at = prediction.get('created_at')
            if created_at:
                st.markdown(f"**Created:** {format_date(created_at)}")
        
        with col2:
            related_news_count = prediction.get('related_news_count', 0)
            st.markdown(f"**Based on {related_news_count} news articles**")
    
    # Render sector predictions
    sectors = prediction.get('sectors', [])
    render_sector_predictions(sectors)
    
    # Render trade ideas
    trade_ideas = prediction.get('trade_ideas', [])
    render_trade_ideas(trade_ideas) 