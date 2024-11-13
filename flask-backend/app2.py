# -*- coding: cp949 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model

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

# Load the model
model = load_model("../flash-backend/models/CNN_model.h5")  # Use load_model for Keras models

# Hyperparameter settings
max_length = 100  # Maximum URL length
vocab_size = 1000  # Size of character vocabulary

# Tokenizer setup
tokenizer = Tokenizer(char_level=True, oov_token='UNK')
# Note: Ensure that tokenizer is fitted on the training data beforehand and saved using joblib
# Load the pre-trained tokenizer
tokenizer = joblib.load("../ml/model/CNN_tokenizer.joblib")

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

        # Prepare URL as input to the model
        sequence = tokenizer.texts_to_sequences([url])
        X = pad_sequences(sequence, maxlen=max_length, padding='post')

        # Make prediction
        prediction = model.predict(X)[0][0]
        is_phishing = int(prediction > 0.5)
        
        response_data = {
            'url': url,
            'is_phishing': is_phishing,
            'prediction_score': float(prediction),
            'status': 'error' if is_phishing else 'success',
            'message': 'Warning: Phishing Site Detected' if is_phishing else 'Site Appears Safe'
        }

        return jsonify(response_data)

    except Exception as e:
        print(f"Error checking URL: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    connect_to_database()
    app.run(port=3000, debug=True)
