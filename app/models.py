# This file has models to create Database object like -> Database table
# Inheriting from base means This table mapped to database Class->DATABASE

from .database import Base
from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(VARCHAR, nullable=False)
    content = Column(VARCHAR, nullable=False)
    published = Column(BOOLEAN, server_default='TRUE',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()')) # -> text() to pass postgresql function
    
    
    