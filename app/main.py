from fastapi import FastAPI, Response,HTTPException, status, Depends 
from fastapi.params import Body #JSON Body to dict
import psycopg # Python -> PostgreSQL Connection Library
from psycopg.rows import dict_row # To Return Column Names 
import time # to delay while
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

import sqlalchemy # ORM style database controller
from sqlalchemy import create_engine, text # Object for establishing connection

#############################################     
from pydantic import BaseModel #Schema Check
#############################################



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
        print("Database connection is established")
        break
    except Exception as error:
        print("Connection to database is failed")
        print("Error : ", error)
        time.sleep(2)





#Creating Schema pydantic BaseModel###########
class Post(BaseModel):
    title : str
    content : str
    published : bool =  True # defalult to  True if doesnt passed by user

   
##############################################    

    
    

app = FastAPI()


#Path parameter : type -> path
@app.get("/files/{file_path:path}")
async def file_ops(file_path : str):
    return {"file_path": file_path} # --> if path parameter has / then files//home/main.py is possible -> unreachable

#SQLalchemy setup TEST
@app.get("/sqlalchemy")
async def test_alchemy(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"This is a test" : posts}



#Get all posts
@app.get("/posts")
async def get_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()    
    # cursor.execute("""SELECT * FROM posts """) 
    # posts = cursor.fetchall()
    print(posts)
    return {"data" : posts} #auto serialazition 

#Get certain post with id
@app.get("/posts/{id}")
async def get_post(id : int, db : Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first() # Better than all() cuz it finishes search after first hit
    
    if not post : #Error Part
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The ID: {id} is not valid")
    else:        #No Error, RETURN
        return {"The post is :" : post}    




    # cursor.execute("""SELECT EXISTS (SELECT 1 FROM posts WHERE id = %s ) """, (id,)) # Returns dict true or false
    # result = cursor.fetchone()
    # exists = result['exists'] # --> boolean value
    
    # if exists:
    #     #logic
    #     cursor.execute("""SELECT * FROM posts WHERE id = %s """,(id,)) # Important to pass , after !!!
    #     my_row = cursor.fetchone()
    #     return {"The post : " : my_row}
    # else:
    #     #error message no content with that ID    
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"This {id} is not in the database")
        
    
    

#Need to pass status code to path decorator
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post : Post, db: Session = Depends(get_db)):
    
    post_dict = post.model_dump()
    new_post = models.Post(**post.model_dump()) # Using unpacking for dictionary ->'title':post.tile ->  title=post.title ** mapping is good for passing as parameter
    db.add(new_post) # Saving Row to database
    db.commit() # Comitting the change
    db.refresh(new_post) # Getting back new_post / prevents Flushing
    
    
    #with approach like you need to write as much code as your length of column numbers
    # new_post = models.Post(title = post.title, content = post.content, published = post.published) #Returns a row to save later
    return{"Succesful Add" : new_post}
    
    
    ############################# RAW SQL IMPLEMENTATION  ######################################3
    # post_dict = post.model_dump()  # post -> dict
        
    # title = post_dict["title"]      # Data Save
    # content = post_dict["content"]
    # published = post_dict["published"]
    
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *; """,(title, content, published)) # SQL Injection protected
    
    # new_post = cursor.fetchone() # Fetch returning data
    # conn.commit() # Commit database changes
    
    # return {"data" : new_post}        


#Delete spesific post
@app.delete("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_post(id : int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""",(id,))
    
    deleted_post = cursor.fetchone()
    conn.commit()
    return {"Succesfully Deleted " : deleted_post }
    


#Update Spesific post
@app.put("/posts/{id}")
async def update_post(id :int, post : Post):
    post_dict = post.model_dump()
    cursor.execute("""UPDATE posts SET title = %s, content=%s, published=%s  WHERE id = %s  RETURNING *;""", (post_dict['title'], post_dict['content'],post_dict['published'] ,id))
    
    updated_post = cursor.fetchone()
    conn.commit()
    return {"This Post is updated" : updated_post}
    

#Patch Spesific post
@app.patch("/posts/{id}")      
async def patch_post(id: int, post : dict = Body(...)):
    print(post.keys())
    
    #Update Given values
    for column in post.keys():
        cursor.execute(f"""UPDATE posts SET {column} = %s WHERE id = %s RETURNING *; """, (post[column],id))
        print(column + " Succesfully updated")
        
    patched_post = cursor.fetchone()
    conn.commit()
    return {"This Post is Updated": patched_post}
        
    
         
        
         
        
    





