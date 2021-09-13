import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

database_name = "tristan"
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']

database_uri = "postgresql://{}:{}@{}/{}".format(db_user, db_pass,
                                                 'localhost:5432', database_name)

SQLALCHEMY_DATABASE_URI = database_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
