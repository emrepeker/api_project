from enum import Enum

from fastapi import FastAPI
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
    published : bool = True
    rating : int | None = None
##############################################    
    
    

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

@app.get("/posts")
async def get_posts():
    return {"data" : "This is your posts"}



@app.post("/posts")
async def create_post(post : Post):
    print(post)
    print(post.model_dump())
    return {"data" : post}
        
    





#Query parameters 
@app.get("/items") 
async def get_page(skip : int = 0, limit : int = 10):
    return {"message" : f"{skip}" + " Other " + f"{limit}"}