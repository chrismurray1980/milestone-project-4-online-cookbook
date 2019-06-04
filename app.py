
""" MODULE IMPORT """

import os
import ast
import boto3
import botocore
from flask              import Flask, render_template, redirect, request, url_for, jsonify, session as user_session, flash
from flask_login        import LoginManager, login_required, current_user, login_user, logout_user, UserMixin, confirm_login, fresh_login_required
from bson.objectid      import ObjectId
from bson.json_util     import dumps 
from ming               import mim, create_datastore
from ming.odm           import ThreadLocalODMSession, Mapper
from ming.base          import Cursor
from models             import recipes, users
from werkzeug.utils     import secure_filename
from werkzeug.security  import generate_password_hash, check_password_hash


""" APPLICATION CONFIGURATION """

# Configure application to use either mongodb or mongo-in-memory db 
def database_config_setup( filename ):
    database_config = os.getenv( 'MONGO_URI' ) if filename == '__main__' else 'mim://localhost/test'
    return database_config

# Create flask app
app = Flask(__name__)                                                                  

# Define db name
app.config[ 'MONGO_DBNAME' ]  = 'onlineCookbook'  

# Define db URI
app.config[ 'MONGO_URI' ] = database_config_setup( __name__ )

# Create image upload path
app.config[ 'UPLOAD_FOLDER' ] = os.getenv( 'UPLOAD_FOLDER' )  

# Secret key for session
app.config[ 'SECRET_KEY' ] = os.getenv( 'SECRET_KEY' )                                  


"""S3 CONFIGURATION """

# Define S3 bucket
app.config[ 'S3_BUCKET' ] = os.environ.get( 'S3_BUCKET' )

# Define S3 access key
app.config[ 'S3_KEY' ] = os.environ.get( 'S3_ACCESS_KEY' )

# Define S3 secret key
app.config[ 'S3_SECRET' ] = os.environ.get( 'S3_SECRET_ACCESS_KEY' )

# Define S3 client for upload
s3_upload = boto3.client( 's3' )

# Define S3 resource for download
s3_resource = boto3.resource( 's3' )

# Define S3 bucket variable name
image_bucket = s3_resource.Bucket( app.config[ 'S3_BUCKET' ] )

# Define function to download file from S3
def download_s3_file( file ):
    # Check if file already stored locally
    if os.path.isfile( app.config[ 'UPLOAD_FOLDER' ] + file ) == False:
        # Download file to local storage
        s3_resource.Bucket( app.config[ 'S3_BUCKET' ] ).download_file( file, app.config[ 'UPLOAD_FOLDER' ] + file )

# Download recipe images from S3 into local folder on server start     
for key in image_bucket.objects.all():
    # Define image name variable
    image_name = key.key
    # Download S3 file
    download_s3_file( image_name )


""" DATABASE CONNECTION """

# Create database session
session = ThreadLocalODMSession( bind = create_datastore( app.config[ 'MONGO_URI' ]  ) )

# Create recipe variable
recipes_collection = session.db.recipes  

# Create user variable
users_collection = session.db.users       

# Ensure all indexes
index_mapper = Mapper.ensure_all_indexes()         

# Drop search index
drop_index = recipes_collection.drop_index( '$**_text' )   

# Create search index
create_index = recipes_collection.create_index( [ ( '$**' , 'text' ) ] )                      


""" LOGIN MANAGER """


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User( UserMixin ):
  def __init__( self, id ):
      self.id = id

@login_manager.user_loader
def load_user( user_id ):
    return User( user_id )
    
    
@login_manager.unauthorized_handler
def unauthorized_callback():
    if 'login' not in request.path:
        user_session[ 'next_url' ] = request.path
    return redirect( url_for( 'login' ) )


""" RECIPE ROUTES """

# Access recipes with largest number of upvotes, convert all data to json string and display index page  
@app.route( '/' )
def get_recipes():
    try:
        #find top 5 recipes based on number of likes
        recipes = recipes_collection.find().sort( [ ( 'recipeUpvotes' , -1 ) ] ).sort( [ ( 'recipeUpvotes' , -1 ) ] ).limit( 5 )
        # Find all recipes and convert to bson
        data = dumps( recipes_collection.find() )
        return render_template( 'index.html' , recipes = recipes , data = data )
    except:
        print( 'Error in accessing database documents' )

# Post search text and redirect to search results page
@app.route( '/search' , methods = [ 'POST' ] )
def search():
    try:
        search_content = request.form[ 'searchContent' ]
        # For empty search return to home page and flash user message
        if search_content == '':
            user_session.pop( '_flashes' , None )
            flash( 'Please enter some search criteria' )
            return redirect( url_for( 'get_recipes' ) )
        # Pass search content to search function
        else:
            return redirect( url_for( 'search_results' , search_content = search_content ) )
    except:
        print( 'Error, could not retrieve text search input' )
            
# Display recipes returned from db based upon text input
@app.route( '/search_results/<search_content>' )
def search_results( search_content ):
    try:
        # Format search text string
        search_text = '{}{}{}'.format( '\"' , search_content , '\"' )
        # Find recipes based on search text content
        recipes = recipes_collection.find( { '$text' : { '$search' : search_text } } , 
                                           { '_txtscr' : { '$meta' : 'textScore' } } ).sort( [ ( '_txtscr', { '$meta' : 'textScore' } ) ] )
        # Return count of recipes found
        recipes_count = recipes.count()
        return render_template( 'search_results.html' , recipes = recipes, recipes_count = recipes_count )
    except:
        print( 'Error accessing database documents' )


# Post advanced search values and redirect to search results page
@app.route( '/advanced_search' , methods = [ 'POST' ] )
def advanced_search():
    try:
        # Run search query function based on field list elements
        advanced_search_list = advanced_search_query_formatting( field_list[ 7: ] )
        return redirect( url_for( 'advanced_search_results' , advanced_search_list = advanced_search_list ) )
    except:
        print( 'Error, could not retrieve advanced search input' )  


# Return recipes from db based on advanced search fields 
@app.route( '/advanced_search_results/<advanced_search_list>' )
def advanced_search_results(advanced_search_list):
    try:
        
        advanced_search_list = ast.literal_eval( advanced_search_list )
        # Check if list is not empty and query db for recipes
        if advanced_search_list != []:
            # Find recipes based on search 
            recipes = recipes_collection.find( { '$and' : advanced_search_list } ).sort( [ ( 'recipeUpvotes' , -1 ) ] ).limit( 10 )
            # Count recipes found
            recipes_count = recipes.count()
            return render_template( 'search_results.html' , recipes = recipes, recipes_count = recipes_count )
        # Inform user that search is empty and return to home page
        else:
            user_session.pop( '_flashes' , None )
            flash( 'Please enter some search criteria' )
            return redirect( url_for( 'get_recipes' ) )
    except:
        print( 'Error accessing database documents' )

# Display add recipe page 
@app.route( '/add_recipe' )
@login_required
def add_recipe():
    try:
        return render_template( 'add_recipe.html' )
    except:
        print( 'Error, could not render add recipe view' )
 
# Insert recipe to db and display index.html 
@app.route( '/insert_recipe' , methods = [ 'POST' ] )
def insert_recipe():
    try:
        # Run function to obtain fields to be inserted
        input_fields = insert_update_db_format( field_list )
        # Insert new recipe
        new_recipe = recipes_collection.insert_one( input_fields )
        # Find recipe inserted
        recipe = recipes_collection.find_one( { '_id' : ObjectId( new_recipe.inserted_id ) } )
        # Add inserted recipe to user document 
        users_collection.update({ 'email': user_session[ 'user' ] },{ '$addToSet': { 'my_recipes': ObjectId( recipe['_id'] ) } }, upsert = True)
        # Notify user
        user_session.pop( '_flashes' , None )
        flash( 'Recipe successfully added and can be viewed in the my-recipes link!' )
        return  render_template( 'show_recipe.html' , recipe = recipe )
    except:
        print( 'Error writing database document' )

# Open edit/delete page for specific document 
@app.route( '/edit_delete_recipe/<recipe_id>' )
@login_required
def edit_delete_recipe( recipe_id ):
    try:
        # Find recipe document
        recipe = recipes_collection.find_one( { '_id' : ObjectId (recipe_id ) } )
        # Check if current user is recipe author
        if recipe['recipeEmail'] == user_session['user']:
            return render_template( 'edit_delete_recipe.html' , recipe = recipe )
        # If not, inform user and return to home page
        else: 
            user_session.pop( '_flashes' , None )
            flash('You are not authorised to edit this recipe')
            return redirect(url_for( 'get_recipes'))
    except:
        print( 'Error accessing database documents' )

# Update specific document with form elements 
@app.route( '/update_recipe/<recipe_id>' , methods = [ 'POST' ] )
def update_recipe( recipe_id ):
    try:
        # Run function to obtain recipe fields to be updated
        update_fields = insert_update_db_format( field_list[ 2: ] )
        # Update recipe document
        recipes_collection.update_one( { '_id' : ObjectId( recipe_id ) } , { '$set' : update_fields }, upsert = True )
        # Find updated recipe
        recipe = recipes_collection.find_one( { '_id' : ObjectId( recipe_id ) } )
        # Inform user of update
        user_session.pop( '_flashes' , None )
        flash( 'Recipe successfully updated!' )
        return  render_template( 'show_recipe.html' , recipe = recipe )
    except:
        print( 'Error updating database document' )
        
# Show recipe page of specific document 
@app.route( '/show_recipe/<recipe_id>' )
def show_recipe( recipe_id ):
    try:
        # Find recipe document
        recipe = recipes_collection.find_one( { '_id' : ObjectId( recipe_id ) } )
        return render_template( 'show_recipe.html' , recipe = recipe  )
    except:
        print( 'Error accessing database documents' )

# Delete specific document 

@app.route( '/delete_recipe/<recipe_id>' )
def delete_recipe( recipe_id ):
    try:
        recipes_collection.delete_one( { '_id' : ObjectId( recipe_id ) } )
        users_collection.update({ 'email': user_session[ 'user' ] },{ '$pull': { 'favourite_recipes': ObjectId( recipe_id ) } }, upsert = True)
        users_collection.update({ 'email': user_session[ 'user' ] },{ '$pull': { 'my_recipes': ObjectId( recipe_id ) } }, upsert = True)
        
        
        # Inform user of deletion
        user_session.pop( '_flashes' , None )
        flash( 'Recipe successfully deleted!' )
        return redirect( url_for( 'get_recipes' ) )
    except:
        print( 'Error accessing database documents' )


# Add like and document to favourites when button clicked 
@app.route( '/like_recipe/<recipe_id>' )
@login_required
def like_recipe( recipe_id ):
    try:
        # Check if recipe already in user favourites
        user_favourites=users_collection.find( { 'email': user_session[ 'user' ], 'favourite_recipes': ObjectId( recipe_id )} )
        user_session.pop( '_flashes' , None )
        if user_favourites.count() != 0:
            # If already in favourites, notify user
            flash( 'This recipe has already been added to your favourites list' )
        else:
            # Update number of recipe likes
            recipes_collection.update( { '_id' : ObjectId( recipe_id ) } , { '$inc' : { 'recipeUpvotes': 1 } } )
            # Add recipe to user document
            users_collection.update({ 'email': user_session[ 'user' ] },{ '$addToSet': { 'favourite_recipes': ObjectId( recipe_id ) } }, upsert = True)
            # Notify user of successful addition
            flash( 'You have successfully added this recipe to your favourite recipe list!' )
        # Find recipe in collection
        recipe = recipes_collection.find_one( { '_id' : ObjectId( recipe_id ) } )
        return render_template( 'show_recipe.html' , recipe = recipe )
    except:
        print( 'Error accessing database documents' )

# Open favourites page 
@app.route( '/favourites' )
@login_required
def favourites():
    try:
        favourites_list = []
        # Find recipes in user favourites
        user_favourites = users_collection.find( {'email': user_session[ 'user' ] }, { 'favourite_recipes' } )
        # Append recipes to favourites list
        for recipe in user_favourites:
            for recipe_id in recipe['favourite_recipes']:
                favourites_list.append(recipe_id)
        # Find recipes contained in favpurites list
        recipes=recipes_collection.find( { '_id' : { '$in' : favourites_list } } )
        # Count recipes found
        favourites_count = recipes.count()
        return render_template( 'favourites.html', recipes=recipes, favourites_count = favourites_count) 
    except:
        print( 'Error, could not render favourites view' )

# Open my_recipes page 
@app.route( '/my_recipes' )
@login_required
def my_recipes():
    try:
        my_recipes_list = []
        # Find recipes in users my-recipes list
        user_my_recipes = users_collection.find( {'email': user_session[ 'user' ] }, { 'my_recipes' } )
        # Append recipes to my_recipes_list
        for recipe in user_my_recipes:
            for recipe_id in recipe['my_recipes']:
                my_recipes_list.append(recipe_id)
        # Find recipes from list in collection
        recipes=recipes_collection.find( { '_id' : { '$in' : my_recipes_list } } )
        # Count recipes found
        my_recipes_count = recipes.count()
        return render_template( 'my_recipes.html', recipes=recipes, my_recipes_count = my_recipes_count ) 
    except:
        print( 'Error, could not render my recipes view' )


""" USER ROUTES """

# User to login form
@app.route( '/login' )
def login():
    return render_template( 'login.html' )


# Check user login details from login form

@app.route( '/submit_login' , methods = [ 'POST' ] )
def submit_login():
	form = request.form.to_dict()
	user_in_db = users_collection.find_one( { 'email' : form[ 'email' ] } )
	user_session.pop( '_flashes' , None )
	# Check for user in database
	if user_in_db:
		# If passwords match 
		if check_password_hash( user_in_db[ 'password' ] , form[ 'user_password' ] ):
			# Login user
			user_obj = User( user_in_db[ '_id' ] )
			login_user( user_obj )
			user_session[ 'user' ] = form[ 'email' ]
			flash( 'You are now logged in!' )
			next_page = user_session.get( 'next_url' )
			return redirect( next_page ) if next_page else redirect( url_for( 'get_recipes' ) )
		else:
			flash( 'Incorrect login details' )
			return redirect( url_for( 'login' ) )
	else:
		flash( 'No account found with those login details!' )
		return redirect( url_for( 'register' ) ) 


# Register new user


@app.route( '/register' , methods = [ 'GET' , 'POST' ] )
def register():
    user_session.pop( '_flashes' , None )
    # Check if user is logged in
    if 'user' in user_session:
        flash( 'You are currently signed in!' )
        return redirect( url_for( 'get_recipes' ) )
    elif request.method == 'POST':
        form = request.form.to_dict()
        # Check if the password and retyped password match
        if form[ 'user_password' ] == form[ 'retyped_user_password' ]:
            # find the user in db
            user = users_collection.find_one( { "username" : form[ 'username' ] } )
            if user:
                flash( 'Your account already exists!' )
                return redirect( url_for( 'login' ) )
			# If user does not exist register new user
            else:
		        # Hash password
                hash_pass = generate_password_hash( form[ 'user_password' ] )
				#Create new user with hashed password
                users_collection.insert_one(
					{
						'username': form[ 'username' ],
						'email': form[ 'email' ],
						'password': hash_pass,
						'favourite_recipes':[],
						'my_recipes':[]
					}
				)
				# Check if user is saved
                user_in_db = users_collection.find_one( { "username": form[ 'username' ] } )
                if user_in_db:
					# Log user in (add to session)
                    user_session[ 'user' ] = user_in_db[ 'username' ]
                    flash( 'You have successfully registered, please login to access site features' )
                    return redirect( url_for( 'login' ) )
                else:
                    flash( 'There was a problem saving your profile' )
                    return redirect( url_for( 'register' ) )
        else:
            flash( 'Passwords do not match!' )
            return redirect( url_for( 'register' ) )
    return render_template( 'register.html' )
	

# Log out user

@app.route( '/logout' )
def logout():
	# Clear user session
	user_session.clear()
	flash( 'You have successfully logged out!' )
	return redirect( url_for( 'get_recipes' ) )


""" ASSISTING VARIABLES AND FUNCTIONS """


field_list = [ 'recipeEmail', 'recipeUpvotes', 'recipeName', 'recipeAuthor', 'recipeIngredients', 'recipeInstructions', 'recipeImageLink', 
               'recipeCuisine', 'recipeCountryOfOrigin', 'recipeMealTime', 'recipeServings', 'recipeDifficulty', 'recipePreparationTime', 
               'recipeCookingTime', 'recipeAllergen', 'recipeDietary', 'recipeMainIngredient' ]
  

        
# Ensure uploaded image type is of allowed type
	
def allowed_file( filename ):
    return '.' in filename and filename.rsplit( '.' , 1 )[ 1 ].lower() in set( [  'png' , 'jpg' , 'jpeg' ] )


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
        elif field == 'recipeImageLink':
            file = request.files[ 'file' ]
            if file != '' and allowed_file( file.filename ):
                filename = secure_filename( file.filename )
                file.save( os.path.join( app.config[ 'UPLOAD_FOLDER' ] , filename ) )
                file = '/' + os.path.join( app.config[ 'UPLOAD_FOLDER' ] , filename )
                s3_upload.upload_file( app.config[ 'UPLOAD_FOLDER' ] + filename, app.config[ 'S3_BUCKET' ] , filename )
                field_input_dict[ field ] = '/' + os.path.join( app.config[ 'UPLOAD_FOLDER' ] , filename )
        elif field == 'recipeEmail':
            field_input_dict[ field ]= user_session[ 'user' ]
        else:
            field_input_dict[ field ] = request.form[ field ]
    return field_input_dict         
     
     
if __name__  ==  '__main__':
    app.run( host = os.environ.get( 'IP' ) , port = int( os.environ.get( 'PORT' ) ) , debug = True )
    
    