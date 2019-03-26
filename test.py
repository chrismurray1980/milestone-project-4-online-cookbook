from flask_testing import TestCase
from app import app, session 
import unittest
from models import add_recipe, add_user
from config import test_config
import unittest

if test_config:
    class FlaskTestCase(TestCase):
        
        def create_app(self):
            return app
            
        def setUp(self):
            session.db.users.insert_one(add_user.make(dict(author='rrrr', name='ttttt')))
            session.db.users.insert_one(add_user.make(dict(author='hhhhh', name='gggg')))
            
        def tearDown(self):
            session.clear()
    
        def test_index_loads(self):
            #Ensure index page loads correctly.
            response = self.client.get('/', follow_redirects=True)
            self.assert200(response)
            self.assertTemplateUsed('index.html')
            self.assertIn(b'knod', response.data)
            self.assertEqual(session.db.users.count(), 2)
        
    if __name__ == '__main__':
        unittest.main()