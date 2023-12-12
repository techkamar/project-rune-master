from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from admin_controller import admin
from slave_controller import slave
import os

os.system("python slave/main.py &")

app = FastAPI()

origins = [
    os.environ["UI_SERVER"]
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MasterPasswordRequest(BaseModel):
    password: str


@app.get("/")
async def root():
    return os.environ["UI_SERVER"]

@app.post("/api/validate/master/password")
async def validate_master_password(password_request:MasterPasswordRequest):
    if password_request.password == os.environ["SECRET_KEY"]:
        return {"success":True}
    return {"success":False}
    
app.include_router(admin, prefix="/api")
app.include_router(slave, prefix="/api")
