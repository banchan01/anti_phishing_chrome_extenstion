from pymongo import MongoClient
from datetime import datetime
import os

def get_url_history(url):
    """
    Retrieves history of a given URL's analysis results.
    
    Args:
        url (str): The URL for which to retrieve the history.
    
    Returns:
        list: A list of dictionaries with each record containing analysis data.
    """
    try:
        # Retrieve all cached results for the specified URL from the database
        history_records = db.analysis_cache.find({"url": url})
        
        # Format the records into a list
        history_list = []
        for record in history_records:
            # Add each record to history_list, removing the internal MongoDB "_id" field
            record.pop("_id", None)
            history_list.append(record)
        
        return history_list
    
    except Exception as e:
        print(f"Error retrieving history for URL {url}: {e}")
        return []

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