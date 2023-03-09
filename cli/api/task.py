import requests
from config import get_config
import utils.auth as auth_utils
cfg = get_config()

def create_task(task_data: dict):
    resp = requests.post(
        cfg.base_url + "/tasks",
        json=task_data,
        headers=auth_utils.build_jwt_header(cfg.config_path)
    )
    return resp
    

def get_tags():
    resp = requests.get(
        cfg.base_url + "/tasks/tags",
        headers=auth_utils.build_jwt_header(cfg.config_path)
    )
    return resp
    