import os
import requests
from urllib.parse import urlparse

def get_page_rank(url):
    try:
        domain = urlparse(url).netloc
        api_key = os.getenv('OPENPAGE_API_KEY')
        
        if not api_key:
            return {'page_rank': 0}

        response = requests.get(
            f'https://openpagerank.com/api/v1.0/getPageRank?domains[]={domain}',
            headers={'API-OPR': api_key}
        )
        
        data = response.json()
        
        if data.get('status_code') == 200:
            return {'page_rank': data['response'][0]['page_rank_decimal']}
        
        return {'page_rank': 0}
    except Exception as e:
        print(f'PageRank Error: {str(e)}')
        return {'page_rank': 0}