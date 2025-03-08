# AI Market Prediction Frontend

A Streamlit-based frontend for the AI Market Prediction application that visualizes market predictions based on news sentiment analysis.

## Features

- **Interactive Dashboard**: View market trends and predictions at a glance
- **News Analysis**: Browse and search financial news with AI-powered sentiment analysis
- **Market Predictions**: Visualize XGBoost model predictions for different market sectors
- **Responsive Design**: Optimized for both desktop and mobile viewing

## Deployment

### Streamlit Cloud

This application is designed to be deployed on Streamlit Cloud:

1. Fork or clone this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Deploy the app by selecting this repository
5. Set up any required secrets in the Streamlit Cloud dashboard

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-market-prediction-frontend.git
   cd ai-market-prediction-frontend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run streamlit_app.py
   ```

## Environment Variables

Create a `.streamlit/secrets.toml` file with the following variables:

```toml
[api]
base_url = "your_backend_api_url"
```

## Project Structure

- `streamlit_app.py`: Main application entry point
- `src/components/`: UI components
- `src/pages/`: Application pages
- `src/utils/`: Utility functions
- `.streamlit/`: Streamlit configuration

## Dependencies

See `requirements.txt` for a full list of dependencies. 