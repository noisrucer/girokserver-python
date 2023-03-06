import requests
from rich.console import Console

from config import get_config
import utils.auth as auth_utils
import utils.general as general_utils
import utils.display as display_utils

console = Console()
cfg = get_config()

def get_categories():
    resp = requests.get(
        cfg.base_url + "/categories",
        headers=auth_utils.build_jwt_header(cfg.config_path)
    )
    
    if resp.status_code == 200:
        return general_utils.bytes2dict(resp.content)
    

def add_category(cat_str: str, color='yellow'):
    cats = cat_str.split('/')
    resp = requests.post(
        cfg.base_url + "/categories",
        json={
            "names": cats,
            "color": color
        },
        headers=auth_utils.build_jwt_header(cfg.config_path)
    )
    return resp
        
        
def remove_category(cat_str: str):
    cats = cat_str.split('/')
    resp = requests.delete(
        cfg.base_url + "/categories",
        json={
            "cats": cats
        },
        headers=auth_utils.build_jwt_header(cfg.config_path)
    )
    
    return resp


def rename_category(cat_str: str, new_name: str):
    cats = cat_str.split('/')
    resp = requests.patch(
        cfg.base_url + "/categories/name",
        json={
            "cats": cats,
            "new_name": new_name
        },
        headers=auth_utils.build_jwt_header(cfg.config_path)
    )
    
    return resp


def move_category(cat_str: str, new_parent_cat_str: str):
    if cat_str.endswith('/'):
        cat_str = cat_str[:-1]
    if new_parent_cat_str.endswith('/'):
        new_parent_cat_str = new_parent_cat_str[:-1]
        
    cats = cat_str.split('/') if cat_str else []
    new_parent_cats = new_parent_cat_str.split('/') if new_parent_cat_str else []
    resp = requests.patch(
        cfg.base_url + "/categories/parent",
        json={
            "cats": cats,
            "new_parent_cats": new_parent_cats
        },
        headers=auth_utils.build_jwt_header(cfg.config_path)
    )
    return resp