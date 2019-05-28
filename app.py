from flask_login import login_required
""" MODULE IMPORT """


import os
import ast
import boto3
import botocore
import flask
from flask              import Flask, render_template , redirect , request , url_for , jsonify , session as user_session, flash
from bson.objectid      import ObjectId
from bson.json_util     import dumps 
from ming               import mim, create_datastore
from ming.odm           import ThreadLocalODMSession , Mapper
from ming.base          import Cursor
from models             import recipes , users
from werkzeug.utils     import secure_filename
from werkzeug.security  import generate_password_hash , check_password_hash


""" APPLICATION CONFIGURATION """

# Configure application to use either mongodb or mongo-in-memory db 
def database_config_setup( filename ):
    database_config = os.getenv( 'MONGO_URI' ) if filename == '__main__' else 'mim://localhost/test'
    return database_config

app = Flask(__name__)                                                                   # Create flask app

app.config[ 'MONGO_DBNAME' ]  = 'onlineCookbook'                                         # Define db name
app.config[ 'MONGO_URI' ]     = database_config_setup( __name__ )                           # Define db URI
app.config[ 'UPLOAD_FOLDER' ] = os.getenv( 'UPLOAD_FOLDER' )                            # Create image upload path
app.config[ 'SECRET_KEY' ]    = os.getenv( 'SECRET_KEY' )                                  # Secret key for session


"""S3 CONFIGURATION """

app.config[ 'S3_BUCKET' ]     = os.environ.get( 'S3_BUCKET' )
app.config[ 'S3_KEY' ]        = os.environ.get( 'S3_ACCESS_KEY' )
app.config[ 'S3_SECRET' ]     = os.environ.get( 'S3_SECRET_ACCESS_KEY' )

s3_upload                     = boto3.client( 's3' )
s3_resource                   = boto3.resource( 's3' )
image_bucket                  = s3_resource.Bucket( app.config[ 'S3_BUCKET' ] )

# Download file from S3
def download_s3_file( file ):
    if os.path.isfile( app.config[ 'UPLOAD_FOLDER' ] + file ) == False:
        s3_resource.Bucket( app.config[ 'S3_BUCKET' ] ).download_file( file, app.config[ 'UPLOAD_FOLDER' ] + file )

# Download recipe images from S3 into local folder        
for key in image_bucket.objects.all():
    image_name = key.key
    download_s3_file( image_name )


""" DATABASE CONNECTION """

session                       = ThreadLocalODMSession( bind = create_datastore( app.config[ 'MONGO_URI' ]  ) ) # Create db session
recipes_collection            = session.db.recipes                                                             # Set recipe variable
users_collection              = session.db.users                                                               # Set user variable
index_mapper                  = Mapper.ensure_all_indexes()                                                    # Ensure all indexes
drop_index                    = recipes_collection.drop_index( '$**_text' )                                    # Drop search index
create_index                  = recipes_collection.create_index( [ ( '$**' , 'text' ) ] )                      # Create search index


""" RECIPE ROUTES """

# Access recipes with largest number of upvotes, convert all data to json string and display index page  
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
            
# Display recipes returned from db based upon text input 
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
        return redirect( url_for( 'advanced_search_results' , advanced_search_list = advanced_search_list ) )
    except:
        print( 'Error, could not retrieve advanced search input' )  

# Return recipes from db based on advanced search fields 
@app.route( '/advanced_search_results/<advanced_search_list>' )
def advanced_search_results(advanced_search_list):
    try:
        advanced_search_list = ast.literal_eval( advanced_search_list )
        recipes = recipes_collection.find( { '$and' : advanced_search_list } ).sort( [ ( 'recipeUpvotes' , -1 ) ] ).limit( 10 )
        return render_template( 'search_results.html' , recipes = recipes )
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
        return render_template( 'show_recipe.html' , recipe = recipe  )
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


""" USER ROUTES """
from flask_login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin,
                            confirm_login, fresh_login_required)
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
  def __init__(self,id):
    self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route( '/login')
def login():
    return render_template( 'login.html')

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
			user_obj = User(user_in_db['_id'])
			login_user(user_obj)
			user_session[ 'user' ] = form[ 'email' ]

			flash( 'You are now logged in!' )
			
			return redirect( url_for( 'get_recipes' ) )
			
		else:
		    
			flash( 'Incorrect login details' )
			
			return redirect( url_for( 'get_recipes' ) )
			
	else:
		
		flash( 'Please register!' )
		return redirect( url_for( 'register' ) )

# Register new user 

@app.route( '/register' , methods = [ 'GET' , 'POST' ] )

def register():
    
	# Check if user is logged in
	
	if 'user' in user_session:
	    
		flash( 'You are currently signed in!' )
		
		return redirect( url_for( 'get_recipes' ) )
		
	if request.method == 'POST':
	    
		form = request.form.to_dict()
		
		# Check if the password and retyped password match
		
		if form[ 'user_password' ] == form[ 'retyped_user_password' ]:
		    
			# If so try to find the user in db
			user = users_collection.find_one({"username" : form['username']})
			if user:
				#                                                     flash(f"{form['username']} already exists!")
				return redirect(url_for('register'))
			# If user does not exist register new user
			else:				
				# Hash password
				hash_pass = generate_password_hash(form['user_password'])
				#Create new user with hashed password
				users_collection.insert_one(
					{
						'username': form['username'],
						'email': form['email'],
						'password': hash_pass
					}
				)
				# Check if user is actualy saved
				user_in_db = users_collection.find_one({"username": form['username']})
				if user_in_db:
					# Log user in (add to session)
					user_session['user'] = user_in_db['username']
					return redirect(url_for('profile', user=user_in_db['username']))
				else:
					flash("There was a problem savaing your profile")
					return redirect(url_for('register'))

		else:
			flash("Passwords dont match!")
			return redirect(url_for('register'))
		
	return render_template("register.html")



# Log out user

@app.route( '/logout' )

def logout():
    
	# Clear user session
	
	user_session.clear()
	
	flash( 'You have been logged out!' )
	
	return redirect( url_for( 'get_recipes' ) )



# Profile Page
@app.route('/profile/<user>')
def profile(user): 
	# Check if user is logged in
	if 'user' in user_session:
		# If so get the user and pass him to template for now
		user_in_db = users_collection.find_one({"username": user})
		return render_template('profile.html', user=user_in_db)
	else:
		flash("You must be logged in!")
		return redirect(url_for('index'))

# Admin area
@app.route('/admin')
def admin():
	if 'user' in user_session:
		if user_session['user'] == "admin":
			return render_template('admin.html')
		else:
			flash('Only Admins can access this page!')
			return redirect(url_for('index'))
	else:
		flash('You must be logged')
		return redirect(url_for('get_recipes'))



""" ASSISTING VARIABLES AND FUNCTIONS """



field_list = [ 'recipeUpvotes', 'recipeName', 'recipeAuthor', 'recipeIngredients', 'recipeInstructions', 'recipeImageLink', 
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
                
                s3_upload.upload_file( app.config[ 'UPLOAD_FOLDER' ] + filename, app.config['S3_BUCKET'] , filename )

                
                field_input_dict[ field ] = '/' + os.path.join( app.config[ 'UPLOAD_FOLDER' ] , filename )
        else:
            field_input_dict[ field ] = request.form[ field ]
    return field_input_dict         
     
     
     
if __name__  ==  '__main__':
    
    app.run( host = os.environ.get( 'IP' ) , port = int( os.environ.get( 'PORT' ) ) , debug = True )