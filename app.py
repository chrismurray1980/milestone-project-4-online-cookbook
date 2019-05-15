import os

from flask              import Flask, render_template , redirect , request , url_for , jsonify

from bson.objectid      import ObjectId

from bson.json_util     import dumps 

from ming               import mim, create_datastore

from ming.odm           import ThreadLocalODMSession , Mapper

from ming.base          import Cursor

from models             import recipes , users

import ast


# Configure application to use either mongodb or mongo-in-memory db 

def database_config_setup( filename ):
    
    database_config = os.getenv( 'MONGO_URI', 'mongodb://localhost' ) if filename == '__main__' else 'mim://localhost/test'
   
    return database_config

app = Flask(__name__) # Create flask app

app.config[ 'MONGO_DBNAME' ] = 'onlineCookbook' # Define db name

app.config[ 'MONGO_URI' ] = database_config_setup( __name__ ) # Define db URI

session = ThreadLocalODMSession( bind = create_datastore( app.config[ 'MONGO_URI' ] ) ) # Create db session



recipes_collection = session.db.recipes # Set recipe variable

Mapper.ensure_all_indexes() # Ensure all indexes

recipes_collection.drop_index( '$**_text' ) # Drop search index

recipes_collection.create_index( [ ( '$**' , 'text' ) ] ) # Create search index



# Access recipes with largest number of upvotes and display index page  

@app.route( '/' )

def get_recipes():
    
    try:
        
        recipes = recipes_collection.find().sort( [ ( 'recipeUpvotes' , -1 ) ] ).sort( [ ( 'recipeUpvotes' , -1 ) ] ).limit( 5 )
        
        data = dumps( recipes_collection.find() )
        
        return render_template( 'index.html' , recipes = recipes , data = data )
        
    except:
        
        print( 'Error in accessing database documents' )



# Post search text and redirect to search results page

@app.route( '/search' , methods = [ 'POST' ] )

def search():
    
    try:
        
        return redirect( url_for( 'search_results' , search_content = request.form[ 'searchContent' ] ) )

    except:
        
            print( 'Error, could not retrieve text search input' )
            
            
 
# Display recipes returned from db based on text input 

@app.route( '/search_results/<search_content>' )

def search_results( search_content ):
    
    try:

        search_text = '{}{}{}'.format( '\"' , search_content , '\"' ) 
        
        recipes = recipes_collection.find( { '$text' : { '$search' : search_text } } , 
                                           { '_txtscr' : { '$meta' : 'textScore' } } ).sort( [ ( '_txtscr', { '$meta' : 'textScore' } ) ] )
                                        
        return render_template( 'search_results.html' , recipes = recipes )
        
    except:
        
            print( 'Error accessing database documents' )



# Post advanced search values and redirect to search results page

@app.route( '/advanced_search' , methods = [ 'POST' ] )

def advanced_search():
    
    
    
    try:
        advanced_search_list = advanced_search_query_formatting( field_list[ 6: ] )
        print (advanced_search_list)
        
        return redirect( url_for( 'advanced_search_results' , advanced_search_list = advanced_search_list  ) )
    except:
        
        print( 'Error, could not retrieve advanced search input' )  
            
            
      
# Return recipes from mongodb based on advanced search fields 

@app.route( '/advanced_search_results/<advanced_search_list>' )

def advanced_search_results(advanced_search_list):
    
    #try:
        bums = ast.literal_eval(advanced_search_list)
        #advanced_search_list = advanced_search_query_formatting( field_list[ 6: ] )
        print(type(bums))
        recipes = recipes_collection.find( { '$and' : bums } ).sort( [ ( 'recipeUpvotes' , -1 ) ] ).limit( 10 )
        
        return render_template( 'search_results.html' , recipes = recipes )
        
    #except:
        
        #print( 'Error accessing database documents' )
        
    

# Display add recipe page 

@app.route( '/add_recipe' )

def add_recipe():
    
    try:
        
        return render_template( 'add_recipe.html' )
        
    except:
        
        print( 'Error, could not render add recipe view' )
    
    
 
# Insert recipe to db and display index.html 
 
@app.route( '/insert_recipe' , methods = [ 'POST' ] )

def insert_recipe():
    
    try:
        
        input_fields = insert_update_db_format( field_list )
        
        new_recipe = recipes_collection.insert_one( input_fields )
        
        recipe = recipes_collection.find_one( { '_id' : ObjectId( new_recipe.inserted_id ) } )
        
        return  render_template( 'show_recipe.html' , recipe = recipe )
        
    except:
        
        print( 'Error writing database document' )



# Open edit/delete page for specific document 

@app.route( '/edit_delete_recipe/<recipe_id>' )

def edit_delete_recipe( recipe_id ):
    
    try:
        
        recipe = recipes_collection.find_one( { '_id' : ObjectId (recipe_id ) } )
        
        return render_template( 'edit_delete_recipe.html' , recipe = recipe )
        
    except:
        
        print( 'Error accessing database documents' )
        
        

# Update specific document with form elements 

@app.route( '/update_recipe/<recipe_id>' , methods = [ 'POST' ] )

def update_recipe( recipe_id ):
    
    try:
        
        update_fields = insert_update_db_format( field_list[ 1: ] )
        
        recipes_collection.update_one( { '_id' : ObjectId( recipe_id ) } , { '$set' : update_fields }, upsert = True )
        
        recipe = recipes_collection.find_one( { '_id' : ObjectId( recipe_id ) } )
        
        return  render_template( 'show_recipe.html' , recipe = recipe )
        
    except:
        
        print( 'Error updating database document' )
        
        

# Show recipe page of specific document 

@app.route( '/show_recipe/<recipe_id>' )

def show_recipe( recipe_id ):
    
    try:
        
        recipe = recipes_collection.find_one( { '_id' : ObjectId( recipe_id ) } )
        
        return render_template( 'show_recipe.html' , recipe = recipe )
        
    except:
        
        print( 'Error accessing database documents' )
        
        

# Delete specific document 

@app.route( '/delete_recipe/<recipe_id>' )

def delete_recipe( recipe_id ):
    
    try:
        
        recipes_collection.delete_one( { '_id' : ObjectId( recipe_id ) } )
        
        return redirect( url_for( 'get_recipes' ) )
        
    except:
        
        print( 'Error accessing database documents' )
        
        

# Add upvote to document when button clicked 

@app.route( '/like_recipe/<recipe_id>' )

def like_recipe( recipe_id ):
    
    try:
        
        recipes_collection.update( { '_id' : ObjectId( recipe_id ) } , { '$inc' : { 'recipeUpvotes': 1 } } )
        
        recipe = recipes_collection.find_one( { '_id' : ObjectId( recipe_id ) } )
        
        return render_template( 'show_recipe.html' , recipe = recipe )
        
    except:
        
        print( 'Error accessing database documents' )



# Open favourites page 

@app.route( '/favourites' )

def favourites():
    
    try:
        
        return render_template( 'favourites.html' ) 
        
    except:
        
        print( 'Error, could not render favourites view' )
        
        

# Assisting variables and functions

field_list = [ 'recipeUpvotes', 'recipeName', 'recipeAuthor', 'recipeIngredients', 'recipeInstructions', 'recipeImageLink', 
               'recipeCuisine', 'recipeCountryOfOrigin', 'recipeMealTime', 'recipeServings', 'recipeDifficulty', 'recipePreparationTime', 
               'recipeCookingTime', 'recipeAllergen', 'recipeDietary', 'recipeMainIngredient' ]
     
        

# Obtain input values for select boxes and append to list for advanced search query 

def advanced_search_query_formatting( list ):
    
    search_list = []
    
    for value in list:
        
        if request.form[ value ] != '':
            
            if value == 'recipeAllergen' or value == 'recipeDietary':
                
                value_text = request.form[ value ]
                
                value_split_text = value_text.split( ', ' )
                
                search_subset = []
                
                for i in value_split_text:
                    
                    search_subset.append( i )
                    
                search_list.append( { value : { '$in' : search_subset } } )  
                
            elif value == 'recipePreparationTime' or value == 'recipeCookingTime' or value == 'recipeServings':
                
                if request.form[ value ].isdigit() == True:
                    
                    search_list.append( { value: { '$lte' : int( request.form[ value ] ) } } )
                    
            else:
                
                search_list.append( { value : request.form[ value ] } )
                
    return search_list
       
       

# Construct format of insert or update to be sent to db 

def insert_update_db_format( list ):
    
    field_input_dict = {}
    
    for field in list:
        
        if field == 'recipeAllergen' or field == 'recipeDietary':
            
            field_value = request.form[ field ]
            
            field_value = request.form[ field ] if field_value != '' else 'None'
            
            field_input_dict[ field ] = field_value.split( ',' )
            
        elif field == 'recipePreparationTime' or field == 'recipeCookingTime' or field == 'recipeServings':
            
            field_value = request.form[ field ]
            
            field_input_dict[ field ] = int( field_value ) if field_value.isdigit() == True else 0
            
        elif field == 'recipeUpvotes' in list:
            
            field_input_dict[ field ] = 0
            
        else:
            field_input_dict[ field ] = request.form[ field ]
            
    return field_input_dict         
     
     
     
if __name__  ==  '__main__':
    
    app.run( host = os.environ.get( 'IP' ), port = int( os.environ.get( 'PORT' ) ), debug = True )
