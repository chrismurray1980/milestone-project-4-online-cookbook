"""from flask_testing import TestCase
from app import app
import unittest


class FlaskTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

if __name__ == '__main__':
    unittest.main()"""
    
from flask import Flask
from flask_testing import TestCase
import unittest

class MyTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
        
def test_index_loads(self):
        """Ensure index page loads correctly."""
        response = self.client.get('/', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertIn(b'Walk the dog', response.data)
        self.assertEqual(len(self.get_context_variable('todos')), 2)


if __name__ == '__main__':
        unittest.main()