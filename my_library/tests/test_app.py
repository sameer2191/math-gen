# tests/test_app.py
import unittest
from my_library.app import create_app
from my_library.db import initialize_database

class MyLibraryTestCase(unittest.TestCase):
    def setUp(self):
        self.config = {
            'FLASK_SECRET_KEY': 'your_flask_secret_key',
            'UPLOAD_FOLDER': 'path_to_upload_folder',
            'JSON_FOLDER': 'path_to_json_folder',
            'api_key': 'your_openai_api_key',
            'instructions': 'your_instructions'
        }
        self.app = create_app(self.config)
        self.client = self.app.test_client()

    def test_upload_form(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_ask_question(self):
        response = self.client.post('/ask', data=json.dumps({'question': 'What is 2 + 2?'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
