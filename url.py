import requests
from urllib.parse import urlparse, parse_qs

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50)
session.mount("https://", adapter)

def check_single_code(sessionurl, code):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        }
        
        start_url = f'{sessionurl}'
        
        response = session.get(start_url, headers=headers)
        
        redirect_url = response.url
        #print(redirect_url)
        
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        
        if 'sessionId' in query_params:
            session_id = query_params['sessionId'][0]
        else:
            session_id = None
            
        headers = {
            'content-type': 'application/json',
            'referer': f'{redirect_url}',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        }
        
        params = {
            'lang': 'en_US',
        }
        
        json_data = {
            'accessCode': f'{code}',
            'sessionId': f'{session_id}',
            'apiVersion': 1,
        }
        
        response = session.post('https://portal-as.ruijienetworks.com/api/auth/voucher/', params=params, headers=headers, json=json_data)
        return response.text
        
    except Exception as e:
        return "error"