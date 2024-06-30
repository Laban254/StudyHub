import requests
import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Make requests to keep the server alive and log the results'

    def handle(self, *args, **kwargs):
        urls = [
            'https://studyhub-irj2.onrender.com/', 
            'https://ticketingsystem-p5ew.onrender.com/'
        ]
        
        for url in urls:
            try:
                logger.debug(f'Making request to {url}')
                with open('/debug.log', 'a') as f:
                    f.write(f'Cron job executed for {url}\n')  # Write to a temporary debug file
                response = requests.get(url)
                with open('/debug.log', 'a') as f:
                    f.write(f'Request to {url} completed with status code {response.status_code}\n')
                logger.info(f"Request to {url} completed with status code {response.status_code}")
            except requests.RequestException as e:
                with open('/debug.log', 'a') as f:
                    f.write(f'Request to {url} failed: {e}\n')
                logger.error(f"Request to {url} failed: {e}")
