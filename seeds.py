from app.models import User, Post, Comment, Vote
from app.db import Session, Base, engine

# uses the Base class together with the engine connection variable to do two things: drop and rebuild tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Anytime we want to perform a CRUD operation using SQLAlchemy, we need to establish a temporary session connection with the Session class.
db = Session()

# Within this db session object, we use the add_all() method and the User model to create several new users.
# insert users
db.add_all([
  User(username='alesmonde0', email='nwestnedge0@cbc.ca', password='password123'),
  User(username='jwilloughway1', email='rmebes1@sogou.com', password='password123'),
  User(username='iboddam2', email='cstoneman2@last.fm', password='password123'),
  User(username='dstanmer3', email='ihellier3@goo.ne.jp', password='password123'),
  User(username='djiri4', email='gmidgley4@weather.com', password='password123')
])

db.commit()
# Note that db.add_all() alone doesn't change the database. In fact, it only preps the SQL queries. To run the INSERT statements, you need to call db.commit(). 
# If you don't need to make any other database transactions at this time, you can close the session connection by calling db.close().

# insert posts
# important to run this add_all() method after creating the users, because the Post model requires valid user_id fields
# also need to run db.commit() again to confirm these latest insertions in the database
db.add_all([
  Post(title='Donec posuere metus vitae ipsum', post_url='https://buzzfeed.com/in/imperdiet/et/commodo/vulputate.png', user_id=1),
  Post(title='Morbi non quam nec dui luctus rutrum', post_url='https://nasa.gov/donec.json', user_id=1),
  Post(title='Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue', post_url='https://europa.eu/parturient/montes/nascetur/ridiculus/mus/etiam/vel.aspx', user_id=2),
  Post(title='Nunc purus', post_url='http://desdev.cn/enim/blandit/mi.jpg', user_id=3),
  Post(title='Pellentesque eget nunc', post_url='http://google.ca/nam/nulla/integer.aspx', user_id=4)
])

db.commit()

# insert comments
db.add_all([
  Comment(comment_text='Nunc rhoncus dui vel sem.', user_id=1, post_id=2),
  Comment(comment_text='Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est.', user_id=1, post_id=3),
  Comment(comment_text='Aliquam erat volutpat. In congue.', user_id=2, post_id=1),
  Comment(comment_text='Quisque arcu libero, rutrum ac, lobortis vel, dapibus at, diam.', user_id=2, post_id=3),
  Comment(comment_text='In hac habitasse platea dictumst.', user_id=3, post_id=3)
])

db.commit()

# insert votes
db.add_all([
  Vote(user_id=1, post_id=2),
  Vote(user_id=1, post_id=4),
  Vote(user_id=2, post_id=4),
  Vote(user_id=3, post_id=4),
  Vote(user_id=4, post_id=2)
])

db.commit()

db.close()