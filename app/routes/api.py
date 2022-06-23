from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db
import sys

# define all the API endpoints for the app
bp = Blueprint('api', __name__, url_prefix='/api')

# add a new route that will resolve to /api/users, and we specify the method to be of type POST - route is to receive data
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  # try block now contains the user creation, and if it fails, the except block will send a JSON error message to the front end. 
  # At the same time, we set the response status code to 500 to indicate that a server error occurred
  try:
    # attempt creating a new user
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )

    # save in database
    # these changes, we use the db.add() method to prep the INSERT statement and the db.commit() method to officially update the database
    db.add(newUser)
    db.commit()
  except:
    # insert failed, so send error to front end
    print(sys.exe_info()[0])
    # insert failed, so rollback and send error to front end
    # you won't see the benefits of calling db.rollback() in your local environment, but doing so ensures that the database won't lock up when deployed to Heroku. 
    # The good news is that this signup route is now completely resistant to failure.
    db.rollback()
    return jsonify(message = 'Signup failed'), 500

  # This clears any existing session data and creates two new session properties: 
  # a user_id to aid future database queries and a Boolean property that the templates will use to conditionally render elements.
  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True  

  return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()

  # If the email exists, then we need to verify the password. The password in the database is hashed, though, so we can't do a one-to-one comparison. We need to decrypt it.
  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])

    return jsonify(message = 'Incorrect credentials'), 400

  # Note that data['password'] becomes the second parameter in the verify_password() method of the class, because the first parameter is reserved for self
  # login() route will return a 400 status code if the posted email can't be found or if the posted password doesn't match. 
  # If neither happens, we can safely assume that the credentials are correct and thus create the session.
  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400

  # following code to create the session and send back a valid response
  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True

  return jsonify(id = user.id)