from flasgger import Swagger

def init_swagger(app):
    """Initialize Swagger with the given Flask app."""
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Library API",
            "description": "API for managing a library of books.",
            "version": "1.0.0"
        },
        "host": "127.0.0.1:80",
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
    return Swagger(app, template=swagger_template)
