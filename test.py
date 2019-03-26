from flask_testing import TestCase
from app import app, session, get_recipes
import unittest
from ming import Session, create_datastore
from models import add_recipe, add_user
from ming import mim
from ming.datastore import DataStore
import unittest
import os
from ming.odm import ThreadLocalODMSession


class FlaskTestCase(TestCase):
    
    def create_app(self):
        app.config["MONGO_URI"] = 'mim://localhost/test'
        session = ThreadLocalODMSession(bind=create_datastore(app.config["MONGO_URI"] ) )
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
        self.assertIn(b'rrrr', response.data)
        self.assertEqual(session.db.users.count(), 2)
    
if __name__ == '__main__':
    unittest.main()