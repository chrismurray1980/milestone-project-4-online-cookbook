from ming import Document, Field, schema, Session

session = Session()
class add_recipe(Document):

    class __mongometa__:
        session = session
        name = 'recipe'

    _id = Field(schema.ObjectId)
    author = Field(str)
    name = Field(str)