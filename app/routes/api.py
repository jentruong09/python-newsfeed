from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
import sys
from app.utils.auth import login_required

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


# takes care of the first step: connecting to the database. 
# Because this is a POST route, we can capture the posted data by using the get_json() method and create a new comment by using the returned dictionary. 
# Because the creation of a comment can fail, we want to wrap it in a try...except statement
@bp.route('/comments', methods=['POST'])
@login_required
def comment():
  data = request.get_json()
  db = get_db()

  # comment_text and post_id values come from the front end, but the session stores the user_id value. 
  # Recall that db.commit() performs the INSERT against the database and that db.rollback() discards the pending commit if it fails
  try:
  # create a new comment
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newComment)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Comment failed'), 500
  
  return jsonify(id = newComment.id)


# An upvote creates a new record in the votes table, but the Post model ultimately uses that information. We'll thus define this action as a PUT route for posts.
@bp.route('/posts/upvote', methods=['PUT'])
@login_required
def upvote():
  data = request.get_json()
  db = get_db()

  try:
    # create a new vote with incoming id and session id
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newVote)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Upvote failed'), 500

  return '', 204

# route for creating new posts—a process that closely follows the one that we created for new comments and upvotes
@bp.route('/posts', methods=['POST'])
@login_required
def create():
  data = request.get_json()
  db = get_db()

  try:
    # create a new post
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )

    db.add(newPost)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post failed'), 500

  return jsonify(id = newPost.id)


# create the API route that will update the details of a post. Updating differs from creating a new post, of course, so we'll step through this a bit more slowly
@bp.route('/posts/<id>', methods=['PUT'])
@login_required
def update(id):
  data = request.get_json()
  db = get_db()

  # when you make updates, SQLAlchemy requires you to query the database for the corresponding record, update the record like you'd update a normal object, and then recommit it.
  try:
    # retrieve post and update title property
    post = db.query(Post).filter(Post.id == id).one()
    post.title = data['title']
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204


# API route for deleting posts. Like updating, deleting in SQLAlchemy requires us to first query for the corresponding record. 
# We then pass the returned object to a db.delete() method before committing the change.
@bp.route('/posts/<id>', methods=['DELETE'])
@login_required
def delete(id):
  db = get_db()

  try:
    # delete post from db
    db.delete(db.query(Post).filter(Post.id == id).one())
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204