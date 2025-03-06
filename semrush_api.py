# semrush_api.py
import requests
from config import SEMRUSH_API_KEY, SEMRUSH_DATABASE

BASE_URL = "https://api.semrush.com"

def get_serp_data(keyword):
    """
    Fetches the top SERP results for a given keyword.
    """
    params = {
        "type": "phrase_organic",
        "key": SEMRUSH_API_KEY,
        "phrase": keyword,
        "database": SEMRUSH_DATABASE,
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.text  # SEMRush API returns CSV format by default
    else:
        return {"error": f"Failed to fetch data: {response.status_code}"}

def get_keyword_volume(keyword):
    """
    Fetches search volume data for a given keyword.
    """
    params = {
        "type": "phrase_this",
        "key": SEMRUSH_API_KEY,
        "phrase": keyword,
        "database": SEMRUSH_DATABASE,
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.text
    else:
        return {"error": f"Failed to fetch keyword volume: {response.status_code}"}
