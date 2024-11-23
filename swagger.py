from flasgger import Swagger
import os
from setup_public_ip import get_public_ip

def init_swagger(app):
    """Initialize Swagger with the given Flask app."""
    # Try to get the public IP from the function or fallback to environment variable/default
    public_ip = get_public_ip() or os.getenv("PUBLIC_IP", "127.0.0.1")

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Library API",
            "description": "API for managing a library of books.",
            "version": "1.0.0"
        },
        "host": f"{public_ip}:80",  # Use the public IP dynamically
        "basePath": "/api",  # Set base path for API
        "tags": [  # Define API tags
            {
                "name": "Books",
                "description": "Operations related to managing books"
            }
        ],
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

    # Set Flask config for Swagger UI path
    app.config['SWAGGER'] = {
        'uiversion': 3,
    }

    # Initialize Swagger and set the UI path to /api/docs
    swagger = Swagger(app, template=swagger_template)
    
    # Configure Swagger UI to use the /api/docs path
    app.config['SWAGGER_UI_PATH'] = '/api/docs'  # This is where the Swagger UI will be served
    
    return swagger
