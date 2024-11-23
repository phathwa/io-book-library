# Book Library API

Create a simple REST API for managing a library's book collection using Flask and SQLite/PostgreSQL (candidate's choice).

## Requirements:

1. Create a Flask application with the following endpoints:

- GET /api/books - List all books
- GET /api/books/<id> - Get a specific book
- POST /api/books - Add a new book
- PUT /api/books/<id> - Update a book

2. Database Requirements:

- Books should have the following fields:
  - id (auto-generated)
  - title
  - author
  - isbn
  - publish_date
  - created_at
  - updated_at

3. Additional Requirements:

- Implement proper error handling
- Include input validation
- Write at least 3 unit tests
- Include basic authentication (API key or Basic Auth)
- Document API endpoints

## Starter Code:

Here's some starter code to provide structure:

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# API key for basic authentication
API_KEY = "your-api-key-here"

# Authentication decorator
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == API_KEY:
            return f(*args, **kwargs)
        return jsonify({"error": "Invalid API key"}), 401
    return decorated

# Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# TODO: Implement the following endpoints:
# GET /api/books
# GET /api/books/<id>
# POST /api/books
# PUT /api/books/<id>

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

## Part II - AWS Deployment

Temporarily deploy your solution to your AWS account. Make use of any "infrastructure as code" solutions (CDK, serverless framework, SST Cloudformation etc.).
Include your infrastructure as code solution in the same repository as the service source code.
When making your submission you may be required to demonstrate that you are able to redeploy your solution in your account using your infrastructure as code implementation.

You may make use of any AWS services to deploy your solution.

An architecture diagram is not required but is a bonus.

## Evaluation Criteria:

1. Code Quality:

   - Clean, readable code
   - Proper error handling
   - Good coding practices and patterns

2. API Design:

   - RESTful principles
   - Proper status codes
   - Clear request/response format

3. Database Usage:

   - Proper model design
   - Efficient queries
   - Data validation

4. Testing:

   - Test coverage
   - Test quality
   - Edge cases considered

5. Documentation:

   - Clear API documentation
   - Setup instructions
   - Code comments where necessary

6. AWS Cloud knowledge and execution:
   - Understanding of AWS concepts
   - Sound infrastructure best-practices
   - Infrastructure as code best-practices
   - Usage of environment variables / secrets

## Submission Requirements:

1. Provide the code in a GitHub repository
2. Include a README.md with:
   - Setup instructions
   - API documentation
   - Any assumptions made
   - Choice of database and why
3. Requirements.txt file
4. Unit tests
