from rich import print
from rich.console import Console
from rich.padding import Padding
from rich.tree import Tree
from rich.align import Align
import shutil

console = Console()

def display_categories(cats_dict: dict, highlight_cat=None):
    tree = Tree("")
    for idx, cat in enumerate(cats_dict):
        display_category(
            cats_dict,
            cat,
            top_most=True,
            tree=tree,
            icon=f":keycap_{idx+1}:",
            cumul_path=cat,
            highlight_cat=highlight_cat
        )
    console.print(tree)
    
    
def display_category(
    cats_dict: dict,
    cat: str,
    top_most=True,
    tree: Tree=None,
    icon=None,
    cumul_path="",
    highlight_cat=None
):
    cat_txt = f"[green]{cat}[/green]" if highlight_cat == cumul_path else cat
    tree = tree.add(f"{icon + '  ' + '[yellow]' if top_most else ''}{cat_txt}")
    for sub in cats_dict[cat].keys():
        display_category(
            cats_dict[cat],
            sub,
            top_most=False,
            tree=tree,
            cumul_path=cumul_path + "/" + sub,
            highlight_cat=highlight_cat
        )
        
    
def center_print(text, style: str = None, wrap: bool = False) -> None:
    """Print text with center alignment.
    Args:
        text (Union[str, Rule, Table]): object to center align
        style (str, optional): styling of the object. Defaults to None.
    """
    if wrap:
        width = shutil.get_terminal_size().columns // 2
    else:
        width = shutil.get_terminal_size().columns

    console.print(Align.center(text, style=style, width=width), height=100)