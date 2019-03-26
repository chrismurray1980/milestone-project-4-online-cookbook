import os

test_config=True

if test_config:
    connection_config= 'mim://localhost/test'
else:
    connection_config = os.getenv("MONGO_URI",'mongodb://localhost')
