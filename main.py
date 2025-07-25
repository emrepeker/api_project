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
class PostDataSchema(BaseModel):
    title : str
    content : str
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

#Creating a post method 

@app.post("/createpost")
async def create(payLoad : dict = Body(...)):  # JSON Body will converted into dictionary
    return { "new_post" : f"title:  {payLoad['title']}" +    f" content: {payLoad['content']}"}
#Using Schema in Post method #####################
@app.post("/schematest")
async def schema(post : PostDataSchema):
    print(post)
    return {"New Post":"New post is created"}
##################################################

#Query parameters 
@app.get("/items") 
async def get_page(skip : int = 0, limit : int = 10):
    return {"message" : f"{skip}" + " Other " + f"{limit}"}