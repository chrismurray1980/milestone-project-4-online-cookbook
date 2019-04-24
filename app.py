from flask import Flask, render_template, redirect, request, url_for
from bson.objectid import ObjectId
from models import recipes, users
from ming import mim, create_datastore
from ming.odm import ThreadLocalODMSession, Mapper
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
    return render_template("index.html", recipes=session.db.recipes.find())

Mapper.ensure_all_indexes()
session.db.recipes.create_index([("$**","text")])
#session.db.recipes.drop_index("$**_text")

@app.route('/search_results', methods=['POST'])
def search_results():
    search_content=request.form.get('searchContent')
    return render_template("search_results.html", recipes=session.db.recipes.find({"$text": {"$search": search_content}}))

    
@app.route('/add_recipe')
def add_recipe():
    return render_template("add_recipe.html")
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
   session.db.recipes.insert_one(recipes.make(request.form.to_dict()))
   return redirect(url_for('get_recipes'))

@app.route('/edit_delete_recipe/<recipe_id>')
def edit_delete_recipe(recipe_id):
    return render_template("edit_delete_recipe.html", recipe=session.db.recipes.find_one({"_id": ObjectId(recipe_id)}))
    
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    session.db.recipes.update_one( {'_id': ObjectId(recipe_id)}, {"$set": 
    {
        'recipeName':request.form.get('recipeName'),
        'recipeAuthor':request.form.get('recipeAuthor'),
        'recipeCuisine':request.form.get('recipeCuisine'),
        'recipeCountryOfOrigin':request.form.get('recipeCountryOfOrigin'),
        'recipeMealTime': request.form.get('recipeMealTime'),
        'recipeServings': request.form.get('recipeServings'),
        'recipeDifficulty': request.form.get('recipeDifficulty'),
        'recipePreparationTime': request.form.get('recipePreparationTime'),
        'recipeCookingTime': request.form.get('recipeCookingTime'),
        'recipeAllergen': request.form.get('recipeAllergen'),
        'recipeMainIngredient': request.form.get('recipeMainIngredient'),
        'recipeIngredients': request.form.get('recipeIngredients'),
        'recipeInstructions': request.form.get('recipeInstructions'),
        'recipeDietary': request.form.get('recipeDietary'),
        'recipeImageLink': request.form.get('recipeImageLink')
    }}, upsert=True)
    return redirect(url_for('get_recipes'))

@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    return render_template("show_recipe.html", recipe=session.db.recipes.find_one({"_id": ObjectId(recipe_id)}))

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    session.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))

@app.route('/favourites')
def favourites():
    return render_template("favourites.html") 

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True)
    