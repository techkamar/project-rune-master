from pydantic import BaseModel

# When Slave asks the Master for any command to run
class SlaveCommandRequest(BaseModel):
    username: str
    mac: str
    hostname: str
    os: str

# When Slave gives response to the command
class SlaveTextOutputRequest(BaseModel):
    mac: str
    content: str

# When Slave gets command as response
class SlaveCommandResponse(BaseModel):
    type: str
    command: str

# When Master gives command for a slave
class MasterCommandRequest(BaseModel):
    mac: str
    type: str
    command: str

# When Master gets list of all slaves
class SlaveDetailResponse(BaseModel):
    username: str
    mac: str
    ip: str
    hostname: str
    os: str
