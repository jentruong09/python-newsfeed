# import the functions Blueprint() and render_template() from the Flask module
from flask import Blueprint, render_template
from app.models import Post
from app.db import get_db

# Blueprint() lets us consolidate routes onto a single bp object that the parent app can register later. 
# This corresponds to using the Router middleware of Express.js
bp = Blueprint('home', __name__, url_prefix='/')

# define two new functions: index() and login()
# In each case, we add a @bp.route() decorator before the function to turn it into a route.
# Remember, whatever the function returns becomes the response. 
# And this time, we use the render_template() function to respond with a template instead of a string.
@bp.route('/')
def index():
  # get all posts
  # get_db() function returns a session connection that's tied to this route's context. 
  # We then use the query() method on the connection object to query the Post model for all posts in descending order, and we save the results in the posts variable
  db = get_db()
  posts = db.query(Post).order_by(Post.created_at.desc()).all()

  return render_template(
    'homepage.html',
    posts=posts
  )

@bp.route('/login')
def login():
  return render_template('login.html')

# This route uses a parameter. 
# In the URL, <id> represents the parameter. To capture the value, we include it as a function parameter—specifically, single(id)
# Note the <id> route parameter in the decorator function that becomes a function parameter in the single() function. 
# We can use that parameter to query the database for a specific post.
@bp.route('/post/<id>')
def single(id):
  # get single post by id
  db = get_db()
  post = db.query(Post).filter(Post.id == id).one()

  # render single post template
  return render_template(
    'single-post.html',
    post=post
  )
# we use the filter() method on the connection object to specify the SQL WHERE clause, and we end by using the one() method instead of all(). 
# We then pass the single post object to the single-post.html template. 
# Once the template is rendered and the response sent, the context for this route terminates, and the teardown function closes the database connection.