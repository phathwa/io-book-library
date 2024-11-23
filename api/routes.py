from flask import Blueprint, request, jsonify
from .models import Book
from . import db
from .auth import require_api_key
from .helpers import validate_book_data
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/books', methods=['GET'])
def get_books():
    """Get all books.
    ---
    tags:
      - Books
    responses:
      200:
        description: A list of all books
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              author:
                type: string
              isbn:
                type: string
              publish_date:
                type: string
                format: date
              created_at:
                type: string
                format: date-time
              updated_at:
                type: string
                format: date-time
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


@api_bp.route('/books/<int:id>', methods=['GET'])
@require_api_key
def get_book(id):
    """Get a specific book by ID.
    ---
    tags:
      - Books
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the book
    responses:
      200:
        description: Details of a specific book
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            author:
              type: string
            isbn:
              type: string
            publish_date:
              type: string
              format: date
            created_at:
              type: string
              format: date-time
            updated_at:
              type: string
              format: date-time
      404:
        description: Book not found
        schema:
          type: object
          properties:
            error:
              type: string
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

@api_bp.route('/books', methods=['POST'])
@require_api_key
def add_book():
    """Add a new book.
    ---
    tags:
      - Books
    parameters:
      - name: body
        in: body
        required: true
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
              format: date
    responses:
      201:
        description: Book added successfully
        schema:
          type: object
          properties:
            message:
              type: string
            id:
              type: integer
      400:
        description: Invalid input data
        schema:
          type: object
          properties:
            error:
              type: string
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

@api_bp.route('/books/<int:id>', methods=['PUT'])
@require_api_key
def update_book(id):
    """Update an existing book.
    ---
    tags:
      - Books
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the book to update
      - name: body
        in: body
        required: true
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
              format: date
    responses:
      200:
        description: Book updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Invalid input data
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Book not found
        schema:
          type: object
          properties:
            error:
              type: string
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

@api_bp.route('/books/<int:id>', methods=['DELETE'])
@require_api_key
def delete_book(id):
    """Delete a book by ID.
    ---
    tags:
      - Books
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the book to delete
    responses:
      200:
        description: Book deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Book not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200
