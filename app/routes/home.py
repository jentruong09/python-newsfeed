# import the functions Blueprint() and render_template() from the Flask module
from flask import Blueprint, render_template

# Blueprint() lets us consolidate routes onto a single bp object that the parent app can register later. 
# This corresponds to using the Router middleware of Express.js
bp = Blueprint('home', __name__, url_prefix='/')

# define two new functions: index() and login()
# In each case, we add a @bp.route() decorator before the function to turn it into a route.
# Remember, whatever the function returns becomes the response. 
# And this time, we use the render_template() function to respond with a template instead of a string.
@bp.route('/')
def index():
  return render_template('homepage.html')

@bp.route('/login')
def login():
  return render_template('login.html')

# This route uses a parameter. 
# In the URL, <id> represents the parameter. To capture the value, we include it as a function parameter—specifically, single(id)
@bp.route('/post/<id>')
def single(id):
  return render_template('single-post.html')