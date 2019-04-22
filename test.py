from flask_testing import TestCase
from app import app, session
from models import recipes, users
import unittest
from bson.objectid import ObjectId

class FlaskTestCase(TestCase):
    
    def create_app(self):
        app.config['TESTING'] = True
        return app
    
    def setUp(self):
        objectId = ObjectId('0123456789ab0123456789ab')
        session.db.recipes.insert_one(recipes.make(dict(_id=objectId, recipeName='test this document')))
        
    def tearDown(self):
        objectId = ObjectId('0123456789ab0123456789ab')
        session.db.recipes.delete_one({"_id":objectId})
        session.clear()

    def test_index_loads(self):
        #Ensure index page loads correctly.
        response = self.client.get('/', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertIn(b'test this', response.data)
        self.assertEqual(session.db.recipes.count(), 1)
    
    def test_edit_delete_recipe_loads(self):
        #Ensure edit_delete_recipe page loads correctly.
        response = self.client.get('/edit_delete_recipe/0123456789ab0123456789ab', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('edit_delete_recipe.html')
        self.assertIn(b'test this document', response.data)
    
    def test_add_recipe_loads(self):
        #Ensure add_recipe page loads correctly.
        response = self.client.get('/add_recipe', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('add_recipe.html')
        
    def test_favourites_loads(self):
        #Ensure favourites page loads correctly.
        response = self.client.get('/favourites', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('favourites.html')
    
    def test_show_recipe_loads(self):
        #Ensure show_recipe page loads correctly.
        response = self.client.get('/show_recipe/0123456789ab0123456789ab', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('show_recipe.html')
        
if __name__ == '__main__':
    unittest.main()