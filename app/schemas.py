from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


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
        
        
        
        
## USER SCHEMAS ##

class User(BaseModel):
    email : EmailStr
    password : str
    
    
class UserCreate(User):
    pass


### USER RESPONSE ##

class UserOut(BaseModel):
    email : EmailStr
    id : int
    created_at : datetime
    class Congif:
        from_attributes = True
        
## Login
class LoginCredential(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    acces_token : str 
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None 
   
