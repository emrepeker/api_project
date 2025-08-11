from fastapi import Response, HTTPException, status, Depends, APIRouter
from fastapi.params import Body
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/posts",
    tags = ['Posts']
)

#Get all posts
@router.get("/")
async def get_posts(db : Session = Depends(get_db)) -> list[schemas.Post]:
    posts = db.query(models.Post).all()    
    # cursor.execute("""SELECT * FROM posts """) 
    # posts = cursor.fetchall()
    print(posts)
    return posts #auto serialazition 

#Get certain post with id
@router.get("/{id}")
async def get_post(id : int, db : Session = Depends(get_db)) -> schemas.Post:
    
    post = db.query(models.Post).filter(models.Post.id == id).first() # Better than all() cuz it finishes search after first hit
    
    if not post : #Error Part
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"The ID: {id} is not valid")
    else:        #No Error, RETURN
        return post                              
                                                                      




    # cursor.execute("""SELECT EXISTS (SELECT 1 FROM posts WHERE id = %s ) """, (id,)) # Returns dict true or false
    # result = cursor.fetchone()
    # exists = result['exists'] # --> boolean value
    
    # if exists:
    #     #logic
    #     cursor.execute("""SELECT * FROM posts WHERE id = %s """,(id,)) # Important to pass , after !!!
    #     my_row = cursor.fetchone()
    #     return {"The post : " : my_row}
    # else:
    #     #error message no content with that ID    
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"This {id} is not in the database")
        
    
    

#Need to pass status code to path decorator
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(post : schemas.PostCreate, db: Session = Depends(get_db)) -> schemas.Post:  # New version gets response models like this
    
    post_dict = post.model_dump()
    new_post = models.Post(**post.model_dump()) # Using unpacking for dictionary ->'title':post.tile ->  title=post.title ** mapping is good for passing as parameter
    db.add(new_post) # Saving Row to database
    db.commit() # Comitting the change
    db.refresh(new_post) # Getting back new_post / prevents Flushing
    
    
    #with approach like you need to write as much code as your length of column numbers
    # new_post = models.Post(title = post.title, content = post.content, published = post.published) #Returns a row to save later
    return new_post
    
    
    ############################# RAW SQL IMPLEMENTATION  ######################################3
    # post_dict = post.model_dump()  # post -> dict
        
    # title = post_dict["title"]      # Data Save
    # content = post_dict["content"]
    # published = post_dict["published"]
    
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *; """,(title, content, published)) # SQL Injection protected
    
    # new_post = cursor.fetchone() # Fetch returning data
    # conn.commit() # Commit database changes
    
    # return {"data" : new_post}        


#Delete spesific post
@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_post(id : int, db : Session = Depends(get_db)):
    
    
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The ID: {id} is not valid")
    
    
    post.delete(synchronize_session=False)
    db.commit()
    
    
    #No content Response
    return Response(status_code=status.HTTP_204_NO_CONTENT)    
    
    ####################### RAW SQL  ####################
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""",(id,))
    
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # return {"Succesfully Deleted " : deleted_post }
    


#Update Spesific post
@router.put("/{id}")
async def update_post(id :int, post : schemas.PostCreate, db : Session = Depends(get_db)) -> schemas.Post:
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"This ID: {id} is not valid")
    post_dict = post.model_dump()    
    
    post_query.update(post_dict, synchronize_session=False) # need to pass dict
    
    db.commit()
    
    return post_query.first()
    # post_dict = post.model_dump()
    # models.Post.update().where(models.Post.id == id).values(**post_dict)
    
    # post_dict = post.model_dump()
    # cursor.execute("""UPDATE posts SET title = %s, content=%s, published=%s  WHERE id = %s  RETURNING *;""", (post_dict['title'], post_dict['content'],post_dict['published'] ,id))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    # return {"This Post is updated" : updated_post}
    

#Patch Spesific post
@router.patch("/{id}")      
async def patch_post(id: int, post = Body(...), db : Session = Depends(get_db)):
    ##UNSECURE##
    # post = post.model_dump()
    # #I belive this is unsecure any content of the post can be anyting
    # post_query = db.query(models.Post).filter(models.Post.id == id)  #Getting the Row
    
    # if post_query.first() is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"The given id : {id} is not valid")
    
    # post_query.update(post,synchronize_session=False)
    
    # db.commit()
    
    
    # return {"data": post_query.first() }


    ###### Alternative Solution for security ####### Get all valid values
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"The given id : {id} is not valid")
        
        
    bucket_dict = {}
    #complexity of this is O(keys)
    for a in schemas.PostCreate.model_fields.keys(): 
        if post.get(a) is not None:
            bucket_dict[a] = post[a]
            
    post_query.update(bucket_dict,synchronize_session=False)
    
    db.commit()
    
    
    return  post_query.first()   