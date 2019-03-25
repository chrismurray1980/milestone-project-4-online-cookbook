from flask_testing import TestCase
from app import app, mongo, get_recipes
import unittest
import os
from flask_pymongo import PyMongo

app.config["MONGO_DBNAME"] = 'onlineCookbook'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)

coll = mongo.db.recipes

documents = coll.find()

for doc in documents:
    print(doc)

class recipe:
  def __init__(self, author, name, countryOfOrigin, cuisine, mealTime):
    self.author=author
    self.name = name
    self.countryOfOrigin = countryOfOrigin
    self.cuisine = cuisine
    self.mealTime = mealTime

class FlaskTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config["MONGO_URI"] ='mongodb:///:memory:'
        recipe("chris murray", "chicken curry", "India", "Indian", "Dinner")
        return app
        
    def test_index_rendered(self):
        """Ensure index page loads correctly."""
        response = self.client.get('/', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertIn(b'chris murray', response.data)
        self.assertEqual(len(self.get_context_variable('recipes')), 2)
        print(response.data)
        
        
if __name__ == '__main__':
    unittest.main() 


