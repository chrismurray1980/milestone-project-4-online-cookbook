import os

from flask import Flask, render_template, redirect, request, url_for, jsonify

from bson.objectid import ObjectId

from bson.json_util import dumps

from ming import mim, create_datastore

from ming.odm import ThreadLocalODMSession, Mapper

from ming.base import Cursor

from models import recipes, users


Mapper.ensure_all_indexes()


def database_config_setup( filename ):
    """Configure application to use either mongodb or mongo-in-memory db"""
    
    database_config = os.getenv( 'MONGO_URI', 'mongodb://localhost' ) if filename == '__main__' else 'mim://localhost/test'
   
    return database_config


app = Flask(__name__)

app.config[ 'MONGO_DBNAME' ] = 'onlineCookbook'

app.config[ 'MONGO_URI' ] = database_config_setup( __name__ )

session = ThreadLocalODMSession( bind = create_datastore( app.config[ 'MONGO_URI' ] ) )


recipes_collection = session.db.recipes

recipes_collection.drop_index( '$**_text' )

recipes_collection.create_index( [ ( '$**' , 'text' ) ] )



@app.route( '/' )

def get_recipes():
    
    """Access recipes with largest number of upvotes and display index page""" 
    
    try:
        
        recipes = recipes_collection.find().sort( [ ( 'recipeUpvotes' , -1 ) ] ).sort( [ ( 'recipeUpvotes' , -1 ) ] ).limit( 5 )
        
        data = dumps( recipes_collection.find() )
        
        return render_template( 'index.html' , recipes = recipes , data = data )
        
    except:
        
        print( 'Error in accessing database documents' )
 
 
     
@app.route( '/search_results' , methods = [ 'POST' ] )

def search_results():
    
    """Display recipes returned from db based on text input"""
    
    try:
        # search_content = '"{}"'.format(request.form.get('searchContent'))
        
        search_content = search_text_formatting( 'searchContent' )
        
        recipes = recipes_collection.find( { '$text' : { '$search' : search_content } } , 
                                           { '_txtscr' : { '$meta' : 'textScore' } } ).sort( [ ( '_txtscr', { '$meta' : 'textScore' } ) ] )
                                        
        return render_template( 'search_results.html' , recipes = recipes )
        
    except:
        
            print( 'Error accessing database documents' )
            
      
            
@app.route( '/advanced_search_results' , methods = [ 'POST' ] )

def advanced_search_results():
    
    """Return recipes from mongodb based on advanced search fields"""
    
    try:
        
        advanced_search_list = advanced_search_query_formatting( field_list[ 6: ] )
        
        recipes = recipes_collection.find( { '$and' : advanced_search_list } ).sort( [ ( 'recipeUpvotes' , -1 ) ] ).limit( 10 )
        
        return render_template( 'search_results.html' , recipes = recipes )
        
    except:
        
        print( 'Error accessing database documents' )
        
    
        
@app.route( '/add_recipe' )

def add_recipe():
    
    """Display add recipe page"""
    
    try:
        
        return render_template( 'add_recipe.html' )
        
    except:
        
        print( 'Error, could not render add recipe view' )
    
    
    
@app.route( '/insert_recipe' , methods = [ 'POST' ] )

def insert_recipe():
    
    """Insert recipe to db and display index.html"""
    
    try:
        
        input_fields = insert_update_db_format( field_list )
        
        recipes_collection.insert_one( input_fields )
        
        return redirect( url_for( 'get_recipes' ) )
        
    except:
        
        print( 'Error writing database document' )



@app.route( '/edit_delete_recipe/<recipe_id>' )

def edit_delete_recipe( recipe_id ):
    
    """Open edit/delete page for specific document"""
    
    try:
        
        recipe = recipes_collection.find_one( { '_id' : ObjectId (recipe_id ) } )
        
        return render_template( 'edit_delete_recipe.html' , recipe = recipe )
        
    except:
        
        print( 'Error accessing database documents' )
        
        
        
@app.route( '/update_recipe/<recipe_id>' , methods = [ 'POST' ] )

def update_recipe( recipe_id ):
    
    """Update specific document with form elements"""
    
    try:
        
        update_fields = insert_update_db_format( field_list[ 1: ] )
        
        recipes_collection.update_one( { '_id' : ObjectId( recipe_id ) } , { '$set' : update_fields }, upsert = True )
        
        return redirect( url_for( 'get_recipes' ) )
        
    except:
        
        print( 'Error updating database document' )
        
        

@app.route( '/show_recipe/<recipe_id>' )

def show_recipe( recipe_id ):
    
    """Show recipe page of specific document"""
    
    try:
        
        recipe = recipes_collection.find_one( { '_id' : ObjectId( recipe_id ) } )
        
        return render_template( 'show_recipe.html' , recipe = recipe )
        
    except:
        
        print( 'Error accessing database documents' )
        
        

@app.route( '/delete_recipe/<recipe_id>' )

def delete_recipe( recipe_id ):
    
    """Delete specific document"""
    
    try:
        
        recipes_collection.delete_one( { '_id' : ObjectId( recipe_id ) } )
        
        return redirect( url_for( 'get_recipes' ) )
        
    except:
        
        print( 'Error accessing database documents' )
        
        

@app.route( '/like_recipe/<recipe_id>' )

def like_recipe( recipe_id ):
    
    """Add upvote to document when button clicked"""
    
    try:
        
        recipes_collection.update( { '_id' : ObjectId( recipe_id ) } , { '$inc' : { 'recipeUpvotes': 1 } } )
        
        recipe = recipes_collection.find_one( { '_id' : ObjectId( recipe_id ) } )
        
        return render_template( 'show_recipe.html' , recipe = recipe )
        
    except:
        
        print( 'Error accessing database documents' )



@app.route( '/favourites' )

def favourites():
    
    """Open favourites page"""
    
    try:
        
        return render_template( 'favourites.html' ) 
        
    except:
        
        print( 'Error, could not render favourites view' )
        
        

#Assisting variables and functions

field_list = [ 'recipeUpvotes', 'recipeName', 'recipeAuthor', 'recipeIngredients', 'recipeInstructions', 'recipeImageLink', 
               'recipeCuisine', 'recipeCountryOfOrigin', 'recipeMealTime', 'recipeServings', 'recipeDifficulty', 'recipePreparationTime', 
               'recipeCookingTime', 'recipeAllergen', 'recipeDietary', 'recipeMainIngredient' ]
     
        
            
def search_text_formatting( search_text ):
    
    """Correctly format string for text search of entire db"""
    
    formatted_search_text = '\"' + request.form.get( search_text ) + '\"'
    
    return formatted_search_text
       
       
       
def advanced_search_query_formatting( list ):
    
    """Obtain input values for select boxes and append to list for advanced search query"""
    
    search_list = []
    
    for value in list:
        
        if request.form.get( value ) != '':
            
            if value == 'recipeAllergen' or value == 'recipeDietary':
                
                value_text = request.form.get( value )
                
                value_split_text = value_text.split( ', ' )
                
                search_subset = []
                
                for i in value_split_text:
                    
                    search_subset.append( i )
                    
                search_list.append( { value : { '$in' : search_subset } } )  
                
            elif value == 'recipePreparationTime' or value == 'recipeCookingTime' or value == 'recipeServings':
                
                if request.form.get( value ).isdigit() == True:
                    
                    search_list.append( { value: { '$lte' : int( request.form.get( value ) ) } } )
                    
            else:
                
                search_list.append( { value : request.form.get( value ) } )
                
    return search_list
       
       
       
def insert_update_db_format( list ):
    
    """Construct format of insert or update to be sent to db"""
    
    field_input_dict = {}
    
    for field in list:
        
        if field == 'recipeAllergen' or field == 'recipeDietary':
            
            field_value = request.form.get( field )
            
            field_value = request.form.get( field ) if field_value != '' else 'None'
            
            field_input_dict[ field ] = field_value.split( ',' )
            
        elif field == 'recipePreparationTime' or field == 'recipeCookingTime' or field == 'recipeServings':
            
            field_value = request.form.get( field )
            
            field_input_dict[ field ] = int( field_value ) if field_value.isdigit() == True else 0
            
        elif field == 'recipeUpvotes' in list:
            
            field_input_dict[ field ] = 0
            
        else:
            field_input_dict[ field ] = request.form.get( field )
            
    return field_input_dict         
     
     
     
if __name__  ==  '__main__':
    
    app.run( host = os.environ.get( 'IP' ), port = int( os.environ.get( 'PORT' ) ), debug = True )
