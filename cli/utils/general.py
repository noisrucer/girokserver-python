import json
import os

def config_setup(APP_DIR, CONFIG_PATH):
    if not CONFIG_PATH.is_file():
        if not os.path.isdir(APP_DIR):
            os.makedirs(APP_DIR)
        write_json(CONFIG_PATH, {})


def read_json(fpath):
    with open(fpath, 'r') as f:
        data = json.load(f)
        return data
    
    
def write_json(fpath, data):
    with open(fpath, 'w') as f:
        json.dump(data, f)
        

def update_json(fpath, data):
    with open(fpath, 'r') as f:
        org_data = json.load(f)
        org_data.update(**data)
    write_json(fpath, org_data)
    
    
def bytes2dict(b):
    return json.loads(b.decode('utf-8'))


def dict2json(d):
    return json.dumps(d)