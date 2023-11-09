import redisutil
import json
import os
import time
import shutil


REDIS_PREFIX_INFO = "INFO"
REDIS_PREFIX_SLAVE_COMMAND = "SLAVE_COMMAND"
REDIS_PREFIX_SLAVE_RESPONSE = "SLAVE_RESPONSE"

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
        "timestamp": int(time.time())
    }
    key = f"{REDIS_PREFIX_INFO}_{slave_command_obj.mac}"
    redisutil.set_key_val(key,json.dumps(info_json))

def fetch_slave_command(mac_address):
    key = f"{REDIS_PREFIX_SLAVE_COMMAND}_{mac_address}"
    value = redisutil.get_value_from_key(key)
    
    if value is None:
        return {}
    
    value = json.loads(value)
    return value

def del_slave_command_entry_from_redis(mac_address):
    key = f"{REDIS_PREFIX_SLAVE_COMMAND}_{mac_address}"
    redisutil.delete_key(key)


def set_slave_response(slave_text_op_req):
    key = f"{REDIS_PREFIX_SLAVE_RESPONSE}_{slave_text_op_req.mac}"
    
    resp_json = {"content": slave_text_op_req.content}

    redisutil.set_key_val(key,json.dumps(resp_json))

def save_slave_file_upload(mac_address, file):
    # Delete slave command entry
    del_slave_command_entry_from_redis(slave_text_op_req.mac)

    # Save file to directory
    output_dir = f"{os.getcwd()}/savefile/{mac_address}"
    os.makedirs(output_dir, exist_ok=True)
    
    full_file_path = f"{output_dir}/{file.filename}"
    with open(full_file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    # Add entry in slave response
    key = f"{REDIS_PREFIX_SLAVE_RESPONSE}_{slave_text_op_req.mac}"
    
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
def set_slave_command_output(slave_text_op_req):
    # Delete slave command entry
    del_slave_command_entry_from_redis(slave_text_op_req.mac)
    

    # Set Slave Response to REDIS
    set_slave_response(slave_text_op_req)
    return {"message":"done"}

# SERVICE ENTRY FUNCTION
def save_screenshot_from_slave(file):
    full_file_path = f"{os.getcwd()}/screenshot.png"
    with open(full_file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    return "OK"

######################################################################
#                           REDIS CONTROL                            #
######################################################################
def clear_redis():
    redisutil.reset_all()
    return "OK"


#######################################################################
#                           MASTER METHODs                            #
#######################################################################


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

def set_command_to_slave_from_master(master_command):
    slave_cmd_json = {
        "type": master_command.type,
        "command": master_command.command
    }

    key = f"{REDIS_PREFIX_SLAVE_COMMAND}_{master_command.mac}"
    redisutil.set_key_val(key,json.dumps(slave_cmd_json))

def get_response_from_slave_to_master(mac_address):
    key = f"{REDIS_PREFIX_SLAVE_RESPONSE}_{mac_address}"
    
    value = redisutil.get_value_from_key(key)

    if value is None:
        return {}
    
    return json.loads(value)