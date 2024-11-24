import os
from flask import request, jsonify
from functools import wraps

API_KEY = os.getenv("API_KEY", "fake-key") # fake-key for debugging purposes

# Decorator to require API key for a route
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key == API_KEY:
            return f(*args, **kwargs)
        return jsonify({"error": "Invalid API key"}), 401
    return decorated
