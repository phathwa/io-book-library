import os
from flask import json, request, jsonify
from functools import wraps

# Extract the API_KEY environment variable (with a fallback to "fake-key")
api_key_env = os.getenv("API_KEY", "fake-key")

# If the API_KEY is in JSON format, you can parse it
try:
    api_key_dict = json.loads(api_key_env)
    api_key_value = api_key_dict.get("x-api-key", "fake-key")  # Extract 'x-api-key'
except json.JSONDecodeError:
    api_key_value = api_key_env  # In case the value is not JSON, use the raw value

print(f"====================> {api_key_value}")

# Decorator to require API key for a route
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == api_key_value:  # Use api_key_value here
            return f(*args, **kwargs)
        return jsonify({"error": "Invalid API key"}), 401
    return decorated
