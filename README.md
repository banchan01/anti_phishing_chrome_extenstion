# Anti-Phishing Chrome Extension

A machine learning-powered Chrome extension that helps detect and prevent phishing attacks in real-time.

## Features

- Real-time URL analysis
- Machine learning-based phishing detection
- Page rank and Google index checking
- Visual notifications for suspicious sites
- Detailed analysis popup
- MongoDB integration for tracking detected phishing sites

## Architecture

The project consists of three main components:

1. **Chrome Extension**
   - Content scripts for webpage interaction
   - Background service worker
   - Popup interface for results display

2. **Flask Backend**
   - REST API for URL analysis
   - Integration with ML model
   - Page rank and Google index checking
   - MongoDB database connection (Future improvements)

3. **Machine Learning**
   - Random Forest classifier
   - Feature extraction
   - Model training scripts
   - Saved model files


## Installation

1. Install Python dependencies:
- Run `cd flask-backend` to navigate to the backend directory.
- Set-up python virtual environment `python3 -m venv venv`
- Activate the virtual environment with `source venv/bin/activate` (Mac) or `venv\Scripts\activate` (Windows)
- Install dependencies with `pip install pandas numpy scikit-learn joblib matplotlib seaborn`

2. Set up environment variables:
- Create `.env` file in flask-backend directory
- Copy the code and replace 
    ```bash
    # API Keys
    OPENPAGE_API_KEY=<your_openpage_api_key>

    # Google Index API Key
    GOOGLE_API_KEY=<your_google_api_key>
    GOOGLE_SEARCH_ENGINE_ID=<your_google_search_engine_id>

3. Steps to get required API keys
- OpenPage Rank API
    - Visit OpenPageRank : https://www.domcop.com/openpagerank/
    - Create an account/Sign up
    - Navigate to API dashboard
    - Replace `<your_openpage_api_key>` in `.env` with your actual API key

- Google API Key
    - Go to Google Cloud Console : https://console.cloud.google.com/
    - Create new project/Select existing project
    - Enable billing
    - Go to "APIs & Services" > "Library"
    - Enable "Custom Search API"
    - Go to "Credentials"
    - Create API Key (Create Credentials > API Key)
    - Replace `<your_google_api_key>` in `.env` with your actual API key

- Google Search Engine ID
    - Go to Programmable Search Engine : https://programmablesearchengine.google.com/
    - Click "Create Search Engine"
    - Configure settings:
        - Set search engine name
        - Use "*" for all sites
        - Click "Create" to finalize the setup
        - Copy `Search Engine ID` and replace `<your_google_search_engine_id>` in `.env`
    
4. Load the Chrome extension:
- Open Chrome extensions page
- Enable Developer mode
- Click "Load unpacked"
- Select the chromeExtension directory

## Usage
1. Start the Flask backend:
    - Run `cd flask-backend` to navigate to the backend directory.
    - Start the app with `python app.py`.
    - Enjoy the extension!

## Tech Stack 
- Frontend: HTML, CSS, JavaScript
- Backend: Flask, Python
- ML: scikit-learn, NumPy, Pandas
- Database: MongoDB
- APIs: OpenPageRank, Google Search
