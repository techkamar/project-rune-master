from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
    
@app.get("/api/slave/command")
async def command():
    return {"message": "Slave Command"}
    
@app.get("/api/slave/response/text")
async def textresponse():
    return {"message": "Slave Text Response"}
    
@app.get("/api/slave/response/file")
async def fileresponse():
    return {"message": "Slave File Response"}