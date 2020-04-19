import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from manage import app
from app.models import setup_db, User, Post

jwt_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImY5ZDk3YjRjYWU5MGJjZDc2YWViMjAwMjZmNmI3NzBjYWMyMjE3ODMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiODI4NzU5Mjc4OTAwLThtcW9wOTEyc25zdDRsNjZ2MGF1aDZjOTU4dG4xc2hmLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiODI4NzU5Mjc4OTAwLThtcW9wOTEyc25zdDRsNjZ2MGF1aDZjOTU4dG4xc2hmLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTAzNDk5NDIyODgxMTY5MDMyMTc1IiwiZW1haWwiOiJqaWJpbi50aG9tYXMyNzA2QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoibE9KZHR5eWNYdFJfM1BwLXZJVzM1QSIsIm5hbWUiOiJKaWJpbiBUaG9tYXMiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EtL0FPaDE0R2g3ZmhQdWtLM1dzQi1nZkVNYkNvQnhOMXpaUkVuSGdRaGpxY3hhPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkppYmluIiwiZmFtaWx5X25hbWUiOiJUaG9tYXMiLCJsb2NhbGUiOiJlbi1HQiIsImlhdCI6MTU4NzI5NTU3MCwiZXhwIjoxNTg3Mjk5MTcwLCJqdGkiOiIwMjAzOGViMzBhYTAzMzk3MjcwOWJjNGFiOWRkMTA4MjViMTJmZTVhIn0.J_mvB_v0Jp8sh7E5Ged3DzDYZ69R15wfDZthEZzh4QFA0_Mr5Lz_C4GATlCVoZcjRjOgIZl4KZsUUyLP1ncTX6hgnAxOTvdeR9AZx0JPZxGZfIPS_w0GKICZ7qDpGynPyrG-DtnsTuQCZfZkWPM-hGA23mJoO9wLzlqZXqxqdTuIsA8KrY0-zn6LYf5MJTsRkJCwia_DYMCgTmoiLfd7ELrlSlgANK2lsM_ebaMAMrzeTQ8IdBs6aoorOQKK-wW706-0jWi2yUGf4zFNzFuioA9ZZpv8sxNK0RJoNykVDvZoD4pohzZ4b51p2-VRXaGRdCR1WZVIzFeAUjJ6y0LGNg'


class BlogTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': jwt_token}
        setup_db(app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_article(self):
        res = self.client().get('/posts')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['posts']), 2)

    def test_get_featured_article(self):
        res = self.client().get('/posts?type=featured')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        for post in data['posts']:
            self.assertEqual(post['is_featured'], True)

    def test_get_individual_article(self):
        res = self.client().get('/post?url=nextjs')
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/post')
        self.assertEqual(res.status_code, 400)

        res = self.client().get('/post?url=post-not-available')
        self.assertEqual(res.status_code, 404)

    def test_post_article(self):
        res = self.client().post('/post',
                                 json={'user_id': '2', 'title': 'new test post',
                                       'url_slug': 'new-test-post', 'is_publish': True, 'body': 'test post'},
                                 headers=self.headers)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/post',
                                 json={'user_id': '2',
                                       'title': 'new test post'},
                                 headers=self.headers)
        self.assertEqual(res.status_code, 404)

        res = self.client().post('/post',
                                 json={'user_id': '2',
                                       'title': 'new test post'})
        self.assertEqual(res.status_code, 401)

    def test_update_article(self):
        res = self.client().patch('/post',
                                  json={'id': 5, 'user_id': '2', 'title': 'new test post',
                                        'url_slug': 'new-test-post', 'is_publish': True, 'body': 'test post update'},
                                  headers=self.headers)
        self.assertEqual(res.status_code, 200)

        res = self.client().patch('/post',
                                  json={'user_id': '2',
                                        'title': 'new test post'},
                                  headers=self.headers)
        self.assertEqual(res.status_code, 404)

        res = self.client().patch('/post',
                                  json={'user_id': '2',
                                        'title': 'new test post'})
        self.assertEqual(res.status_code, 401)

    def test_delete_article(self):
        res = self.client().delete('/post/2', headers=self.headers)
        self.assertEqual(res.status_code, 200)

        res = self.client().delete('/post/1000', headers=self.headers)
        self.assertEqual(res.status_code, 404)

        res = self.client().delete('/post/3')
        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
