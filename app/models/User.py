# import statement
from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
import bcrypt

# want to directly use the bcrypt module, so this time, the import syntax differs a bit. The first thing we need to do is create a salt to hash passwords against.
salt = bcrypt.gensalt()
# created a User class that inherits from the Base class
# earlier, we created Base as part of the db package. In the User class, we declare several properties that the parent Base class will use to make the table. 
# use classes from the sqlalchemy module to define the table columns and their data types
# can also give options to each column, like nullable=False, which will become a SQL NOT NULL
class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False, unique=True)
  password = Column(String(100), nullable=False)
    # add a new validate_email() method to the class that a @validates('email') decorator wraps
    # validate_email() method returns what the value of the email column should be, and the @validates() decorator internally handles the rest
    # This decorator is similar to the @bp.routes() decorator that we used previously to handle the route functions
    # validate_email() method uses the assert keyword to check if an email address contains an at-sign character (@)
    # assert keyword automatically throws an error if the condition is false, thus preventing the return statement from happening
  @validates('email')
  def validate_email(self, key, email):
    # make sure email address contains @ character
    assert '@' in email

    return email

  # validation for the password
  # use assert to check the length of the password and throw an error if it has fewer than four characters
  @validates('password')
  def validate_password(self, key, password):
    assert len(password) > 4

    # encrypt password
    # validate_password() function now returns an encrypted version of the password, if the assert doesn't throw an error.
    return bcrypt.hashpw(password.encode('utf-8'), salt)