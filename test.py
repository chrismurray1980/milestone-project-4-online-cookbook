import unittest
from flask              import session as user_session
from flask_testing      import TestCase
from app                import app , session, recipes_collection, users_collection
from models             import recipes , users
from bson.objectid      import ObjectId
from bson.json_util     import dumps 


# Create flask test case class 
class FlaskTestCase(TestCase):

    # Create app for test 
    def create_app( self ):
        app.config[ 'TESTING' ] = True
        return app
    
    # Create test setup 
    def setUp( self ):
        # setup application
        self.app = app.test_client()
        # create mock object id's
        objectId_1 = ObjectId( '0123456789ab0123456789ab' )
        objectId_2 = ObjectId( '0123456789ab0123456789ad' )
        # create mock user document
        users_collection.insert_one(users.make( dict(username = 'chris', email = 'chris@chris', password = 'chris', favouriteRecipes = [], myRecipes = [], likedRecipes = []) ) )
        # create mock recipe documents
        recipes_collection.insert_one( recipes.make( dict( _id = objectId_1, recipeName = 'test this document' , recipeUpvotes = 15, recipeCuisine = 'Mexican' ) ) )
        recipes_collection.insert_one( recipes.make( dict( _id = objectId_2, recipeName = 'test another document', recipeUpvotes = 14, recipeCuisine = 'Italian' ) ) )
    
    # Tear down test setup 
    def tearDown( self ):
        # remove all recipes and users documents
        recipes_collection.delete_many( {} )
        users_collection.delete_many( {} )
        # clear db session
        session.clear()
        
    # Test database used
    def test_database( self ):
        # ensure mongo in memory db used
        self.assertTrue( app.config[ 'MONGO_URI' ] , 'mim://localhost/test' )
    
    # Ensure index page loads, contains recipe data and converts cursor to json string
    def test_get_recipes( self ):
        # create response variable
        response = self.app.get( '/' , follow_redirects = True )
        # convert recipe documents to bson
        data_dumps = dumps( recipes_collection.find() )
        # ensure 200 repsonse given by server
        self.assertTrue( response, 200 )
        # ensure redirect to index page
        self.assertTrue( response, 'index.html' )
        # ensure recipe document text in response
        self.assertIn( b'test this document' , response.data )
        self.assertIn( b'Italian' , response.data )
        # ensure recipe document count is correct
        self.assertEqual( recipes_collection.count() , 2 )
        # ensure user document count is correct
        self.assertEqual( users_collection.count() , 1 )
        # ensure bson is of correct data type
        self.assertTrue( type( data_dumps) , 'str' )    
        
    # Ensure search results page loads and contains recipe data 
    def test_search( self ):
        # create mock search text
        search_text = 'test this document'
        # find document with search text
        data = recipes_collection.find( { 'recipeName' : search_text } )
        # extract data contents from cursor
        for document in data: 
            return document[ 'recipeName' ]
        # create response variable    
        response = self.app.get( '/search_results/test this document' , follow_redirects = True , data = document[ 'recipeName' ])
        # ensure correct response from server
        self.assertTrue( response, 200 )
        # ensure correct template used
        self.assertTrue( response, 'search_results.html' )
        # ensure correct information in document
        self.assertIn( b'test this document' , response.data )
        # ensure correct number of recipe documents in db
        self.assertEqual( recipes_collection.count() , 2 )    
        # ensure correct number of user documents in db
        self.assertEqual( users_collection.count() , 1 ) 
        
    # Ensure search results page loads and contains recipe data for advanced search
    def test_advanced_search( self ):
        # find mock recipe in collection
        data = recipes_collection.find( { 'recipeCuisine' : 'Italian' } )
        # extract data from recipe 
        for document in data: 
            return document[ 'recipeCuisine' ]
        # create response variable
        response = self.app.get( "/search_results/[{'recipeCuisine': 'Italian'}]" , follow_redirects = True, data =  document[ 'recipeCuisine' ] )  
        # ensure correct server response
        self.assertTrue( response, 200 )
        # ensure correct template used
        self.assertTrue( response, 'search_results.html' )
        # ensure correct cuisine in response
        self.assertIn( b'Italian' , response.data )
        # assert correct number of recipe documents
        self.assertEqual( recipes_collection.count() , 2 )
        # assert correct number of user documents
        self.assertEqual( users_collection.count() , 1 )
        
    # Ensure add_recipe page loads correctly 
    def test_add_recipe( self ):
        # create response variable
        response = self.app.get( '/add_recipe' , follow_redirects = True )
        # ensure correct server response
        self.assertTrue( response, 200 )
        # ensure correct template used
        self.assertTrue( response, 'add_recipe.html' )
    
    # Ensure insert recipe works correctly and show_recipe page is then rendered
    def test_insert_recipe( self ): 
        # setup recipe test object id
        objectId = ObjectId( '5cf4f99b6a6c520e6648eee5' )
        # insert document to recipes
        recipes_collection.insert_one( {'_id'  : objectId , 'recipeName' : 'test insert document' }  )
        # insert recipe id to user document
        users_collection.update_one({ 'email': 'chris@chris' },{ '$addToSet': { 'myRecipes': objectId } }, upsert = True)
        # find recipe document inserted
        recipe = recipes_collection.find_one({'recipeName': 'test insert document'})
        # find user document updated
        user_recipe = users_collection.find_one({"myRecipes": [objectId]})
        # create response variable
        response = self.app.get( '/show_recipe' , follow_redirects = True )
        # ensure correct server repsonse
        self.assertTrue( response, 200 )
        # ensure correct template used
        self.assertTrue(response, 'show_recipe.html')
        # ensure correct recipe content
        self.assertTrue(recipe['recipeName'] == 'test insert document')
        # ensure correct user content
        self.assertTrue(user_recipe['myRecipes'] == [objectId])
        # assert correct number of recipe documents
        self.assertEqual( recipes_collection.count() , 3 )
        # assert correct number of user documents
        self.assertEqual( users_collection.count() , 1 )
    
    # Ensure edit_delete_recipe page loads with correct recipe_id
    def test_edit_delete_recipe( self ):
        # create response variable
        response = self.app.get( '/edit_delete_recipe/0123456789ab0123456789ab' , follow_redirects = True )
        # ensure correct server response
        self.assertTrue( response, 200 )
        # ensure correct template used
        self.assertTrue( response, 'edit_delete_recipe.html' )
        
    #Ensure recipe is updated and show_recipe page is rendered
    def test_update_recipe( self ):
        # update recipe document
        recipes_collection.update_one( { '_id' : ObjectId( '0123456789ab0123456789ab' ) } , { "$set" : { 'recipeName' : 'This has been updated' } } , upsert = True )
        # find recipe updated
        recipe = recipes_collection.find_one({'recipeName': 'This has been updated' } )
        # create response variable
        response = self.app.get( '/show_recipe' , follow_redirects = True )
        # ensure correct server response
        self.assertTrue( response, 200 )
        # ensure correct template used
        self.assertTrue(response, 'show_recipe.html')
        # ensure correct recipe content
        self.assertTrue(recipe['recipeName'] == 'This has been updated' )
        # assert correct number of recipe documents
        self.assertEqual( recipes_collection.count() , 2 )
        # assert correct number of user documents
        self.assertEqual( users_collection.count() , 1 )
    
    # Ensure show_recipe page loads and shows correct recipe
    def test_show_recipe( self ):
        # create repsonse variable
        response = self.app.get( '/show_recipe' , follow_redirects = True )
        # ensure correct server repsonse
        self.assertTrue( response, 200 )
        # ensure correct template used
        self.assertTrue( response, 'show_recipe.html' )
    
    # Ensure recipe is deleted and index page is returned
    def test_delete_recipe( self ):
        # delete recipe from collection
        recipes_collection.delete_one( { '_id' : ObjectId( '0123456789ab0123456789ab' ) } )
        # create response
        response = self.app.get( '/' , follow_redirects = True )
        # ensure correct server response
        self.assertTrue( response, 200 )
        # ensure correct template used
        self.assertTrue( response, 'index.html' )
        # ensure correct recipe count
        self.assertEqual( recipes_collection.count() , 1 )
        
    #Ensure favourites page loads correctly
    def test_favourites_loads( self ):
        # create response variable
        response = self.app.get( '/favourites' , follow_redirects = True )
        # ensure correct server response
        self.assertTrue( response, 200 )
        # ensure correct template used
        self.assertTrue( response, 'favourites.html' )

if __name__ == '__main__':
    
    unittest.main()