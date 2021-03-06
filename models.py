
""" MODULE IMPORT """

from flask_login import UserMixin
from ming        import Document, Field, schema, Session
from ming.odm    import Mapper
    
# Create db session    
session = Session()

""" SCHEMA CREATION """

# Create recipe schema
class recipes(Document):
    class __mongometa__:
        session = session
        name = 'recipe'
    _id = Field(schema.ObjectId)
    recipeName = Field(schema.String)
    recipeAuthor = Field(schema.String)
    recipeCuisine = Field(schema.String)
    recipeCountryOfOrigin = Field(schema.String)
    recipeMealTime = Field(schema.String)
    recipeServings = Field(schema.String)
    recipeDifficulty = Field(schema.String)
    recipePreparationTime = Field(int)
    recipeCookingTime = Field(int)
    recipeAllergen = Field(schema.Array(str))
    recipeMainIngredient = Field(schema.String)
    recipeIngredients = Field(schema.String)
    recipeInstructions = Field(schema.String)
    recipeDietary= Field(schema.Array(str))
    recipeUpvotes = Field(int)
    recipeImageLink = Field(schema.String)
    recipeEmail = Field(schema.String)

# Create user schema   
class users(UserMixin, Document):
    class __mongometa__:
        session = session
        name = 'user'
    _id = Field(schema.ObjectId)
    username = Field(str)
    email = Field(str)
    password = Field(str)
    favouriteRecipes = Field(schema.Array(str))
    myRecipes = Field(schema.Array(str))
    likedRecipes = Field(schema.Array(str))

# Compile schemas
Mapper.compile_all()
