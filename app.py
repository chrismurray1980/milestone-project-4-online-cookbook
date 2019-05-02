import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from ming import mim, create_datastore
from ming.odm import ThreadLocalODMSession, Mapper
from ming.base import Cursor
from models import recipes, users

Mapper.ensure_all_indexes()

def database_config_setup(filename):
    """Configure application to use either mongodb or mongo-in-memory db"""
    if filename == "__main__":
        database_config=os.getenv("MONGO_URI",'mongodb://localhost')
    else:
        database_config='mim://localhost/test'
    return database_config

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'onlineCookbook'
app.config["MONGO_URI"]=database_config_setup(__name__)    
session = ThreadLocalODMSession(bind=create_datastore(app.config["MONGO_URI"] ) )

recipes_collection=session.db.recipes
recipes_collection.drop_index("$**_text")
recipes_collection.create_index([("$**","text")])

@app.route('/')
def get_recipes():
    """Access recipes with largest number of upvotes and display index page"""
    recipes=recipes_collection.find().sort([('recipeUpvotes', -1)]).sort([('recipeUpvotes', -1)]).limit( 5 )
    data=dumps(recipes_collection.find())
    return render_template("index.html", recipes=recipes, data=data)

@app.route('/search_results', methods=['POST'])
def search_results():
    """Display recipes returned from db based on text input"""
    search_content=search_text_formatting('searchContent')
    recipes=recipes_collection.find({"$text": {"$search": 
            search_content}}, {'_txtscr': {'$meta': 'textScore'}}).sort([('_txtscr', {'$meta':'textScore'})])
    return render_template("search_results.html", recipes=recipes)

@app.route('/advanced_search_results', methods=['POST'])
def advanced_search_results():
    """Return recipes from mongodb based on advanced search fields"""
    advanced_search_array=advanced_search_query_formatting(select_array)
    #{"$and": advanced_search_array}
    print(advanced_search_array)
    recipes=recipes_collection.find({"$and": advanced_search_array})
    return render_template("search_results.html", recipes=recipes)
    
@app.route('/add_recipe')
def add_recipe():
    """Display add recipe page"""
    return render_template("add_recipe.html")
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    """Insert recipe to db and display index.html"""
    recipes_collection.insert_one({
        'recipeName':request.form.get('recipeName'),
        'recipeAuthor':request.form.get('recipeAuthor'),
        'recipeCuisine':request.form.get('recipeCuisine'),
        'recipeCountryOfOrigin':request.form.get('recipeCountryOfOrigin'),
        'recipeMealTime': request.form.get('recipeMealTime'),
        'recipeServings': request.form.get('recipeServings'),
        'recipeDifficulty': request.form.get('recipeDifficulty'),
        'recipePreparationTime': request.form.get('recipePreparationTime'),
        'recipeCookingTime': request.form.get('recipeCookingTime'),
        'recipeAllergen': request.form.get('recipeAllergen').split(','),
        'recipeMainIngredient': request.form.get('recipeMainIngredient'),
        'recipeIngredients': request.form.get('recipeIngredients'),
        'recipeInstructions': request.form.get('recipeInstructions'),
        'recipeDietary': request.form.get('recipeDietary').split(','),
        'recipeImageLink': request.form.get('recipeImageLink')
    })
    return redirect(url_for('get_recipes'))

@app.route('/edit_delete_recipe/<recipe_id>')
def edit_delete_recipe(recipe_id):
    """Open edit/delete page for specific document"""
    recipe=recipes_collection.find_one({"_id": ObjectId(recipe_id)})
    return render_template("edit_delete_recipe.html", recipe=recipe)
    
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    """Update specific document with form elements"""
    recipes_collection.update_one( {'_id': ObjectId(recipe_id)}, {"$set": {
        'recipeName':request.form.get('recipeName'),
        'recipeAuthor':request.form.get('recipeAuthor'),
        'recipeCuisine':request.form.get('recipeCuisine'),
        'recipeCountryOfOrigin':request.form.get('recipeCountryOfOrigin'),
        'recipeMealTime': request.form.get('recipeMealTime'),
        'recipeServings': request.form.get('recipeServings'),
        'recipeDifficulty': request.form.get('recipeDifficulty'),
        'recipePreparationTime': request.form.get('recipePreparationTime'),
        'recipeCookingTime': request.form.get('recipeCookingTime'),
        'recipeAllergen': request.form.get('recipeAllergen').split(','),
        'recipeMainIngredient': request.form.get('recipeMainIngredient'),
        'recipeIngredients': request.form.get('recipeIngredients'),
        'recipeInstructions': request.form.get('recipeInstructions'),
        'recipeDietary': request.form.get('recipeDietary').split(','),
        'recipeImageLink': request.form.get('recipeImageLink')
    }}, upsert=True)
    return redirect(url_for('get_recipes'))

@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    """Show recipe page of specific document"""
    recipe=recipes_collection.find_one({"_id": ObjectId(recipe_id)})
    return render_template("show_recipe.html", recipe=recipe)

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    """Delete specific document"""
    recipes_collection.delete_one({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))

@app.route('/like_recipe/<recipe_id>')
def like_recipe(recipe_id):
    """Add upvote to document when button clicked"""
    recipes_collection.update( {'_id': ObjectId(recipe_id)}, { '$inc': { 'recipeUpvotes': 1} } )
    recipe=recipes_collection.find_one({"_id": ObjectId(recipe_id)})
    return render_template("show_recipe.html", recipe=recipe)

@app.route('/favourites')
def favourites():
    """Open favourites page"""
    return render_template("favourites.html") 

"""Assisting variables and functions"""

def search_text_formatting(search_text):
    """Correctly format string for text search of entire db"""
    formatted_search_text='\"'+request.form.get(search_text)+'\"'
    return formatted_search_text
    
"""id for input names""" 
select_array=['recipeCuisine', 'recipeCountryOfOrigin', 'recipeMealTime', 'recipeServings', 'recipeDifficulty', 
                  'recipePreparationTime', 'recipeCookingTime', 'recipeAllergen', 'recipeMainIngredient', 'recipeDietary']
                  
def advanced_search_query_formatting(array):
    """obtain input values for select boxes and append to array for advanced search query"""
    search_array=[]
    for value in array:
        if request.form.get(value) != '':
            if value =='recipeAllergen' or value =='recipeDietary':
                value_text = request.form.get(value)
                value_split_text = value_text.split(', ')
                search_subset=[]
                for i in value_split_text:
                    search_subset.append(i)
                search_array.append({value : { '$in': search_subset} })  
            elif value=='recipePreparationTime' and request.form.get(value).isdigit()==True:
                new_value=request.form.get(value)
                print(type(int(new_value)))
                search_array.append({value: { '$lte': int(request.form.get(value))} })
            elif value=='recipeCookingTime' and request.form.get(value).isdigit()==True:
                new_value=request.form.get(value)
                print(type(int(new_value)))
                search_array.append({value: { '$lte': int(request.form.get(value))} })    
            elif value=='recipeServings' and request.form.get(value).isdigit()==True:
                new_value=request.form.get(value)
                print(type(int(new_value)))
                search_array.append({value: { '$lte': int(request.form.get(value))} })    
            else:
                search_array.append({value : request.form.get(value)})
    return search_array
       
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True)
