from ming import Document, Field, schema, Session

session = Session()

class recipes(Document):
    class __mongometa__:
        session = session
        name = 'recipe'

    _id = Field(schema.ObjectId)
    author = Field(str)
    name = Field(str)
    
class users(Document):
    class __mongometa__:
        session = session
        name = 'user'

    _id = Field(schema.ObjectId)
    author = Field(schema.String)
    name = Field(schema.String)