from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import LoginCredential
from ..models import Users
from ..utils import verify
from ..oauth import create_acces_token
from ..schemas import Token

router = APIRouter(
    tags = ['Authentication']
)



@router.post('/login', response_model=Token)             # {"username" : username, "password" : password} -> returns this dict
async def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
            #      OAuth2PasswordRequestForm         
            # email --> username
            # password --> password
            
    user = db.query(Users).filter(
        Users.email == user_credentials.username).first()
    
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    
    if not verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= "Invalid Credentials") 
    
    #To Generate token. First find the mail and then check is password verified then Generate
    
    # generate Token
    token =create_acces_token(data = {"User_id" : user.id})
    # Return
    return {"token" : token, "Token type" : "bearer"}      