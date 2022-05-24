# import statements
from datetime import datetime
from app.db import Base
from .Vote import Vote
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, select, func
from sqlalchemy.orm import relationship, column_property

# post class - SQLAlchemy models as Python classes
class Post(Base):
  __tablename__ = 'posts'
  id = Column(Integer, primary_key=True)
  title = Column(String(100), nullable=False)
  post_url = Column(String(100), nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'))
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
  user = relationship('User')
  comments = relationship('Comment', cascade='all,delete')
  votes = relationship('Vote', cascade='all,delete')
  # Post model now has two defined relationships: one for users and one for comments
  # Querying for a post returns both data subsets
  # the model for comments also defines a relationship, querying for a post returns the comment-to-user subset as well

  # query the model, this dynamic property will perform a SELECT, together with the SQLAlchemy func.count() method, to add up the votes
  vote_count = column_property(
    select([func.count(Vote.id)]).where(Vote.post_id == id)
  )
  
# note the user_id field that we define as a ForeignKey that references the users table. 
# also add created_at and updated_at fields that use Python's built-in datetime module to generate the timestamps.

# Post model includes a dynamic property for votes, meaning that a query for a post should also return information about the number of votes the post has. 
# We also want to make sure that when we delete a post from the database, every vote associated is subsequently deleted