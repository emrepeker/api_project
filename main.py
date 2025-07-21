from enum import Enum

from fastapi import FastAPI


class LogName(str, Enum):
    login = "login"
    logout = "logout"
    sign_in = "sign_in"


app = FastAPI()

@app.get("/log/{log_name}")
async def log_ops(log_name : LogName): 
    if log_name == "login":
        return {"log_name" : log_name, "message": "You at login page"}
    if log_name == "logout":
        return {"log_name" : log_name, "message":"You at logout page"}
    return {"log_name": log_name,"message":"you at sign-in page bye bye "}
