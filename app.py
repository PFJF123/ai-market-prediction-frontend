"""
AI Market Prediction - Main Entry Point

This file serves as the entry point for the Streamlit application.
It imports and runs the main application from the src directory.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import the main function from the src/app.py file
from src.app import main

# Run the main function
if __name__ == "__main__":
    main() 