from ming.declarative import Document 
from ming import Field, Session
from ming.odm import Mapper

session = Session()

class recipes(Document):
    class __mongometa__:
        session = session
        name = 'recipe'

    _id = Field(str)
    recipeName = Field(str, index=True)
    recipeAuthor = Field(str)
    recipeCuisine = Field(str)
    recipeCountryOfOrigin = Field(str)
    recipeMealTime = Field(str)
    recipeServings = Field(str)
    recipeDifficulty = Field(str)
    recipePreparationTime = Field(str)
    recipeCookingTime = Field(str)
    recipeAllergen = Field(str)
    recipeMainIngredient = Field(str, index=True)
    recipeIngredients = Field(str, index=True)
    recipeInstructions = Field(str)
    recipeDietary= Field(str)
    recipeUpvotes = Field(str)
    recipeImageLink = Field(str)
    
    
class users(Document):
    class __mongometa__:
        session = session
        name = 'user'

    _id = Field(str)
    user_name = Field(str)
    email = Field(str)
    password = Field(str)
    my_recipes = Field(str)
    favourite_recipes = Field(str)
    my_filters = Field(str)
    

Mapper.compile_all() 

