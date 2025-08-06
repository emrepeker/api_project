# This file has required connection tools Engine/SessionLocal
# And has a declarative_base() to inherit and create models tables

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

from sqlalchemy.exc import SQLAlchemyError

SQLACHEMY_DATABASE_URL = "postgresql+psycopg://postgres:Emreemre1441@localhost:5432/fastapi" 

engine = create_engine(SQLACHEMY_DATABASE_URL)
# Database connection test
while True:
   try:
       result = engine.connect().execute(text("SELECT 1"))
       print("Connection is succesfull POSTGRESS", result.scalar())
       break
       
   except SQLAlchemyError as e:
       print("Connection is failed trying again", str(e))
       time.sleep(3)
          
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # it is like stagin are of git

Base = declarative_base() # Bindng SQL to sqlachemy //We can create models tables with inheriting 


#Every time we get request. We will call this function to reach session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    



