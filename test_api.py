import unittest
from main import app, db, Book

class TestBookAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_book(self):
        response = self.app.post('/api/books', json={
            "title": "Test Book",
            "author": "Author Name",
            "isbn": "1234567890123",
            "publish_date": "2024-01-01"
        }, headers={"X-API-Key": "fake-key"})
        self.assertEqual(response.status_code, 201)

    def test_get_books(self):
        response = self.app.get('/api/books', headers={"X-API-Key": "fake-key"})
        self.assertEqual(response.status_code, 200)

    def test_invalid_auth(self):
        response = self.app.get('/api/books', headers={"X-API-Key": "invalid-api-key"})
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
