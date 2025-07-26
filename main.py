from enum import Enum

from fastapi import FastAPI, Response
from fastapi.params import Body #JSON Body to dict

#############################################     
from pydantic import BaseModel #Schema Check
#############################################


class LogName(str, Enum):
    login = "login"
    logout = "logout"
    sign_in = "sign_in"
#Creating Schema pydantic BaseModel###########
class Post(BaseModel):
    title : str
    content : str
   
##############################################    

################# HARD CODING SOME DATA    #########################
my_posts = [{"title":"title of post 1","content":"content of post 1", "id": 0},
            {"title":"favorite foods","content":"I like pizza","id" : 1}]
##########################################
    
    

app = FastAPI()

@app.get("/log/{log_name}")
async def log_ops(log_name : LogName): 
    if log_name == "login":
        return {"log_name" : log_name, "message": "You at login page"}
    if log_name == "logout":
        return {"log_name" : log_name, "message":"You at logout page"}
    return {"log_name": log_name,"message":"you at sign-in page bye bye "}
#Path parameter : type -> path
@app.get("/files/{file_path:path}")
async def file_ops(file_path : str):
    return {"file_path": file_path} # --> if path parameter has / then files//home/main.py is possible -> unreachable

#Get all posts
@app.get("/posts")
async def get_posts():
    return {"data" : my_posts} #auto serialazition 
#Get certain post with id
@app.get("/posts/{id}")
async def get_post(id : int,response : Response):
    if id > my_posts[len(my_posts) - 1]["id"] or id < 0:
        response.status_code = 404
        return {"404 Error":"There is no post with this is ID"}                          #Need to return otherwise it doesn't stop
    return {id : my_posts[id]}



@app.post("/posts")
async def create_post(post : Post):
    my_posts.append(post.model_dump()) # post -> dict
    #unique id 
    leng = len(my_posts)
    my_posts[leng -1]["id"] = my_posts[leng -2]["id"] + 1
    print(my_posts)
    return {"data" : my_posts[leng - 1]}
        
    





#Query parameters 
@app.get("/items") 
async def get_page(skip : int = 0, limit : int = 10):
    return {"message" : f"{skip}" + " Other " + f"{limit}"}