from flask_testing import TestCase
from app import app, session
from models import add_recipe, add_user
import unittest

class FlaskTestCase(TestCase):
    
    def create_app(self):
        app.config['TESTING'] = True
        return app
    
    def setUp(self):
        session.db.users.insert_one(add_user.make(dict(author='AAAAA', name='BBBBB')))
        session.db.users.insert_one(add_user.make(dict(author='CCCCC', name='DDDDD')))
        
    def tearDown(self):
        session.clear()

    def test_index_loads(self):
        #Ensure index page loads correctly.
        response = self.client.get('/', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertIn(b'knuckle', response.data)
        self.assertEqual(session.db.users.count(), 2)
    
if __name__ == '__main__':
    unittest.main()