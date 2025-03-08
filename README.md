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
5. Set up the following secrets in the Streamlit Cloud dashboard:
   ```toml
   [api]
   base_url = "http://chic-nourishment-production.up.railway.app"
   ```

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/PFJF123/ai-market-prediction-frontend.git
   cd ai-market-prediction-frontend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following content:
   ```
   API_URL=http://chic-nourishment-production.up.railway.app
   ```

4. Run the application:
   ```
   streamlit run app.py
   ```

## Backend Connection

The frontend is configured to connect to the backend API deployed at:
- http://chic-nourishment-production.up.railway.app

If you need to connect to a different backend, update the `API_URL` in the `.env` file.

## Project Structure

- `app.py`: Main application entry point
- `src/app.py`: Core application logic
- `src/components/`: UI components
- `src/pages/`: Application pages
- `src/utils/`: Utility functions
- `.streamlit/`: Streamlit configuration

## Dependencies

See `requirements.txt` for a full list of dependencies. 