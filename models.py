from ming import Document, Field, schema, Session

session = Session()

class recipes(Document):
    class __mongometa__:
        session = session
        name = 'recipe'

    _id = Field(schema.ObjectId)
    author = Field(str)
    name = Field(str)
    country_of_origin = Field(str)
    cuisine = Field(str)
    meal_time = Field(str)
    servings = Field(int)
    difficulty = Field(str)
    cooking_time = Field(int)
    allergen = Field(str)
    main_ingredient = Field(str)
    ingredients = Field(str)
    instructions = Field(str)
    dietary = Field(str)
    upvotes = Field(int)
    image_link = Field(str)
    
    
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
    
    
    
    