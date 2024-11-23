import os
from flask import request, jsonify
from functools import wraps

# Set API_KEY from environment variable or default to "fake-key"
API_KEY = os.getenv("API_KEY", "fake-key")
print(f"====================> {API_KEY}")
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == API_KEY:
            return f(*args, **kwargs)
        return jsonify({"error": "Invalid API key"}), 401
    return decorated
