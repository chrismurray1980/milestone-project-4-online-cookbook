import unittest
import flask
from flask              import Flask, session as user_session, url_for
from flask_testing      import TestCase
from flask_login        import LoginManager
from app                import app , session, recipes_collection, users_collection, User
from models             import recipes , users
from bson.objectid      import ObjectId
from bson.json_util     import dumps 


# Create flask test case class 
class FlaskTestCase(TestCase):

    # Create app for test 
    def create_app( self ):
        app.config[ 'TESTING' ] = True
        app.config[ 'LOGIN_DISABLED' ] = True
        login_manager = LoginManager()
        login_manager.init_app( app )
        return app
    
    # Create test setup 
    def setUp( self ):
        # create mock object id's
        objectId_1 = ObjectId( '0123456789ab0123456789ab' )
        objectId_2 = ObjectId( '0123456789ab0123456789ad' )
        # create mock user document
        users_collection.insert_one(users.make( dict( username = 'chris', email = 'chris@chris', password = 'chris', favouriteRecipes = [ '0123456789ab0123456789ab' ], myRecipes = [], likedRecipes = [] ) ) )
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
        self.assertEqual( app.config[ 'MONGO_URI' ] , 'mim://localhost/test' )
    
    # Ensure index page loads, contains recipe data and converts cursor to json string
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
        
    # Ensure search results page loads and contains recipe data for advanced search
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
      
    # Ensure add_recipe page loads correctly 
    def test_add_recipe( self ):
        # create response variable
        response = self.client.get( '/add_recipe' , follow_redirects = True )
        # ensure correct server response
        self.assert200( response )
        # ensure correct template used
        self.assertTemplateUsed( 'add_recipe.html' )
    
    # Ensure insert recipe works correctly and show_recipe page is then rendered
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
    
    
    #Ensure recipe is updated and show_recipe page is rendered
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
    
    # Ensure show_recipe page loads and shows correct recipe
    def test_show_recipe( self ):
        with app.test_request_context( '/show_recipe/0123456789ab0123456789ad' ):
           response = self.client.get( '/show_recipe/0123456789ab0123456789ad', follow_redirects = True )
           # ensure correct response
           self.assert200( response )
           # ensure correct templaye used
           self.assertTemplateUsed( 'show_recipe.html' )
           # ensure correct data
           self.assertIn( b'test another document', response.data )
    
    # Ensure recipe is deleted and index page is returned
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

if __name__ == '__main__':
    unittest.main()