from fastapi import FastAPI, Response,HTTPException, status, Depends, APIRouter 
from fastapi.params import Body #JSON Body to dict
import psycopg # Python -> PostgreSQL Connection Library
from psycopg.rows import dict_row # To Return Column Names 
import time # to delay while
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .router import post, user, login





import sqlalchemy # ORM style database controller
from sqlalchemy import create_engine, text # Object for establishing connection

#Creates tables under models
models.Base.metadata.create_all(bind=engine) 
#Base.metadata is collection of tables definitons that inherited from Base class class Name(Base)




    


# while True:
#     try:
#         engine = create_engine("postgresql+psycopg://postgres:Emreemre1441@localhost:5432/fastapi") 
#         #TEST CONNECTIVITY
#         engine_connect = engine.connect()
#         result = engine_connect.execute(text("SELECT "))
#         print(result.scalar)
#         print("sqlalchemy -> postgress connection is established")
#         break
#     except Exception as error:
#         print("SQLalchemy -> Postgres DATABASE Connection failed")
#         print("Error :", error)
#         time.sleep(3)    






    


while True:  # try until we get a database connection   
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='Emreemre1441', row_factory=dict_row) # Bad practice to push this git repo
        cursor = conn.cursor() # cursor is used to use database ops
        print("Database connection is established POSTGRESS")
        break
    except Exception as error:
        print("Connection to database is failed")
        print("Error : ", error)
        time.sleep(2)







    
    

app = FastAPI()
## ROUTING OPS ### 
router = APIRouter()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(login.router)


#Path parameter : type -> path
@app.get("/files/{file_path:path}")
async def file_ops(file_path : str):
    return {"file_path": file_path} # --> if path parameter has / then files//home/main.py is possible -> unreachable



 


