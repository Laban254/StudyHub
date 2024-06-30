import requests
import logging

logger = logging.getLogger(__name__)

def log_request(url):
    try:
        response = requests.get(url)
        logger.info(f"Request to {url} completed with status code {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"Request to {url} failed: {e}")
