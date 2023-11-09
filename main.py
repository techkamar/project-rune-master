from typing import Annotated
from fastapi import FastAPI, Request, UploadFile
from models import SlaveCommandRequest
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
    return resp
    
@app.get("/api/slave/response/text")
async def textresponse():
    return {"message": "Slave Text Response"}
    
@app.post("/api/slave/response/file")
async def fileresponse(file: UploadFile):
    return {"name": file.filename, "size": file.size}
