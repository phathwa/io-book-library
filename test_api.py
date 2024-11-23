import unittest
from unittest.mock import patch
from main import app, db

class TestBookAPI(unittest.TestCase):
    def setUp(self):
        """Set up the test client and mock the get_public_ip function."""
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

        # Mocking get_public_ip to return a dummy IP during tests
        patch('setup_public_ip.get_public_ip', return_value='127.0.0.1').start()

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_book(self):
        """Test the addition of a new book."""
        response = self.app.post('/api/books', json={
            "title": "Test Book",
            "author": "Author Name",
            "isbn": "1234567890123",
            "publish_date": "2024-01-01"
        }, headers={"X-API-Key": "fake-key"})
        self.assertEqual(response.status_code, 201)

    def test_get_books(self):
        """Test retrieving the list of books."""
        response = self.app.get('/api/books', headers={"X-API-Key": "fake-key"})
        self.assertEqual(response.status_code, 200)

    def test_invalid_auth(self):
        """Test invalid authentication with the wrong API key."""
        response = self.app.get('/api/books', headers={"X-API-Key": "invalid-api-key"})
        self.assertEqual(response.status_code, 401)

    # Edge Case 1: Retrieving Books When the Database is Empty
    def test_get_books_empty_db(self):
        """Test retrieving books when no books exist in the database."""
        with app.app_context():
            # Ensure database is empty before the test
            db.session.remove()
            db.drop_all()
            db.create_all()

        response = self.app.get('/api/books', headers={"X-API-Key": "fake-key"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])  # Should return an empty list

    # Edge Case 2: Adding a Book with Invalid Data (Malformed ISBN)
    def test_add_book_invalid_data(self):
        """Test adding a book with invalid data (e.g., incorrect ISBN)."""
        response = self.app.post('/api/books', json={
            "title": "Invalid Book",
            "author": "Invalid Author",
            "isbn": "invalidisbn",  # Invalid ISBN format
            "publish_date": "2024-01-01"
        }, headers={"X-API-Key": "fake-key"})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)  # Ensure error is returned

if __name__ == '__main__':
    unittest.main()
