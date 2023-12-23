from pydantic import BaseModel, RootModel
from typing import List

# When Slave asks the Master for any command to run
class SlaveCommandRequest(BaseModel):
    username: str
    mac: str
    hostname: str
    os: str
    ostype : str

# When Slave gives response to the command
class SlaveTextOutputRequest(BaseModel):
    mac: str
    content: str

# When Slave gives response to the command
class SlaveFileBrowseOutputRequest(BaseModel):
    directories: list
    files: list
    working_dir: str
    mac: str

# When Master gives command for a slave
class MasterCommandRequest(BaseModel):
    mac: str
    type: str
    command: str

# Individual Service Detail
class Service(BaseModel):
    ServiceName: str
    ServiceType: str
    StartType: str
    Status : str

class MasterCommandRequestList(RootModel):
    root : List[MasterCommandRequest]


class ServiceList(RootModel):
    root : List[Service]

# When Master gives command for a slave
class RedisCommandRequest(BaseModel):
    key: str