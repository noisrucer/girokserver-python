import json
from rich import print

import utils.general as general_utils

def match_passwords(pwd, confirm_pwd):
    if pwd != confirm_pwd:
        print("Confirm password does not match.")
        exit(0)
        

def remove_access_token(config_path):
    with open(config_path, 'r') as f:
        org_data = json.load(f)
        del org_data['access_token']
        
    general_utils.write_json(config_path, org_data)
        
        
def get_access_token_from_json(fpath):
    with open(fpath, 'r') as f:
        data = json.load(f)
        if "access_token" in data:
            return data['access_token']
        else:
            return None
        

def is_logged_in(config_path):
    return get_access_token_from_json(config_path)
        

def store_access_token_to_json(fpath, access_token):
    data = {"access_token": access_token}
    general_utils.update_json(fpath, data)
    