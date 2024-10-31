from pymongo import MongoClient
from datetime import datetime
import os

def connect_to_database():
    try:
        mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_uri)
        db = client['phishing']  
        print('Connected to MongoDB')
        return db
    except Exception as e:
        print(f'Database connection error: {str(e)}')
        raise e

def add_phishing_link(url, features, prediction):
    try:
        db = connect_to_database()
        result = db.phishing_links.insert_one({
            'url': url,
            'features': features,
            'prediction': prediction,
            'timestamp': datetime.utcnow()
        })
        return result.inserted_id
    except Exception as e:
        print(f'Error adding phishing link: {str(e)}')
        return None