import os
from flask import Flask, render_template, redirect, request, url_for
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
#from jsonschema import validate

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'onlineCookbook'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')
"""mongo=PyMongo(app)

schema = {
    "type" : "object",
     "properties" : {
         "author" : {"type" : "string"},
        "name" : {"type" : "string"} }}

#mydict = {'author':'aaaaaaa', 'name':'This is a page'}"""

from ming import Session, create_datastore
#from ming import Document, Field, schema
from ming.datastore import DataStore
from models import add_recipe
session = Session(create_datastore(app.config["MONGO_URI"]))




page = add_recipe.make(dict(author='MyPage', name='dumb'))

@app.route('/')
def get_recipes():
    #instance={"author" : "Eggs", "name" : 'jhvjhvjhvjhvjhv'}
    #print(validate(instance, schema=schema))
    #session.db.recipes.insert_one(page)
    session.db.recipes.insert_one(page)
    return render_template("index.html", recipes=session.db.recipes.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
                port=int(os.environ.get('PORT')),
    debug=True)