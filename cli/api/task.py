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
        cfg.base_url + "/calendar/categories",
        headers=auth_utils.build_jwt_header(cfg.config_path)
    )
    
    if resp.status_code == 200:
        return general_utils.bytes2dict(resp.content)
    

def add_category(cat_str: str, color='yellow'):
    cats = cat_str.split('/')
    resp = requests.post(
        cfg.base_url + "/calendar/categories",
        json={
            "names": cats,
            "color": color
        }
    )
    if resp.status_code == 201:
        display_utils.center_print("Task added successfully!", "black on green")
    elif resp.status_code == 400:
        err_msg = general_utils.bytes2dict(resp.content)['detail']
        display_utils.center_print(err_msg, "black on bright_red")