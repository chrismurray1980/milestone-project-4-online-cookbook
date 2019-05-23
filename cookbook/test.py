import unittest

from flask_testing      import TestCase

from app                import app , session, recipes_collection

from models             import recipes , users

from bson.objectid      import ObjectId

from bson.json_util     import dumps 



# Create flask test case class 

class FlaskTestCase( TestCase ):
    
    
    
    # Create app for test 
    
    def create_app( self ):
        
        app.config[ 'TESTING' ] = True
        
        return app
    
    
    
    # Create test setup 
    
    def setUp( self ):
        
        objectId_1 = ObjectId( '0123456789ab0123456789ab' )
        
        objectId_2 = ObjectId( '0123456789ab0123456789ad' )
        
        recipes_collection.insert_one( recipes.make( dict( _id=objectId_1 , recipeName = 'test this document' , recipeUpvotes = 15 , recipeCuisine = 'Mexican' ) ) )
        
        recipes_collection.insert_one( recipes.make( dict( _id=objectId_2 , recipeName = 'test another document' , recipeUpvotes = 15 , recipeCuisine = 'Italian' ) ) )
    
    
    
    
    # Tear down test setup 
    
    def tearDown( self ):
        
        recipes_collection.delete_many( {} )
        
        session.clear()
        
    
         
    # Test database used
    
    def test_database( self ):
        
        self.assertTrue( app.config[ 'MONGO_URI' ] , 'mim://localhost/test' )
    
    
    
    # Ensure index page loads, contains recipe data and converts cursor to json string
    
    def test_get_recipes( self ):
        
        response = self.client.get( '/' , follow_redirects = True )
        
        data = dumps( recipes_collection.find() )
        
        self.assert200( response )
        
        self.assertTemplateUsed( 'index.html' )
        
        self.assertIn( b'test this document' , response.data )
        
        self.assertEqual( recipes_collection.count() , 2 )
        
        self.assertTrue( type( data ) , 'str' )



    # Ensure search results page loads and contains recipe data 
    
    def test_search( self ):
        
        search_text = 'test this document'
        
        data = recipes_collection.find( { 'recipeName' : search_text } )
        
        for document in data: 
            
            return document[ 'recipeName' ]
            
        response = self.client.get( '/search_results/test this document' , follow_redirects = True , data = document[ 'recipeName' ])
        
        self.assert200( response )
        
        self.assertTemplateUsed( 'search_results.html' )
        
        self.assertIn( b'test this document' , response.data )
        
        self.assertEqual( recipes_collection.count() , 2 )



    # Ensure search results page loads and contains recipe data for advanced search
        
    def test_advanced_search( self ):
        
        data = recipes_collection.find( { 'recipeCuisine' : 'Italian' } )
        
        for document in data: 
            
            return document[ 'recipeCuisine' ]
        
        response = self.client.get( "/search_results/[{'recipeCuisine': 'Italian'}]" , follow_redirects = True , data =  document[ 'recipeCuisine' ] )  
        
        self.assert200( response )
        
        self.assertTemplateUsed( 'search_results.html' )
        
        self.assertIn( b'Italian' , response.data )
        
        self.assertEqual( recipes_collection.count() , 2 )
        
        
            
    # Ensure add_recipe page loads correctly 
    
    def test_add_recipe( self ):
        
        response = self.client.get( '/add_recipe' , follow_redirects = True )
        
        self.assert200( response )
        
        self.assertTemplateUsed( 'add_recipe.html' )
        
        
    
    # Ensure insert recipe works correctly and show_recipe page is then rendered
    
    def test_insert_recipe( self ): 
        
        objectId = ObjectId( '0123456789ab0123456789ac' )
        
        recipes_collection.insert_one( recipes.make( dict( _id = objectId , recipeName = 'test insert document' ) ) )
        
        response = self.client.get( '/show_recipe/0123456789ab0123456789ac' , follow_redirects = True )
        
        self.assert200( response )
        
        self.assertTemplateUsed( 'show_recipe.html' )
        
        self.assertIn( b'test insert document' , response.data )
        
        self.assertEqual( recipes_collection.count() , 3 )
        
        
    
    # Ensure edit_delete_recipe page loads with correct recipe_id
    
    def test_edit_delete_recipe( self ):
        
        response = self.client.get( '/edit_delete_recipe/0123456789ab0123456789ab' , follow_redirects = True )
        
        self.assert200( response )
        
        self.assertTemplateUsed( 'edit_delete_recipe.html' )
        
        self.assertIn( b'test this document' , response.data )
        
        
    
    #Ensure recipe is updated and show_recipe page is rendered
    
    def test_update_recipe( self ):
        
        recipes_collection.update_one( { '_id' : ObjectId( '0123456789ab0123456789ab' ) } , { "$set" : { 'recipeName' : 'This has been updated' } } , upsert = True )
        
        response = self.client.get( '/show_recipe/0123456789ab0123456789ab' , follow_redirects = True )
        
        self.assert200( response )
        
        self.assertTemplateUsed( 'show_recipe.html' )
        
        self.assertIn( b'This has been updated' , response.data )
        
        self.assertEqual( recipes_collection.count() , 2 )
        
        
    
    # Ensure show_recipe page loads and shows correct recipe
    
    def test_show_recipe( self ):
        
        response = self.client.get( '/show_recipe/0123456789ab0123456789ab' , follow_redirects = True )
        
        self.assert200( response )
        
        self.assertTemplateUsed( 'show_recipe.html' )
        
        self.assertIn( b'test this document' , response.data )
        
        
    
    # Ensure recipe is deleted and index page is returned
    
    def test_delete_recipe( self ):
        
        recipes_collection.delete_one( { '_id' : ObjectId( '0123456789ab0123456789ab' ) } )
        
        response = self.client.get( '/' , follow_redirects = True )
        
        self.assert200( response )
        
        self.assertTemplateUsed( 'index.html' )
        
        self.assertEqual( recipes_collection.count() , 1 )
        
        
    
    #Ensure favourites page loads correctly
    
    def test_favourites_loads( self ):
        
        response = self.client.get( '/favourites' , follow_redirects = True )
        
        self.assert200( response )
        
        self.assertTemplateUsed( 'favourites.html' )
        
        
        
if __name__ == '__main__':
    
    unittest.main()