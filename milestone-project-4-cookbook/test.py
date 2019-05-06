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
        session.db.recipes.delete_many({})
        session.clear()

    def test_get_recipes(self):
        #Ensure index page loads
        response = self.client.get('/', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertIn(b'test this document', response.data)
        self.assertEqual(session.db.recipes.count(), 1)

    def test_add_recipe(self):
        #Ensure add_recipe page loads correctly.
        response = self.client.get('/add_recipe', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('add_recipe.html')
        
    def test_insert_recipe(self): 
        #Ensure insert recipe works correctly and index page is then rendered
        objectId = ObjectId('0123456789ab0123456789ac')
        session.db.recipes.insert_one(recipes.make(dict(_id=objectId, recipeName='test insert document')))
        response = self.client.get('/', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertIn(b'test insert document', response.data)
        self.assertEqual(session.db.recipes.count(), 2)
        
    def test_edit_delete_recipe(self):
        #Ensure edit_delete_recipe page loads with correct recipe_id
        response = self.client.get('/edit_delete_recipe/0123456789ab0123456789ab', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('edit_delete_recipe.html')
        self.assertIn(b'test this document', response.data)
    
    def test_update_recipe(self):
        #Ensure recipe is updated and index page is rendered
        session.db.recipes.update_one( {'_id': ObjectId('0123456789ab0123456789ab')}, {"$set": {'recipeName':'This has been updated'}}, upsert=True)
        response = self.client.get('/', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertIn(b'This has been updated', response.data)
        self.assertEqual(session.db.recipes.count(), 1)
    
    def test_show_recipe(self):
        #Ensure show_recipe page loads and shows correct recipe.
        response = self.client.get('/show_recipe/0123456789ab0123456789ab', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('show_recipe.html')
        self.assertIn(b'test this document', response.data)
        
    def test_delete_recipe(self):
        session.db.recipes.delete_one({'_id': ObjectId('0123456789ab0123456789ab')})
        response = self.client.get('/', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertEqual(session.db.recipes.count(), 0)
        
    def test_favourites_loads(self):
        #Ensure favourites page loads correctly.
        response = self.client.get('/favourites', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('favourites.html')
        
if __name__ == '__main__':
    unittest.main()