from fastapi import FastAPI, Response,HTTPException, status
from fastapi.params import Body #JSON Body to dict
import psycopg
from psycopg.rows import dict_row # To Return Column Names 
import time # to delay while

#############################################     
from pydantic import BaseModel #Schema Check
#############################################

while True:  # try until we get a database connection   
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='Emreemre1441', row_factory=dict_row) # Bad practice to push this git repo
        cursor = conn.cursor() # cursor is used to use database ops
        print("Database connection is established")
        break
    except Exception as error:
        print("Connection to database is failed")
        print("Error : ", error)
        time.sleep(3)





#Creating Schema pydantic BaseModel###########
class Post(BaseModel):
    title : str
    content : str
    published : bool = True

   
##############################################    

################# HARD CODING SOME DATA LATER THIS WILL BE A DATABASE   #########################
my_posts = [{"title":"title of post 1","content":"content of post 1", "id": 0},
            {"title":"favorite foods","content":"I like pizza","id" : 1}]
#################################################################################################
    
    

app = FastAPI()


#Path parameter : type -> path
@app.get("/files/{file_path:path}")
async def file_ops(file_path : str):
    return {"file_path": file_path} # --> if path parameter has / then files//home/main.py is possible -> unreachable

#Get all posts
@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts """) 
    posts = cursor.fetchall()
    print(posts)
    return {"data" : posts} #auto serialazition 

#Get certain post with id
@app.get("/posts/{id}")
async def get_post(id : int):
    if id > my_posts[len(my_posts) - 1]["ixd"] or id < 0: # is id in range
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This ID is not in the posts ID range")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"404 Error":"There is no post with this is ID"}       #Need to return otherwise it doesn't stop
    return {id : my_posts[id]}

#Need to pass status code to path decorator
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post : Post):
    post_dict = post.model_dump()    
    title = post_dict["title"]
    content = post_dict["content"]
    published = post_dict["published"]
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *; """,(title, content, published))
    new_post = cursor.fetchone()
    return {"data" : new_post}        


#Delete spesific post
@app.delete("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_post(id : int):
    if id >= 0 and id <= len(my_posts) - 1: #Valid ID ordered list can cause errors but its good enough for development
        del my_posts[id]
    return {"Deletion Succes" : f"posts with {id} is succesfully deleted" }    


#Update Spesific post
@app.put("/posts/{id}")
async def update_post(id :int, post : Post):
    post = post.model_dump() # post is dict
    if id >= 0 and id <= len(my_posts) - 1:
        my_posts[id] = post
        return {"data": post}
    else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="ID not found")


#Patch Spesific post
@app.patch("/posts/{id}")      
async def patch_post(id: int, post : dict = Body(...)):
    post_dict = post # post -> dict
    print(post_dict)
    if id >= 0 and id <= len(my_posts) - 1:
        for p in post_dict.keys():
            my_posts[id][p] = post_dict[p]
            
    else:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail="Not Valid ID")    
    
    
         
        
         
        
    





