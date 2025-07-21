from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello World"}    
#Path parameters

#Special occasion   item_id == user_id
@app.get("/items/me")                # This has to come before from {item_id} /me has a priority
async def read_user_me():
    return {"Item id":"Current User"}


@app.get("/items/{item_id}")
async def read_item(item_id: int): #You can pass the type of parameter. May create parsing problems
    return {"Item id ":  item_id}   
   