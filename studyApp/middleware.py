# your_app/middleware.py

import logging

logger = logging.getLogger(__name__)

class LogRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request details
        logger.info(f"Incoming request: {request.method} {request.get_full_path()}")
        response = self.get_response(request)
        return response

