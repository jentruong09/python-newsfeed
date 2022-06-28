from flask import session, redirect
from functools import wraps

# functools module contains several helper functions that we can use to change other functions. 
# In fact, the wraps() function that we imported is a decorator itself! Let's find out exactly what that means
def login_required(func):
  @wraps(func)
  def wrapped_function(*args, **kwargs):
    # if logged in, call original function with original arguments
    if session.get('loggedIn') == True:
      return func(*args, **kwargs)

    return redirect('/login')
  
  return wrapped_function
# A decorator is intended to return a new function—hence, we have the wrapped_function(). 
# However, by returning a new function, we change the internal name of the original function. 
# To clarify, printing callback.__name__ prints wrapped_function instead of callback. 
# That might not seem serious, but it can make debugging harder. Thankfully, the @wraps(func) decorator preserves the original name when creating the wrapped function.

# want to preserve not only the name but any arguments that the original function received. 
# For example, callback('data') should translate to func('data') when called inside the decorator. 
# The *args and **kwargs keywords ensure that no matter how many arguments are given (if any), the wrapped_function() captures them all

# ultimate goal of the Python decorator that we're building is to redirect a user who isn't logged in (that is, 
# a user for whom no session exists) or to run the original route function for a user who is logged in