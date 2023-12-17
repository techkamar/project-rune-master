import redis
import os
client = redis.Redis.from_url(os.environ["REDIS_SERVER"])

def set_key_val_with_ttl(key,value,ttl_in_seconds):
  client.set(key,value, ex=ttl_in_seconds)

def set_key_val(key,value):
  client.set(key,value)

def get_value_from_key(key):
  return client.get(key)

def find_all_keys_with_pattern(prefix):
  pattern = f"{prefix}*"
  return client.keys(pattern=pattern)

def delete_key(key):
  client.delete(key)

def reset_all():
  for key in client.keys(pattern="*"):
    client.delete(key)
  
def get_all_keys():
  return list(client.keys(pattern="*"))
