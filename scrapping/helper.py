import requests
import numpy as np
import random

# Helper function to fetch and handle API response
def fetch_api_data(base_url, year, start, limit, api_key):
    params = {
        'year': year,
        'start': start,
        'limit': limit
    }
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {base_url}, status code: {response.status_code}")
        return None
