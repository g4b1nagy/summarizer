# These tests are by no means comprehensive.
# Also, it would be preferable to use Flask's Werkzeug test client
# which would allow for the creation of the DB as a tempfile in setUp,
# allowing tests to run in paralel, each on its own DB.

import unittest

import requests


BASE_URL = 'http://localhost:5000'


class TestApi(unittest.TestCase):

    def setUp(self):
        with open('test_document_1.txt') as f:
            self.text_1 = f.read()
        with open('test_document_2.txt') as f:
            self.text_2 = f.read()

    def test_post_application_json(self):
        """Create and retrieve a new document using Content-Type application/json."""

        data = {'text': self.text_1}
        response = requests.post(f'{BASE_URL}/document/', json=data)
        self.assertEqual(response.status_code, 200)
        document_id = response.json().get('document_id')
        response = requests.get(f'{BASE_URL}/document/{document_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('text'), self.text_1)

    def test_post_application_x_www_form_urlencoded(self):
        """Create and retrieve a new document using Content-Type application/x-www-form-urlencoded."""

        data = {'text': self.text_1}
        response = requests.post(f'{BASE_URL}/document/', data=data)
        self.assertEqual(response.status_code, 200)
        document_id = response.json().get('document_id')
        response = requests.get(f'{BASE_URL}/document/{document_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('text'), self.text_1)

    def test_put(self):
        """Create a new document, then update its text."""

        data = {'text': self.text_1}
        response = requests.post(f'{BASE_URL}/document/', json=data)
        self.assertEqual(response.status_code, 200)
        document_id = response.json().get('document_id')
        data = {'text': self.text_2}
        response = requests.put(f'{BASE_URL}/document/{document_id}', json=data)
        self.assertEqual(response.status_code, 200)
        response = requests.get(f'{BASE_URL}/document/{document_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('text'), self.text_2)

    def test_delete(self):
        """Create a new document, then delete it."""

        data = {'text': self.text_1}
        response = requests.post(f'{BASE_URL}/document/', json=data)
        self.assertEqual(response.status_code, 200)
        document_id = response.json().get('document_id')
        response = requests.delete(f'{BASE_URL}/document/{document_id}')
        self.assertEqual(response.status_code, 200)
        response = requests.get(f'{BASE_URL}/document/{document_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
