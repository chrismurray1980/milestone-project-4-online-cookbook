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
    database_config=os.getenv("MONGO_URI",'mongodb://localhost') if filename == "__main__" else 'mim://localhost/test'
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
    recipes=recipes_collection.find({"$text": {"$search": search_content}}, 
                                    {'_txtscr': {'$meta': 'textScore'}}).sort([('_txtscr', {'$meta':'textScore'})])
    return render_template("search_results.html", recipes=recipes)

@app.route('/advanced_search_results', methods=['POST'])
def advanced_search_results():
    """Return recipes from mongodb based on advanced search fields"""
    advanced_search_list=advanced_search_query_formatting(field_list[6:16])
    recipes=recipes_collection.find({"$and": advanced_search_list}).sort([('recipeUpvotes', -1)]).limit( 10 )
    return render_template("search_results.html", recipes=recipes)
    
@app.route('/add_recipe')
def add_recipe():
    """Display add recipe page"""
    return render_template("add_recipe.html")
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    """Insert recipe to db and display index.html"""
    preparation_time=request.form.get('recipePreparationTime')
    cooking_time=request.form.get('recipeCookingTime')
    servings=request.form.get('recipeServings')
    
    preparation_time=int(preparation_time) if preparation_time.isdigit()==True else 0
    cooking_time=int(cooking_time) if cooking_time.isdigit()==True else 0
    servings=int(servings) if servings.isdigit()==True else 0
    
    recipes_collection.insert_one({
        'recipeName':request.form.get('recipeName'),
        'recipeAuthor':request.form.get('recipeAuthor'),
        'recipeCuisine':request.form.get('recipeCuisine'),
        'recipeCountryOfOrigin':request.form.get('recipeCountryOfOrigin'),
        'recipeMealTime': request.form.get('recipeMealTime'),
        'recipeServings': servings,
        'recipeDifficulty': request.form.get('recipeDifficulty'),
        'recipePreparationTime': preparation_time,
        'recipeCookingTime': cooking_time,
        'recipeAllergen': request.form.get('recipeAllergen').split(','),
        'recipeMainIngredient': request.form.get('recipeMainIngredient'),
        'recipeIngredients': request.form.get('recipeIngredients'),
        'recipeInstructions': request.form.get('recipeInstructions'),
        'recipeDietary': request.form.get('recipeDietary').split(','),
        'recipeUpvotes':0,
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
    preparation_time=request.form.get('recipePreparationTime')
    cooking_time=request.form.get('recipeCookingTime')
    servings=request.form.get('recipeServings')
    
    preparation_time=int(preparation_time) if preparation_time.isdigit()==True else 0
    cooking_time=int(cooking_time) if cooking_time.isdigit()==True else 0
    servings=int(servings) if servings.isdigit()==True else 0
    dietary=request.form.get('recipeDietary')   
    #dietary=dietary.split(',')
    print(dietary)
    
    recipes_collection.update_one( {'_id': ObjectId(recipe_id)}, {"$set": {
        'recipeName':request.form.get('recipeName'),
        'recipeAuthor':request.form.get('recipeAuthor'),
        'recipeCuisine':request.form.get('recipeCuisine'),
        'recipeCountryOfOrigin':request.form.get('recipeCountryOfOrigin'),
        'recipeMealTime': request.form.get('recipeMealTime'),
        'recipeServings': servings,
        'recipeDifficulty': request.form.get('recipeDifficulty'),
        'recipePreparationTime': preparation_time,
        'recipeCookingTime': cooking_time,
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

field_list=['recipeUpvotes', 'recipeName', 'recipeAuthor', 'recipeIngredients', 'recipeInstructions',
            'recipeImageLink', 'recipeCuisine', 'recipeCountryOfOrigin', 'recipeMealTime', 'recipeServings',
            'recipeDifficulty', 'recipePreparationTime', 'recipeCookingTime', 'recipeAllergen', 'recipeDietary',
            'recipeMainIngredient']

select_list=field_list[6:16]   
print(field_list[6:16])
        
def advanced_search_query_formatting(list):
    """Obtain input values for select boxes and append to list for advanced search query"""
    search_list=[]
    for value in list:
        if request.form.get(value) != '':
            if value =='recipeAllergen' or value =='recipeDietary':
                value_text = request.form.get(value)
                value_split_text = value_text.split(', ')
                search_subset=[]
                for i in value_split_text:
                    search_subset.append(i)
                search_list.append({value : { '$in': search_subset} })  
            elif value=='recipePreparationTime' or value=='recipeCookingTime' or value=='recipeServings':
                if request.form.get(value).isdigit()==True:
                    search_list.append({value: { '$lte': int(request.form.get(value))} })
            else:
                search_list.append({value : request.form.get(value)})
    return search_list
       
def insert_update_db_format(list):
    """Construct format of insert or update to be sent to db"""
    field_input_dict={}
    for field in list:
        if field =='recipeAllergen' or field =='recipeDietary':
            field_input_dict[field] = request.form.get(field).split(',')
        elif field=='recipePreparationTime' or field=='recipeCookingTime' or field=='recipeServings':
            field_value = request.form.get(field)
            field_input_dict[field] = int(field_value) if field_value.isdigit()==True else 0
        elif field =='recipeUpvotes' in list:
            field_input_dict[field] = 0
        else:
            field_value = request.form.get(field)
    return field_input_dict         
     
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True)
