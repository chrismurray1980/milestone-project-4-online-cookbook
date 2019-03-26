from flask import Flask, render_template, redirect, request, url_for
from bson.objectid import ObjectId
from models import add_recipe, add_user
from ming import mim, create_datastore
from ming.odm import ThreadLocalODMSession
from config import connection_config
import os

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'onlineCookbook'
app.config["MONGO_URI"]=connection_config
session = ThreadLocalODMSession(bind=create_datastore(app.config["MONGO_URI"] ) )

@app.route('/')
def get_recipes():
    return render_template("index.html", recipes=session.db.users.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True)
    
    