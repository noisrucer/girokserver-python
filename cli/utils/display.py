from datetime import datetime

from rich import print
from rich.console import Console
from rich.padding import Padding
from rich.tree import Tree
from rich.align import Align
from rich.layout import Layout
import shutil

import utils.task as task_utils

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
    # """
    # Print text with center alignment.
    # Args:
    #     text (Union[str, Rule, Table]): object to center align
    #     style (str, optional): styling of the object. Defaults to None.
    # """
    if wrap:
        width = shutil.get_terminal_size().columns // 2
    else:
        width = shutil.get_terminal_size().columns

    console.print(Align.center(text, style=style, width=width), height=100)
    
    
def display_tasks_by_category(task_tree):
    tree = Tree("")
    for idx, cat_name in enumerate(task_tree):
        tree.add(display_category_with_tasks(
            cat_name=cat_name,
            task_tree=task_tree[cat_name],
            icon=f":keycap_{idx+1}:"
            ))
    return tree


def display_category_with_tasks(cat_name, task_tree: dict, icon=None):
    tree = Tree(f"{icon+'  ' if icon else ''}[yellow]{cat_name}[/yellow]")
    for sub_cat_name in task_tree['sub_categories']:
        sub_tree = display_category_with_tasks(
            cat_name=sub_cat_name,
            task_tree=task_tree['sub_categories'][sub_cat_name],
            icon=None
        )
        tree.add(sub_tree)
    for task in task_tree['tasks']:
        deadline = datetime.strptime(task['deadline'], "%Y-%m-%dT%H:%M:%S")
        year, month, day = deadline.year, deadline.month, deadline.day
        h, m, s = str(deadline.time()).split(":")
        month_name = task_utils.get_month_name_from_month(month)
        weekday_name = task_utils.get_weekday_name_from_date(year, month, day)
        h = int(h)
        is_time = task['is_time']
        afternoon = h >= 12
        if h > 12:
            h -= 12
        time = f" / {h}:{m} {'PM' if afternoon else 'AM'}" if is_time else ''
        remaining_days = task_utils.get_day_offset_between_two_dates(datetime.now(), deadline)
        day_offset_message = f"{remaining_days} days left" if remaining_days > 0 else f"{abs(remaining_days)} days passed"
        if remaining_days == 0:
            day_offset_message = "Due Today"
        tree.add(f"[green][{weekday_name}, {day} {month_name}{time}][/green] [red]{task['name']}[/red] [{day_offset_message}]")

    return tree        
            
    

    
    

    
