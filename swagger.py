from flasgger import Swagger
import os

from setup_public_ip import get_public_ip

def init_swagger(app):
    """Initialize Swagger with the given Flask app."""
    public_ip = get_public_ip() # os.getenv("PUBLIC_IP", "127.0.0.1")
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Library API",
            "description": "API for managing a library of books.",
            "version": "1.0.0"
        },
        "host": f"{public_ip if public_ip else '127.0.0.1'}:80",  # Use the public IP from environment
        "basePath": "/",
        "securityDefinitions": {
            "APIKeyHeader": {
                "type": "apiKey",
                "name": "X-API-Key",
                "in": "header",
                "description": "API key required for authentication"
            }
        },
        "security": [
            {"APIKeyHeader": []}
        ]
    }
    return Swagger(app, template=swagger_template, swagger_ui="/docs")
