from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from .schemas import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY arbitary long string
#Hashing Algo HS256
#Expriration time

# To Get string like this run openssl rand -hex 32
SECRET_KEY = "c07843915733c7c8175f1e9c404edda14a4cff0664f98676d6ca4e5f23e2d8dc"
ALGORITHM = "HS256"
ACCES_TOKEN_EXPIRE_MINUTES = 30

def create_acces_token(data : dict): # it is possible to make data a Schema -> Precise payload
    to_encode = data.copy()
    #Time when token will expire
    expire = datetime.now(timezone.utc) + timedelta(minutes= ACCES_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp" : expire})
                                                # Dont Pass list [ALGORITHM] XXXX
    encoded_jwt= jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    
    return encoded_jwt

def verify_acces_token(token :str , credentials_exception):
    try:
        decoded_data =jwt.decode(token, SECRET_KEY, ALGORITHM)
        
        id : str = decoded_data.get("User_id")
       
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id) #Validate token schema
    except JWTError:
        raise credentials_exception    
    return token_data
    
# Pass it into path ops func to expect a token get_current_user : int Depends(oauth2.get_current_user)
def get_current_user(token : Annotated[str,Depends(oauth2_scheme)]):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    
    return verify_acces_token(token, credentials_exception=credentials_exception) # Returns schemas.TokenData. No Error --> Check