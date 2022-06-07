# format_date() function expects to receive a datetime object and then use the strftime() method to convert it to a string. 
# The %m/%d/%y format code will result in something like "01/01/20"
def format_date(date):
  return date.strftime('%m/%d/%y')


from datetime import datetime
print(format_date(datetime.now()))

# This code removes all extraneous information from a URL string, leaving only the domain name. 
# Note that the methods we use, like replace() and split(), behave exactly the same as they do in JavaScript
def format_url(url):
  return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]

print(format_url('http://google.com/test/')) # test previous code
print(format_url('https://www.google.com?q=test'))

# address the issue of correctly pluralizing words
def format_plural(amount, word):
  if amount != 1:
    return word + 's'

  return word

print(format_plural(2, 'cat')) # test previous code
print(format_plural(1, 'dog'))