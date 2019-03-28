from flask import Flask, render_template, redirect, request, url_for
from bson.objectid import ObjectId
from models import recipes, users
from ming import mim, create_datastore
from ming.odm import ThreadLocalODMSession
from ming.base import Cursor
import os

def database_config_setup(filename):
    if filename == "__main__":
        database_config=os.getenv("MONGO_URI",'mongodb://localhost')
    else:
        database_config='mim://localhost/test'
    return database_config

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'onlineCookbook'
app.config["MONGO_URI"]=database_config_setup(__name__)    
session = ThreadLocalODMSession(bind=create_datastore(app.config["MONGO_URI"] ) )

@app.route('/')
def get_recipes():
    
    return render_template("index.html", users=session.db.users.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True)