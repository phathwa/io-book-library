import os
import json
from flask import request, jsonify
from functools import wraps

api_key_env = os.getenv("API_KEY", "fake-key")

try:
    api_key_dict = json.loads(api_key_env)
    api_key_value = api_key_dict.get("x-api-key", "fake-key")
except json.JSONDecodeError:
    api_key_value = api_key_env

print(f"====================> {api_key_value}")

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == api_key_value:
            return f(*args, **kwargs)
        return jsonify({"error": "Invalid API key"}), 401
    return decorated
