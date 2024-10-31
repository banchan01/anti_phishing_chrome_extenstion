import requests
from bs4 import BeautifulSoup

def get_google_index(url):
    try:
        search_url = f'https://www.google.com/search?q=site:{url}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if any results found
        results = soup.find('div', {'id': 'result-stats'})
        is_indexed = results is not None
        
        return {
            'url': url,
            'is_indexed': is_indexed,
            'total_results': results.text if results else '0'
        }
    except Exception as e:
        print(f'Google Index Error: {str(e)}')
        return {'url': url, 'is_indexed': False, 'total_results': '0'}