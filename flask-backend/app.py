from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import joblib
import numpy as np
from dotenv import load_dotenv
import os
from controllers.page_rank_controller import get_page_rank
from controllers.google_index_controller import get_google_index
from controllers.database_controller import connect_to_database, add_phishing_link

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# MongoDB configuration
# app.config["MONGO_URI"] = os.getenv("MONGODB_URI", "mongodb://localhost:27017/phishing")
# mongo = PyMongo(app)

# Load the model
model = joblib.load("../ml/model/random_forest_model.joblib")

# Feature names in exact order from training
FEATURE_NAMES = [
    'length_url',          # Length of the URL
    'length_hostname',     # Length of the hostname
    'ip',                  # Contains IP address (0/1)
    'nb_dots',            # Number of dots
    'nb_hyphens',         # Number of hyphens
    'nb_qm',              # Number of question marks
    'nb_and',             # Number of & symbols
    'nb_eq',              # Number of = symbols
    'nb_underscore',      # Number of underscores
    'nb_percent',         # Number of % symbols
    'nb_slash',           # Number of slashes
    'nb_semicolumn',      # Number of semicolons
    'nb_www',             # Contains 'www' (0/1)
    'page_rank',          # PageRank score
    'google_index'        # Google index (0/1)
]

@app.before_request
def log_request():
    print(f"Received {request.method} request for {request.path}")

@app.route('/api/check-url', methods=['POST'])
def check_url():
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400

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

        # Make prediction with ordered features
        feature_array = np.array([[features[name] for name in FEATURE_NAMES]], dtype=np.float32)
        prediction = model.predict_proba(feature_array)[0]
        is_phishing = int(prediction[1] > 0.5)
        
        # Save to database if phishing
        if is_phishing:
            add_phishing_link(url, features, float(prediction[1]))
        
        response_data = {
            'url': url,
            'features': features,
            'is_phishing': is_phishing,
            'prediction_score': float(prediction[1]),
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
