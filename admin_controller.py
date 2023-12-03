from fastapi import APIRouter, HTTPException, Depends
import service as Service
import os
from models import MasterCommandRequest
from fastapi.responses import FileResponse


def validate_secret_key(auth_token):
    try:
        if auth_token!=os.environ["SECRET_KEY"]:
            raise HTTPException(status_code=403, detail="Unauthenticated")
    except:
        raise HTTPException(status_code=403, detail="Unauthenticated")

admin = APIRouter(
    prefix="/master",
    dependencies=[Depends(validate_secret_key)],
)

@admin.get("/slaves")
async def listallslaves():
    return Service.list_all_slaves()

@admin.post("/slave/command")
async def master_command(master_command: MasterCommandRequest):
    return Service.set_command_to_slave_from_master(master_command)

@admin.get("/slave/response")
async def master_response(mac: str):
    return Service.get_response_from_slave_to_master(mac)


@admin.get("/slave/response/file/download")
async def master_response_file_download(mac: str):
    file_details = Service.get_response_from_slave_to_master(mac)

    file_path = Service.get_file_download_path(mac,file_details['file'])
    
    if file_path is None:
        raise HTTPException(status_code=404, detail="File not found!")
    
    return FileResponse(path=file_path, filename = file_details['file'])

@admin.get("/slave/response/screenshot")
async def master_screenshot_response(mac: str):
    file_path = Service.get_screenshot_from_slave(mac)

    if file_path is None:
        raise HTTPException(status_code=404, detail="Screenshot not found!")
    
    return FileResponse(file_path)

@admin.get("/slave/response/screenshot/exists")
async def master_screenshot_exists(mac: str):
    return Service.check_screenshot_exists(mac)

@admin.get("/slave/response/screenshot/delete")
async def master_screenshot_delete(mac: str):
    return Service.delete_screenshot(mac)

@admin.get("/slave/clear/response")
async def clear_slave_response(mac: str):
    return Service.clear_slave_response(mac)
    
@admin.get("/redis/reset")
async def clearredis():
    return Service.clear_redis()