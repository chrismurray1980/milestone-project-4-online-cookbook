from ming import Document, Field, schema, Session
from ming.odm import Mapper

session = Session()

class recipes(Document):
    class __mongometa__:
        session = session
        name = 'recipe'

    _id = Field(schema.ObjectId)
    recipeName = Field(str)
    recipeAuthor = Field(str)
    recipeCuisine = Field(str)
    recipeCountryOfOrigin = Field(str)
    recipeMealTime = Field(str)
    recipeServings = Field(str)
    recipeDifficulty = Field(str)
    recipePreparationTime = Field(str)
    recipeCookingTime = Field(str)
    recipeAllergen = Field(str)
    recipeMainIngredient = Field(str)
    recipeIngredients = Field(str)
    recipeInstructions = Field(str)
    recipeDietary= Field(str)
    recipeUpvotes = Field(str)
    recipeImageLink = Field(str)
    
    
class users(Document):
    class __mongometa__:
        session = session
        name = 'user'

    _id = Field(schema.ObjectId)
    user_name = Field(str)
    email = Field(str)
    password = Field(str)
    my_recipes = Field(str)
    favourite_recipes = Field(str)
    my_filters = Field(str)

Mapper.compile_all()