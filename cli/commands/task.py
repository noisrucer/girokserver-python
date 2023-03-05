import typer
from rich import print
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.padding import Padding
from rich.panel import Panel

from config import get_config
import api.task as task_api
import utils.general as general_utils
import utils.display as display_utils
import webbrowser

app = typer.Typer(rich_markup_mode='rich')
console = Console()
cfg = get_config()

@app.command("showcats")
def show_categories():
    cats_dict = task_api.get_categories()
    text = Align.center("[bold red]Task Categories[/bold red]")
    display_utils.center_print(text, "cyan on purple3")
    # console.print(Panel(text, title="Welcome", padding=1))
    display_utils.display_categories(cats_dict)
    

@app.command("addcat")
def add_category(
    cat: str = typer.Argument(..., help="Category name - xx/yy/zz.."),
    color: str = typer.Option("yellow", "-c", "--color", help="Color for category")
):
    task_api.add_category(cat, color)
    
    
    