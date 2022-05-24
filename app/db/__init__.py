# use several imported functions from sqlalchemy to create the following three important variables:
    # The engine variable manages the overall connection to the database.
    # The Session variable generates temporary connections for performing create, read, update, and delete (CRUD) operations.
    # The Base class variable helps us map the models to real MySQL tables.
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# connect to database using env variable
# Note that the getenv() function is part of Python's built-in os module. 
# But because we used a .env file to fake the environment variable, we need to first call load_dotenv() from the python-dotenv module. 
# In production, DB_URL will be a proper environment variable.
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()