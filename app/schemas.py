from pydantic import BaseModel
from datetime import datetime


#Creating Schema pydantic BaseModel###########
class PostBase(BaseModel):
    title : str
    content : str
    published : bool =  True # defalult to  True if doesnt passed by user

   
##############################################    
class PostCreate(PostBase):
    pass



############ RESPONSE MODELS ####################

class Post(PostBase):
    id : int
    created_at : datetime  
    class Config:
        from_attributes = True
