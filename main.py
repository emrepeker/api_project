from fastapi import FastAPI, Response,HTTPException, status
from fastapi.params import Body #JSON Body to dict

#############################################     
from pydantic import BaseModel #Schema Check
#############################################



#Creating Schema pydantic BaseModel###########
class Post(BaseModel):
    title : str
    content : str
   
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
    return {"data" : my_posts} #auto serialazition 

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
    my_posts.append(post.model_dump()) # post -> dict
    #unique id 
    leng = len(my_posts)
    my_posts[leng -1]["id"] = my_posts[leng -2]["id"] + 1
    print(my_posts)
    return {"data" : my_posts[leng - 1]}
        
    





