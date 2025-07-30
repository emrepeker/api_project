from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLACHEMY_DATABASE_URL = "postgresql+psycopg://postgres:Emreemre1441@localhost:5432/fastapi" 

engine = create_engine(SQLACHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # it is like stagin are of git

Base = declarative_base() # Bindng SQL to sqlachemy //We can create models tables with inheriting this

