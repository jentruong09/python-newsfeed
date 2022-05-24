from datetime import datetime
from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# comment model includes a dynamic property for user, meaning that a query for a comment should also return information about its author
# want to associate posts and comments so that a query for a post also returns information about any comments on it
class Comment(Base):
  __tablename__ = 'comments'
  id = Column(Integer, primary_key=True)
  comment_text = Column(String(255), nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'))
  post_id = Column(Integer, ForeignKey('posts.id'))
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  user = relationship('User')