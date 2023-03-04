import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_actors_page(self):
        response = self.app.get('/actors')
        self.assertEqual(response.status_code, 200)

    def test_valid_movie_detail_page(self):
        response = self.app.get('/movie/1')
        self.assertEqual(response.status_code, 200)

    def test_invalid_movie_detail_page(self):
        response = self.app.get('/movie/999')
        self.assertEqual(response.status_code, 404)

    def test_404_error_page(self):
        response = self.app.get('/non-existent-url')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
