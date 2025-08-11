from fastapi import Response, HTTPException, status, Depends, APIRouter
from fastapi.params import Body
from .. import schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)

## USER API ##

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)) -> schemas.UserOut: 
    #Save hashed passport
    user.password = utils.hash(user.password)
    
    user_dict = user.model_dump()
    new_user = models.Users(**user_dict)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)




    return new_user

## GET USER with ID

@router.get('/{id}',response_model = schemas.UserOut)
async def get_user(id : int, db : Session = Depends(get_db)):
                                                               #dont make .all() creates parsing problems
    user = db.query(models.Users).filter(models.Users.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The id you are looking for: {id} is not valid")   
    
    
    return user