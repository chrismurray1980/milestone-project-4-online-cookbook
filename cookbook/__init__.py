from flask import Flask
import os
from ming               import mim, create_datastore

from ming.odm           import ThreadLocalODMSession , Mapper

from ming.base          import Cursor


app = Flask(__name__)

# Configure application to use either mongodb or mongo-in-memory db 

def database_config_setup( filename ):
    
    database_config = os.getenv( 'MONGO_URI', 'mongodb://localhost' ) if filename == '__main__' else 'mim://localhost/test'
   
    return database_config



app = Flask(__name__)                                                                   # Create flask app

app.config[ 'MONGO_DBNAME' ] = 'onlineCookbook'                                         # Define db name

app.config[ 'MONGO_URI' ] = os.getenv( 'MONGO_URI')                           # Define db URI

app.config[ 'UPLOAD_FOLDER' ] = os.getenv( 'UPLOAD_FOLDER' )                            # Create image upload path

app.config[ 'SECRET_KEY' ] = os.getenv( 'SECRET_KEY' )                                  # Secret key for session

app.config['FLASKS3_BUCKET_NAME'] = os.getenv('FLASKS3_BUCKET_NAME')
app.config['FLASKS3_ACCESS_KEY'] = os.getenv('FLASKS3_ACCESS_KEY')
app.config['FLASKS3_SECRET_ACCESS_KEY'] = os.getenv('FLASKS3_SECRET_ACCESS_KEY')


app.config['FLASKS3_FORCE_MIMETYPE'] = True
app.config['FLASKS3_ACTIVE'] = True


#s3 = boto.connect_s3()

# Retrieve the list of existing buckets
#s3 = boto3.client('s3')
#response = s3.list_buckets()

# Output the bucket names
#print('Existing buckets:')
#for bucket in response['Buckets']:
    #print(bucket["Name"])

session = ThreadLocalODMSession( bind = create_datastore( app.config[ 'MONGO_URI' ] ) ) # Create db session

recipes_collection = session.db.recipes                                                 # Set recipe variable

users_collection = session.db.users                                                     # Set user variable

index_mapper = Mapper.ensure_all_indexes()                                              # Ensure all indexes

drop_index = recipes_collection.drop_index( '$**_text' )                                # Drop search index

create_index = recipes_collection.create_index( [ ( '$**' , 'text' ) ] )                # Create search index


from cookbook import routes , models