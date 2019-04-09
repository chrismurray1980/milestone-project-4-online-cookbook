from flask_testing import TestCase
from app import app, session
from models import recipes, users
import unittest

class FlaskTestCase(TestCase):
    
    def create_app(self):
        app.config['TESTING'] = True
        return app
    
    def setUp(self):
        pass
        
    def tearDown(self):
        session.clear()

    def test_index_loads(self):
        #session.db.users.insert_one(users.make(dict(user_name='AAAAA', email='BBBBB')))
        session.db.recipes.insert_one(recipes.make(dict(recipeName='CCCCC', recipeAuthor='DDDDD')))
        #session.db.users.insert_one(users.make(dict(user_name='C', email='DD')))
        #Ensure index page loads correctly.
        response = self.client.get('/', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertIn(b'CCCCC', response.data)
        self.assertEqual(session.db.recipes.count(), 1)
    
    def test_edit_delete_recipe_loads(self):
        #Ensure edit_delete_recipe page loads correctly.
        response = self.client.get('/edit_delete_recipe', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('edit_delete_recipe.html')
    
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
        response = self.client.get('/show_recipe', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('show_recipe.html')
        
if __name__ == '__main__':
    unittest.main()