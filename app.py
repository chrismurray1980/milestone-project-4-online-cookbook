import os
from flask import Flask, render_template, redirect, request, url_for
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from ming import Session, create_datastore
from ming.datastore import DataStore
from models import add_recipe, add_user
from ming.odm import ThreadLocalODMSession
from ming import mim

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'onlineCookbook'

Testing_configuration=False

if not Testing_configuration:
    app.config["MONGO_URI"]=os.getenv("MONGO_URI",'mongodb://localhost')
else:
    app.config["MONGO_URI"] = 'mim://localhost/test'

session = ThreadLocalODMSession(bind=create_datastore(app.config["MONGO_URI"] ) )

@app.route('/')
def get_recipes():
    
    return render_template("index.html", recipes=session.db.users.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
    
    