# Deploying to Streamlit Cloud

This guide will walk you through deploying the AI Market Prediction frontend to Streamlit Cloud.

## Prerequisites

- A GitHub account
- The repository pushed to GitHub (already done)

## Steps to Deploy

1. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in with your GitHub account.

2. Click on "New app" button.

3. Select the repository `PFJF123/ai-market-prediction-frontend`.

4. Configure the app:
   - **Main file path**: `streamlit_app.py`
   - **Branch**: `main`
   - **App URL**: Choose a custom subdomain or use the default

5. Advanced Settings:
   - **Python version**: 3.9 or higher
   - **Packages**: No need to specify as they are in requirements.txt

6. Add Secrets (if needed):
   - Click on "Advanced settings" > "Secrets"
   - Add the following secrets:
     ```
     [api]
     base_url = "https://your-backend-api-url.com"
     
     [openai]
     api_key = "your_openai_api_key"
     
     [mongodb]
     uri = "your_mongodb_uri"
     ```

7. Click "Deploy" and wait for the app to be deployed.

8. Once deployed, you can access your app at the URL provided by Streamlit Cloud.

## Troubleshooting

- If you encounter any issues with dependencies, check the logs in the Streamlit Cloud dashboard.
- Make sure all required packages are listed in `requirements.txt`.
- If the app fails to connect to the backend API, check the `base_url` in the secrets configuration.

## Updating the App

To update the app:

1. Make changes to the code locally.
2. Commit and push the changes to GitHub.
3. Streamlit Cloud will automatically redeploy the app with the new changes. 