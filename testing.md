# Testing 

The testing conducted to verify the functionality of the website consisted of both automated testing and manual testing, user various screen sizes and web browsers. Due to time constraints; the automated testing portion is limited compared to the initial
intentions of the author.

### Automated testing

Automated testing was used to test the main functionality of the website and was undertaken using the Ming-In-Memory (mim) database which provides temporary storage for the documents created during testing. Flask-testing is used in conjunction with Python unittests
to conduct the automated tests themselves.  

To begin testing a FlaskTestCase class is created, which contains all the test functions, and a function defined that configures the application for testing. This configures the application to disable the login manager functionality, used to
check authentication, and re-initialises login manager for the application:

        def create_app( self ):
            app.config[ 'TESTING' ] = True
            app.config[ 'LOGIN_DISABLED' ] = True
            login_manager = LoginManager()
            login_manager.init_app( app )
            return app
    
#### test setup 

The test setup function creates the recipe and user documents, using mock object ID's, in the mim database which will used throughout the testing of the site functionality. This setup will be run at the beginning of 
of each test function.

    def setUp( self ):
            # create mock object id's
            objectId_1 = ObjectId( '0123456789ab0123456789ab' )
            objectId_2 = ObjectId( '0123456789ab0123456789ad' )
            # create mock user document
            users_collection.insert_one(users.make( dict( username = 'chris', email = 'chris@chris', password = 'chris', favouriteRecipes = [ '0123456789ab0123456789ab' ], myRecipes = [], likedRecipes = [] ) ) )
            # create mock recipe documents
            recipes_collection.insert_one( recipes.make( dict( _id = objectId_1, recipeName = 'test this document' , recipeUpvotes = 15, recipeCuisine = 'Mexican' ) ) )
            recipes_collection.insert_one( recipes.make( dict( _id = objectId_2, recipeName = 'test another document', recipeUpvotes = 14, recipeCuisine = 'Italian' ) ) )
            
#### test teardown

The test teardown function removes the recipe and user documents from the mim database at the end of each test and clears the database session. This is run at the end of each test function.

    def tearDown( self ):
        # remove all recipes and users documents
        recipes_collection.delete_many( {} )
        users_collection.delete_many( {} )
        # clear db session
        session.clear()

#### test database used

The first actual test run is used to verify that the mim database is currently being used during testing. This was written due to the fact that I initially had issues getting the mim database working. This 
was successfully solved by defining the following function in app.py:

    def database_config_setup( filename ):
        database_config = os.getenv( 'MONGO_URI' ) if filename == '__main__' else 'mim://localhost/test'
        return database_config

This function ensures that if the app.py file is being called directly that the mongoDB database is used otherwise, the mim database is used.   
    
#### test index page loads, contains recipe data and converts cursor to json string

This test firstly creates the response variable for the index page route, then creates BSON data which is used in app.py to create the dc.js plots. It then tests that the response by the server 
is a 200 OK code and that the template used by the flask server is 'index.html'. Furthermore, the test checks that the response from the server contains the recipe document information added in the test 
setup function. The function also tests that the correct number of user and recipe documents are present in the mim database. Finally, the test checks that the BSON conversion of the recipe data returns
a response which is a string.

        def test_get_recipes( self ):
            # create response variable
            response = self.client.get( '/' , follow_redirects = True )
            # convert recipe documents to bson
            data_dumps = dumps( recipes_collection.find() )
            # ensure 200 repsonse given by server
            self.assert200( response )
            # ensure redirect to index page
            self.assertTemplateUsed( 'index.html' )
            # ensure recipe document text in response
            self.assertIn( b'test this document', response.data )
            self.assertIn( b'Italian', response.data )
            # ensure recipe document count is correct
            self.assertEqual( recipes_collection.count() , 2 )
            # ensure user document count is correct
            self.assertEqual( users_collection.count() , 1 )
            # ensure bson is of correct data type
            self.assertEqual( type( data_dumps ) , str )
    
#### Ensure search results page loads and contains recipe data for the advanced search
This test checks the advanced search function in app.py. Firstly the test creates a response for the advanaced search results function with some recipe-cuisine search criteria. The test checks that the
server returns a 200 OK repsonse and that the endpoint template used is 'search_results.html'. Again the number of recipe and user documents present within the mim database is verified.

    def test_advanced_search( self ):
        response = self.client.get( "/advanced_search_results/[{'recipeCuisine': 'Italian'}]", follow_redirects = True )
        # ensure correct server response
        self.assert200( response )
        # ensure correct template used
        self.assertTemplateUsed( 'search_results.html' )
        # assert correct number of recipe documents
        self.assertEqual( recipes_collection.count() , 2 )
        # assert correct number of user documents
        self.assertEqual( users_collection.count() , 1 )
      
#### Ensure add_recipe page loads correctly 

This test ensures that the add-recipe route functions correctly. Firstly a response variable is defined with the add-recipe route as its endpoint. The test checks that the server returns a 200 OK response.
FInally the test ensures that the 'add_recipe.html' is the template used by the flask application.

    def test_add_recipe( self ):
        # create response variable
        response = self.client.get( '/add_recipe' , follow_redirects = True )
        # ensure correct server response
        self.assert200( response )
        # ensure correct template used
        self.assertTemplateUsed( 'add_recipe.html' )
    
#### Ensure insert recipe works correctly and show_recipe page is then rendered

This test first creates a new object ID and inserts a new recipe document into the mim database. It also inserts the recipe ID into the user document. It then finds the newly created recipe in the 
database and the correct user document and verifies that the document has indeed been craeted in the database and that the user document continas the recipe ID in the my-recipe array. The test then verifies
that there are now 3 recipe documents in the databse. The test the creates a test context to verify that the function within the app.py will redirect to that the 'show_recipe.html' with that specific 
recipe ID. The test ensures that a 200 OK response is returned form the flask server; that the 'show_recipe.html' template is used and that the response contains the inserted recipe information.

    def test_insert_recipe( self ): 
        # setup recipe test object id
        objectId = ObjectId( '5cf4f99b6a6c520e6648eee5' )
        # insert document to recipes
        recipes_collection.insert_one( {'_id'  : objectId , 'recipeName' : 'test insert document' }  )
        # insert recipe id to user document
        users_collection.update_one( { 'email': 'chris@chris' },{ '$addToSet': { 'myRecipes': objectId } }, upsert = True )
        # find recipe document inserted
        recipe = recipes_collection.find_one( {'recipeName': 'test insert document' } )
        # find user document updated
        user_recipe = users_collection.find_one( { "myRecipes": [objectId] } )
        # ensure correct recipe content
        self.assertTrue( recipe[ 'recipeName' ] == 'test insert document' )
        # ensure correct user content
        self.assertTrue( user_recipe['myRecipes'] == [objectId] )
        # assert correct number of recipe documents
        self.assertEqual( recipes_collection.count() , 3 )
        # assert correct number of user documents
        self.assertEqual( users_collection.count() , 1 )
        with app.test_request_context( '/show_recipe/5cf4f99b6a6c520e6648eee5' ):
           response = self.client.get( '/show_recipe/5cf4f99b6a6c520e6648eee5', follow_redirects = True )
           # ensure 200 response
           self.assert200( response)
           # ensure correct recipe used
           self.assertTemplateUsed( 'show_recipe.html' )
           # ensure correct data in response
           self.assertIn( b'test insert document' , response.data )

#### Ensure recipe is updated and show_recipe page is rendered

This test firstly updates the recipe in the mim database with new information then finds the recipe in the database. It then checks that the information in the recipe has been updated and checks the recipe and user
document count. It then creates a test context for the endpoint template and the recipe ID and ensures that the server returns a 200 OK response; that the template used is correct; and that the correct recipe data
is contained within the response.

    def test_update_recipe( self ):
        # update recipe document
        recipes_collection.update_one( { '_id' : ObjectId( '0123456789ab0123456789ab' ) } , { "$set" : { 'recipeName' : 'This has been updated' } } , upsert = True )
        # find recipe updated
        recipe = recipes_collection.find_one( {'recipeName': 'This has been updated' } )
        # ensure correct recipe content
        self.assertTrue( recipe['recipeName'] == 'This has been updated' )
        # assert correct number of recipe documents
        self.assertEqual( recipes_collection.count() , 2 )
        # assert correct number of user documents
        self.assertEqual( users_collection.count() , 1 )
        with app.test_request_context( '/show_recipe/0123456789ab0123456789ab' ):
           response = self.client.get( '/show_recipe/0123456789ab0123456789ab', follow_redirects = True )
           # ensure 200 response
           self.assert200( response )
           # ensure correct template
           self.assertTemplateUsed( 'show_recipe.html' )
           # ensure correct data
           self.assertIn( b'This has been updated', response.data )
    
#### Ensure show_recipe page loads and shows correct recipe

This test checks that the show recipe page is shown with information for the correct recipe ID. Firstly a test context is created using the reicpe ID and the test ensures that a 200 OK response is returned 
by the flask server. The test also ensures that correct template is used and that correct recipe information is contained within the server response.

    def test_show_recipe( self ):
        with app.test_request_context( '/show_recipe/0123456789ab0123456789ad' ):
           response = self.client.get( '/show_recipe/0123456789ab0123456789ad', follow_redirects = True )
           # ensure correct response
           self.assert200( response )
           # ensure correct template used
           self.assertTemplateUsed( 'show_recipe.html' )
           # ensure correct data
           self.assertIn( b'test another document', response.data )
    
#### Ensure recipe is deleted and index page is returned

This test was used to ensure the functionality of the delete recipe function. Firstly, the recipe is deleted and the test ensures that the application redirects the user to the index page of the site. The test 
then ensures that the correct number of recipe document are now contained within the database.

    def test_delete_recipe( self ):
        recipes_collection.delete_one( { '_id' : ObjectId( '0123456789ab0123456789ab' ) } )
        # create response
        response = self.client.get( '/' , follow_redirects = True )
        # ensure correct server response
        self.assert200( response )
        # ensure correct template used
        self.assertTemplateUsed( 'index.html' )
        # ensure correct recipe count
        self.assertEqual( recipes_collection.count() , 1 )

#### Running automated tests

Automated testing can be conducted by typing:

    python3 test.py

into the the console. This will run the tests using the mim database.

### Manual testing

Testing was also conducted manually on each of the website pages and overall functionality verified.

#### Tests conducted on navbar

The following tests were conducted on the site navbar on all pages of the site:

| Test  |      Functionality                                                                                     |  Result |
|-------|   :-----------------------:                                                                            |------:|
| 1     |  Clicking site logo on all pages returns index page                                                    | pass |
| 2     |  Clicking add recipe on all pages when not logged-in redirects to login page then to add-recipe page   | pass |
| 3     |  Clicking add recipe on all pages when logged-in redirects to add-recipe page                          | pass |
| 4     |  Clicking favourites on all pages when not logged-in redirects to login page then to favourites        | pass |
| 5     |  Clicking favourites on all pages when logged-in redirects to favourites                               | pass |
| 6     |  Log-in and register links visible on all pages when not logged in                                     | pass |
| 7     |  My-recipes and log-out visible on all pages when logged in                                            | pass |
| 8     |  Clicking log-in renders log-in form on all pages                                                      | pass |
| 9     |  Clicking register renders register form on all pages                                                  | pass |
| 10    |  Clicking log-out logs out user and redirects to index on all pages                                    | pass |
| 11    |  Clicking my-recipes redirects to my-recipes on all pages                                              | pass |

#### Tests conducted on index.html

The following tests were undertaken on the index page:


| Test  |      Functionality                                                               | Result |
|-------|   :-----------------------:                                                      |------:|
| 1     |  Index page is rendered on server startup                                        | pass |
| 2     |  Top 5 most liked recipes shown in recipe carousel with information              | pass |
| 3     |  Recipe data passed to index page as BSON                                        | pass |
| 4     |  Recipe data plots displayed correctly                                           | pass |
| 5     |  Recipe data plots react dynamically                                             | pass |
| 6     |  Search/advanced search/browse all action buttons visible                        | pass |
| 7     |  Input text box visible on page rendered                                         | pass |
| 8     |  Clicking search button renders search_results page with correct results         | pass |
| 9     |  Input text box visible on page rendered                                         | pass |
| 10    |  Advanced search form shown on advanced search button click                      | pass |
| 11    |  Advanced search form hidden on button click                                     | pass |
| 12    |  Search results rendered on advanced search form submission                      | pass |
| 13    |  Recipe card view recipe button renders correct show recipe page on button click | pass |
| 14    |  data plots shown on show data button click                                      | pass |
| 15    |  data plots hidden on show data button click                                     | pass |
| 16    |  data plots reset on button click                                                | pass |
| 17    |  data filter dynamically on click                                                | pass |


#### Tests conducted on add_recipe.html

The following test were undertaken on the add recipe page:

| Test  |      Functionality                                                                                             | Result |
|-------|   :-----------------------:                                                                                    |------:|
| 1     |  Add recipe page is rendered on link click                                                                     | pass |
| 2     |  Add recipe page is rendered correctly                                                                         | pass |
| 3     |  Input fields contain placeholders                                                                             | pass |
| 4     |  Dropdown selects are populated correctly                                                                      | pass |
| 5     |  Checkboxes and values rendered correctly                                                                      | pass |
| 6     |  Textbox appears on add ingredient and add instruction button click                                            | pass |
| 7     |  Textbox removed on remove button click                                                                        | pass |
| 8     |  Confirm ingredients/instructions button visible on add ingredient/instruction button click                    | pass |
| 9     |  Confirm ingredients/instructions button replaced by confirmation text on button click                         | pass |
| 10    |  File upload box opened on browse files button click                                                           | pass |
| 11    |  File name selected shown when file is selected                                                                | pass |
| 12    |  On submit button click the form is submitted and the show recipe page for the added recipe is shown correctly | pass |

#### Tests conducted on edit-delete-recipe.html

The following test were undertaken on the edit delete recipe page:

| Test  |      Functionality                                                                                             | Result |
|-------|   :-----------------------:                                                                                    |------:|
| 1     |  Edit delete recipe page is rendered on button click on show recipe page for recipe creator                    | pass |
| 2     |  Edit delete recipe page is rendered correctly                                                                 | pass |
| 3     |  Input fields contain current recipe information                                                               | pass |
| 4     |  Dropdown selects are populated correctly                                                                      | pass |
| 5     |  Checkboxes and values rendered correctly                                                                      | pass |
| 6     |  Current ingredients/instructions textboxes correctly populated                                                | pass |
| 7     |  Textbox appears on add ingredient and add instruction button click                                            | pass |
| 8     |  Textbox removed on remove button click                                                                        | pass |
| 9     |  Confirm ingredients/instructions button visible on add ingredient/instruction button click                    | pass |
| 10    |  Confirm ingredients/instructions button replaced by confirmation text on button click                         | pass |
| 11    |  File upload box opened on browse files button click                                                           | pass |
| 12    |  File name selected shown when file is selected                                                                | pass |
| 13    |  Current image selected correctly shown as filename only (no path)                                             | pass |
| 14    |  On submit button click the form is submitted and the show recipe page for the added recipe is shown correctly | pass |
| 15    |  On delete button click the recipe is removed from database and the index page is rendered                     | pass |

#### Tests conducted on show-recipe.html

The following test were undertaken on the show recipe page:

| Test  |      Functionality                                                                        | Result |
|-------|   :-----------------------:                                                               |------:|
| 1     |  Show recipe page is rendered on view recipe button click on all pages                    | pass |
| 2     |  Recipe image and information show correctly on page                                      | pass |
| 3     |  Recipe instructions/ingredients shown correctly on page                                  | pass |
| 4     |  If user not logged in, no further action buttons visible on page                         | pass |
| 5     |  If user logged in and is recipe creator, edit-recipe button visible on page              | pass |
| 6     |  If user logged in and but not recipe creator, like and favourite buttons visible on page | pass |
| 7     |  If user has already liked recipe, unlike button visible on page                          | pass |
| 8     |  If user has already added recipe to favourites, unfavourite button visible on page       | pass |
| 9     |  Recipe likes count increments on like button click                                       | pass |
| 10    |  Recipe likes count decrements on unlike button click                                     | pass |
| 11    |  Recipe added to user favourites on favourite button click                                | pass |
| 12    |  Recipe removed from user favourites on unfavourite button click                          | pass |

#### Tests conducted on favourites.html

The following test were undertaken on the favourites page:

| Test  |      Functionality                                                                                  | Result |
|-------|   :-----------------------:                                                                         |------:|
| 1     |  Favourites page is rendered on favourites button click on all pages                                | pass |
| 2     |  Number of recipes in favourites is correctly shown on page                                         | pass |
| 3     |  Recipe information correctly shown for each recipe and view recipe button visible                  | pass |
| 4     |  View recipe button renders show recipe page for correct recipe with correct action buttons visible | pass |

#### Tests conducted on my-recipes.html

The following test were undertaken on the my-recipes page:

| Test  |      Functionality                                                                                  | Result |
|-------|   :-----------------------:                                                                         |------:|
| 1     |  My-recipes page is rendered on my-recipes button click on all pages                                | pass |
| 2     |  Number of recipes in my-recipes is correctly shown on page                                         | pass |
| 3     |  Recipe information correctly shown for each recipe and view recipe button visible                  | pass |
| 4     |  View recipe button renders show recipe page for correct recipe with correct action buttons visible | pass |

#### Tests conducted on search-results.html

The following test were undertaken on the search results page:

| Test  |      Functionality                                                                                  | Result |
|-------|   :-----------------------:                                                                         |------:|
| 1     |  Search results page is rendered upon search/advanced search/browse all button click                | pass |
| 2     |  Number of recipes in search results is correctly shown on page                                     | pass |
| 3     |  Recipe information correctly shown for each recipe and view recipe button visible                  | pass |
| 4     |  View recipe button renders show recipe page for correct recipe with correct action buttons visible | pass |

#### Tests conducted on login.html

The following test were undertaken on the log-in page:

| Test  |      Functionality                                                                                   | Result |
|-------|   :-----------------------:                                                                          |------:|
| 1     |  Log-in page rendered on log-in button click                                                         | pass |
| 2     |  Log-in page rendered on when unauthorised user attempts to access page which requires authorisation | pass |
| 3     |  User logged in when correct details given and login button clicked                                  | pass |
| 4     |  Log-in page re-rendered when password is incorrect on log-in button click                           | pass |
| 5     |  Register page rendered on log-in button click when user not in database                             | pass |

#### Tests conducted on register.html

The following test were undertaken on the register page:

| Test  |      Functionality                                                                | Result |
|-------|   :-----------------------:                                                       |------:|
| 1     |  Register page rendered on register button click                                  | pass |
| 2     |  User redirected to log-in page when new user details submitted to database       | pass |
| 3     |  Register page re-rendered when passwords do not match on register button click   | pass |
| 4     |  Login page rendered when user already in database on register button click       | pass |




