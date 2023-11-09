import redis

client = redis.Redis.from_url('redis://red-cl5r0od6fh7c73etkn90:6379')

def set_key_val_with_ttl(key,value,ttl_in_seconds):
  client.set(key,value, ex=ttl_in_seconds)

def set_key_val(key,value):
  client.set(key,value)

def get_value_from_key(key):
  client.get(key)

def find_all_keys_with_pattern(prefix):
  pattern = f"{prefix}*"
  return client.keys(pattern=pattern)
  
