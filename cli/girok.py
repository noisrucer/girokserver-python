from pathlib import Path
import os
import os.path as osp

import typer
from rich import print
from rich.console import Console
from rich.table import Table

import api.auth as auth_api
import commands.auth as auth_command
import utils.general as general_utils
import utils.auth as auth_utils

app = typer.Typer(rich_markup_mode='rich')
app.registered_commands.extend(auth_command.app.registered_commands)

APP_NAME = "girok"
APP_DIR = typer.get_app_dir(APP_NAME)
CONFIG_PATH: Path = Path(APP_DIR) / "config.json"
    
@app.command()
def test():
    print("test")


@app.callback()
def pre_command_callback(ctx: typer.Context):
    # Setting up app dir and config file if they don't exist
    general_utils.config_setup(APP_DIR, CONFIG_PATH)
    if ctx.invoked_subcommand in ['login', 'logout', 'register']:
        return
        
    # Check if JWT is stored in config file
    stored_access_token = auth_utils.get_access_token_from_json(CONFIG_PATH)
    if stored_access_token:
        resp = auth_api.validate_access_token(stored_access_token)
        if resp.status_code != 200: # invalid(or expired) JWT -> login again
            print("You're not logged in. Please login with [green]girok login[/green].")
            exit(0)
    else:
        print("You're not logged in. Please login with [green]girok login[/green].")
        exit(0)
        
app()