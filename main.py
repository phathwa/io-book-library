from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from functools import wraps
from swagger import init_swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Swagger
swagger = init_swagger(app)

# API key for basic authentication
API_KEY = "fake-key"

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
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

# Helper function for input validation
def validate_book_data(data):
    required_fields = ["title", "author", "isbn", "publish_date"]
    for field in required_fields:
        if field not in data:
            return f"Missing field: {field}"
    try:
        datetime.strptime(data['publish_date'], '%Y-%m-%d')  # Validate date format
    except ValueError:
        return "Invalid date format for publish_date. Use YYYY-MM-DD."
    return None

# API Endpoints
@app.route('/api/books', methods=['GET'])
# @require_api_key
def get_books():
    """Fetch all books.
    ---
    responses:
        200:
            description: A list of all books
    """
    books = Book.query.all()
    return jsonify([{
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "publish_date": book.publish_date.strftime('%Y-%m-%d'),
        "created_at": book.created_at,
        "updated_at": book.updated_at
    } for book in books]), 200

@app.route('/api/books/<int:id>', methods=['GET'])
@require_api_key
def get_book(id):
    """Fetch a book by ID.
    ---
    responses:
        200:
            description: Details of a specific book
        404:
            description: Book not found
    """
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "publish_date": book.publish_date.strftime('%Y-%m-%d'),
        "created_at": book.created_at,
        "updated_at": book.updated_at
    }), 200

@app.route('/api/books', methods=['POST'])
@require_api_key
def add_book():
    """Add a new book.
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            isbn:
              type: string
            publish_date:
              type: string
    responses:
        201:
            description: Book created successfully
        400:
            description: Validation error
    """
    data = request.get_json()
    error = validate_book_data(data)
    if error:
        return jsonify({"error": error}), 400

    new_book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data['isbn'],
        publish_date=datetime.strptime(data['publish_date'], '%Y-%m-%d')
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully", "id": new_book.id}), 201

@app.route('/api/books/<int:id>', methods=['PUT'])
@require_api_key
def update_book(id):
    """Update an existing book.
    ---
    parameters:
      - in: path
        name: id
        required: true
        type: integer
      - in: body
        name: body
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            isbn:
              type: string
            publish_date:
              type: string
    responses:
        200:
            description: Book updated successfully
        400:
            description: Validation error
        404:
            description: Book not found
    """
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    if 'title' in data:
        book.title = data['title']
    if 'author' in data:
        book.author = data['author']
    if 'isbn' in data:
        book.isbn = data['isbn']
    if 'publish_date' in data:
        try:
            book.publish_date = datetime.strptime(data['publish_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format for publish_date. Use YYYY-MM-DD."}), 400

    db.session.commit()
    return jsonify({"message": "Book updated successfully"}), 200

@app.route('/api/books/<int:id>', methods=['DELETE'])
@require_api_key
def delete_book(id):
    """Delete a book.
    ---
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
        200:
            description: Book deleted successfully
        404:
            description: Book not found
    """
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200

@app.route('/', methods=['GET'])
def main():
    return {"message": "Visit /apidocs for API documentation"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=80)
