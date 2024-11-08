from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import joblib
import numpy as np
from dotenv import load_dotenv
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from urllib.parse import urlparse
from controllers.page_rank_controller import get_page_rank
from controllers.google_index_controller import get_google_index
from controllers.database_controller import connect_to_database, add_phishing_link
from config import ALLOWED_DOMAINS  # Import ALLOWED_DOMAINS from config.py

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# MongoDB configuration (also consider moving to config.py if needed)
# app.config["MONGO_URI"] = os.getenv("MONGODB_URI", "mongodb://localhost:27017/phishing")
# mongo = PyMongo(app)

# Load the DNN model and scaler
model = load_model("models/dnn_model.h5")
scaler = joblib.load("scaler.joblib")

# Feature names in exact order from training
FEATURE_NAMES = [
    'length_url', 'length_hostname', 'ip', 'nb_dots', 'nb_hyphens', 'nb_qm', 'nb_and',
    'nb_eq', 'nb_underscore', 'nb_percent', 'nb_slash', 'nb_semicolumn', 'nb_www',
    'page_rank', 'google_index'
]

@app.before_request
def log_request():
    print(f"Received {request.method} request for {request.path}")

def is_trusted_domain(url):
    """Check if the URL belongs to a trusted domain in the allowlist."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "")  # Remove 'www.' prefix if present
    return any(allowed_domain in domain for allowed_domain in ALLOWED_DOMAINS)

@app.route('/api/check-url', methods=['POST'])
def check_url():
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Check if the URL is in the allowlist of trusted domains
        if is_trusted_domain(url):
            response_data = {
                'url': url,
                'is_phishing': 0,
                'prediction_score': 0.0,
                'status': 'success',
                'message': 'Site Appears Safe (Trusted Domain)',
                'analysis': {}
            }
            return jsonify(response_data)

        # Extract features
        features = {
            'length_url': len(url),
            'length_hostname': len(url.split('/')[2]) if len(url.split('/')) > 2 else 0,
            'ip': 1 if '://' in url else 0,
            'nb_dots': url.count('.'),
            'nb_hyphens': url.count('-'),
            'nb_qm': url.count('?'),
            'nb_and': url.count('&'),
            'nb_eq': url.count('='),
            'nb_underscore': url.count('_'),
            'nb_percent': url.count('%'),
            'nb_slash': url.count('/'),
            'nb_semicolumn': url.count(';'),
            'nb_www': 1 if 'www' in url else 0,
            'page_rank': 0,
            'google_index': 0
        }

        # Get PageRank and Google Index
        page_rank_result = get_page_rank(url)
        google_index_result = get_google_index(url)

        features['page_rank'] = page_rank_result.get('page_rank', 0)
        features['google_index'] = 1 if google_index_result.get('is_indexed') else 0

        # Handle missing values like in training
        for name in FEATURE_NAMES:
            features[name] = features.get(name, -1)

        # Make prediction with ordered and scaled features
        feature_array = np.array([[features[name] for name in FEATURE_NAMES]], dtype=np.float32)
        feature_array = scaler.transform(feature_array)  # Scale the features
        prediction = model.predict(feature_array)[0][0]  # Get the prediction probability
        is_phishing = int(prediction > 0.5)  # Threshold at 0.5
        
        # Save to database if phishing
        if is_phishing:
            add_phishing_link(url, features, float(prediction))
        
        response_data = {
            'url': url,
            'features': features,
            'is_phishing': is_phishing,
            'prediction_score': float(prediction),
            'status': 'error' if is_phishing else 'success',
            'message': 'Warning: Phishing Site Detected' if is_phishing else 'Site Appears Safe',
            'analysis': {
                'page_rank': features['page_rank'],
                'google_index': features['google_index']
            }
        }

        return jsonify(response_data)

    except Exception as e:
        print(f"Error checking URL: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    connect_to_database()
    app.run(port=3000, debug=True)
