# use several imported functions from sqlalchemy to create the following three important variables:
    # The engine variable manages the overall connection to the database.
    # The Session variable generates temporary connections for performing create, read, update, and delete (CRUD) operations.
    # The Base class variable helps us map the models to real MySQL tables.
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g

load_dotenv()

# connect to database using env variable
# Note that the getenv() function is part of Python's built-in os module. 
# But because we used a .env file to fake the environment variable, we need to first call load_dotenv() from the python-dotenv module. 
# In production, DB_URL will be a proper environment variable.
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# We're using the same Base.metadata.create_all() method from the seeds.py file, but we won't call it until after we've called init_db(). 
# So when would be a good time to call init_db()? When the Flask app is ready!
def init_db(app):
  Base.metadata.create_all(engine)
    # Now Flask will run close_db() together with its built-in teardown_appcontext() method. 
    # Note that we added app as a parameter of the init_db() function. We need to make sure that the variable gets passed in correctly.
  app.teardown_appcontext(close_db)

# Whenever this function is called, it returns a new session-connection object. 
# Other modules in the app can import Session directly from the db package, but using a function means that we can perform additional logic before creating the database connection.
# get_db() function now saves the current connection on the g object, if it's not already there. 
# Then it returns the connection from the g object instead of creating a new Session instance each time.
def get_db():
  if 'db' not in g:
    # store db connection in app context
    g.db = Session()

  return g.db
# For instance, if get_db() is called twice in the same route, we won't want to create a second connection. Rather, it will make more sense to return the existing connection.

# pop() method attempts to find and remove db from the g object. If db exists (that is, db doesn't equal None), then db.close() will end the connection
# close_db() function won't run automatically, though. We need to tell Flask to run it whenever a context is destroyed
def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()