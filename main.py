from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from admin_controller import admin
from slave_controller import slave
import os

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

@app.get("/")
async def root():
    return "HELLO WORLD"
    
app.include_router(admin, prefix="/api")
app.include_router(slave, prefix="/api")
