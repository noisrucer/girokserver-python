import re
from datetime import datetime

import typer
from rich import print
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.padding import Padding
from rich.panel import Panel

import constants as constants
from config import get_config
import api.task as task_api
import api.category as category_api
import utils.general as general_utils
import utils.display as display_utils
import utils.task as task_utils
import utils.auth as auth_utils

app = typer.Typer(rich_markup_mode='rich')
console = Console()
cfg = get_config()

# Code Credits: https://github.com/tiangolo/typer/issues/140#issuecomment-898937671
def DeadlineMutuallyExclusiveGroup(size=2):
    group = set()
    def callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
        # Add cli option to group if it was called with a value
        if value is not None and param.name not in group:
            group.add(param.name)
        if len(group) > size - 1:
            raise typer.BadParameter(f"{param.name} is mutually exclusive with {group.pop()}")
        return value
    return callback


def TimeMutuallyExclusiveGroup(size=2):
    time_group = set()
    def callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
        # Add cli option to group if it was called with a value
        if value is not None and param.name not in time_group:
            time_group.add(param.name)
        if len(time_group) > size - 1:
            print(time_group)
            raise typer.BadParameter(f"{param.name} is mutually exclusive with {time_group.pop()}")
        return value
    return callback

deadline_exclusivity_callback = DeadlineMutuallyExclusiveGroup()
time_exclusivity_callback = TimeMutuallyExclusiveGroup()

###################################################################################


def priority_callback(value: int):
    if value is None:
        return None
    
    if value < 1 or value > 5:
        raise typer.BadParameter("[Invalid priority] priority must be in [1, 5].")
    
    return value


def category_callback(value: str):
    if value is None:
        return None

    if not re.match("^([a-zA-Z0-9]+/)*[a-zA-Z0-9]+/?$", value):
        raise typer.BadParameter("[Invalid category path] Category path must be in 'xx/yy/zz format.'")

    if value.endswith('/'):
        value =value[:-1]
    return value


def deadline_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    deadline_exclusivity_callback(ctx, param, value)
    
    if value is None:
        return None
    
    # "2023/02/23", "4/23"
    value = value.strip()
    args = value.split(" ")
    
    if len(args) != 1:
        raise typer.BadParameter("Deadline must be in 'yyyy/mm/dd' or 'mm/dd' format.")
    
    date = args[0]
    if not re.match("^([0-9]){4}/([0-9]){1,2}/([0-9]){1,2}|([0-9]){1,2}/([0-9]){1,2}$", date):
        raise typer.BadParameter("Deadline must be in 'yyyy/mm/dd' or 'mm/dd' format.")
    
    year, month, day = datetime.now().year, None, None
    date_list = list(map(int, date.split('/')))
    if len(date_list) == 3:
        year, month, day = date_list
    elif len(date_list) == 2:
        month, day = date_list
    
    if not task_utils.is_valid_year(year):
        raise typer.BadParameter(f"Invalid year: {year}. Year must be in [current_year - 3, current_year + 10]")
    if not task_utils.is_valid_month(month):
        raise typer.BadParameter(f"Invalid month: {month}")
    if not task_utils.is_valid_day(year, month, day):
        raise typer.BadParameter(f"Invalid day: {day}")
    
    return year, month, day


def time_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    time_exclusivity_callback(ctx, param, value)
    if value is None:
        return None
    if not re.match("^[0-9]{2}:[0-9]{2}$", value):
        raise typer.BadParameter(f"[Invalid time: {value}. Time must be in hh:mm format.")
    
    hour, minute = value.split(':')
    if not task_utils.is_valid_hour(int(hour)):
        raise typer.BadParameter(f"Invalid hour: {hour}. Hour must be in [00-23].")
    if not task_utils.is_valid_minute(int(minute)):
        raise typer.BadParameter(f"Invalid minute: {minute}. Hour must be in [00-59].")
    
    return f"{hour}:{minute}:00"


def all_day_callback(ctx: typer.Context, param: typer.CallbackParam, value: bool):
    time_exclusivity_callback(ctx, param, value)
    if value is None:
        return False
    return value


def after_callback(ctx: typer.Context, param: typer.CallbackParam, value: int):
    deadline_exclusivity_callback(ctx, param, value)
    if value is None:
        return None

    if value <= 0:
        raise typer.BadParameter(f"Invalid offset: {value}. It must be greater than 0.")
    return value


def everyday_callback(value: bool):
    if value is None:
        return None
    if value <= 0:
        raise typer.BadParameter(f"Recurring days must be greater than 0.")
    return value
    

# Required: name, deadline
@app.command('addtask')
def add_task(
    name: str = typer.Argument(..., help="Task name"),
    cat: str = typer.Option(None, "-c", "--category", help="Category path - xx/yy/zz..", callback=category_callback),
    priority: int = typer.Option(None, "-p", "--priority", help="priority", callback=priority_callback),
    color: str = typer.Option(None, "--color", help="Color"),
    deadline: str = typer.Option(None, "-d", "--deadline", help="Deadline", callback=deadline_callback),
    everyday: bool = typer.Option(False, "-e", "--everyday", help="Set task due everyday"),
    today: bool = typer.Option(None, "--today", help="Set deadline to today", callback=deadline_exclusivity_callback),
    tomorrow: bool = typer.Option(None, "--tmr", "--tomorrow", help="Set deadline to tomorrow", callback=deadline_exclusivity_callback),
    this_mon: bool = typer.Option(None, "-t1", "--thismon", help="Set deadline to this Monday", callback=deadline_exclusivity_callback),
    this_tue: bool = typer.Option(None, "-t2", "--thistue", help="Set deadline to this Tuesday", callback=deadline_exclusivity_callback),
    this_wed: bool = typer.Option(None, "-t3", "--thiswed", help="Set deadline to, this Wednesday", callback=deadline_exclusivity_callback),
    this_thu: bool = typer.Option(None, "-t4", "--thisthu", help="Set deadline to this Thursday", callback=deadline_exclusivity_callback),
    this_fri: bool = typer.Option(None, "-t5", "--thisfri", help="Set deadline to this Friday", callback=deadline_exclusivity_callback),
    this_sat: bool = typer.Option(None, "-t6", "--thissat", help="Set deadline to this Saturday", callback=deadline_exclusivity_callback),
    this_sun: bool = typer.Option(None, "-t7", "--thissun", help="Set deadline to this Sunday", callback=deadline_exclusivity_callback),
    next_mon: bool = typer.Option(None, "-n1", "--nextmon", help="Set deadline to next Monday", callback=deadline_exclusivity_callback),
    next_tue: bool = typer.Option(None, "-n2", "--nexttue", help="Set deadline to next Tuesday", callback=deadline_exclusivity_callback),
    next_wed: bool = typer.Option(None, "-n3", "--nextwed", help="Set deadline to next Wednesday", callback=deadline_exclusivity_callback),
    next_thu: bool = typer.Option(None, "-n4", "--nextthu", help="Set deadline to next Thursday", callback=deadline_exclusivity_callback),
    next_fri: bool = typer.Option(None, "-n5", "--nextfri", help="Set deadline to next Friday", callback=deadline_exclusivity_callback),
    next_sat: bool = typer.Option(None, "-n6", "--nextsat", help="Set deadline to next Saturday", callback=deadline_exclusivity_callback),
    next_sun: bool = typer.Option(None, "-n7", "--nextsun", help="Set deadline to next Sunday", callback=deadline_exclusivity_callback),
    after: int = typer.Option(None, "-a", "--after", help="Set deadline to after x days", callback=after_callback),
    time: str = typer.Option(None, "-t", "--time", help="Deadline time, xx:yy", callback=time_callback),
    all_day: bool = typer.Option(None, "--allday", help="Set deadline time to all day", callback=all_day_callback),
    tag: str = typer.Option(None, "--tag", help="Tag"),
):  
    # Category
    cat_id = None
    if cat:
        cats = cat.split('/') if cat else []
        cat_id = category_api.get_last_cat_id(cats)
    
    # Deadline
    this_week_group = [this_mon, this_tue, this_wed, this_thu, this_fri, this_sat, this_sun]
    next_week_group = [next_mon, next_tue, next_wed, next_thu, next_fri, next_sat, next_sun]
    
    if not any(this_week_group + next_week_group + [deadline, today, tomorrow, after, everyday]):
        raise typer.BadParameter("At least one of deadline options is required.")
    
    if everyday and any(this_week_group + next_week_group + [deadline, today, tomorrow, after]):
        raise typer.BadParameter("'--everyday' option cannot be used with other deadline options.")
    
    year, month, day = None, None, None
    if deadline:
        year, month, day = deadline
        
    if today:
        year, month, day = task_utils.get_date_from_shortcut(True, datetime.now().weekday())
        
    if tomorrow:
        is_this_week = True
        weekday_num = datetime.now().weekday() + 1
        if weekday_num == 6:
            is_this_week = False
            weekday_num = 0
        year, month, day = task_utils.get_date_from_shortcut(is_this_week, weekday_num)
        
    if after:
        year, month, day = task_utils.get_date_from_offset(after)
    
    if any(this_week_group):
        this_week_day_num = [idx for idx, val in enumerate(this_week_group) if val][0]
        year, month, day = task_utils.get_date_from_shortcut(
            this_week=True,
            weekday_num=this_week_day_num
        )
        
    if any(next_week_group):
        this_week_day_num = [idx for idx, val in enumerate(next_week_group) if val][0]
        year, month, day = task_utils.get_date_from_shortcut(
            this_week=False,
            weekday_num=this_week_day_num
        )
    
    if everyday:
        year, month, day = "2000", "01", "01" # meaningless date in case of everyday
        
    full_deadline = f"{year}-{month}-{day} {time if time else '12:00:00'}"
    
    # Color - 만약 카테고리있으면 자동설정 (category 하고 Color 중복설정 불가)
    if cat:
        cat_color = category_api.get_category_color(cat_id)
        if color: # duplicate colors - prioritize default category color
            raise typer.BadParameter(f"\nInput color: {color}. However, you have set the color for {cat} as {cat_color}.")
        color = cat_color
    else:
        if not color: # default color
            color = constants.DEFAULT_TASK_COLOR
            
    task_data = {
        "task_category_id": cat_id,
        "name": name,
        "deadline": full_deadline,
        "priority": priority,
        "color": color,
        "everyday": everyday,
        "tag": tag,
        "all_day": all_day,
        "is_time": time is not None
    }
    resp = task_api.create_task(task_data)
    
    if resp.status_code == 201:
        display_utils.center_print("Task added successfully!", constants.DISPLAY_TERMINAL_COLOR_SUCCESS)
    elif resp.status_code == 400:
        err_msg = general_utils.bytes2dict(resp.content)['detail']
        display_utils.center_print(err_msg, constants.DISPLAY_TERMINAL_COLOR_ERROR)
    else:
        display_utils.center_print("Error occurred.", constants.DISPLAY_TERMINAL_COLOR_ERROR)
        
    
@app.command("showtask")
def show_task(
    cat: str = typer.Option(None, "-c", "--category", help="Category path - xx/yy/zz..", callback=category_callback),
):
    print(cat)
    
    
@app.command("showtag")
def show_tag():
    resp = task_api.get_tags()
    if resp.status_code == 200:
        tags = general_utils.bytes2dict(resp.content)['tags']
        for tag in tags:
            print(tag)
    elif resp.status_code == 400:
        err_msg = general_utils.bytes2dict(resp.content)['detail']
        display_utils.center_print(err_msg, constants.DISPLAY_TERMINAL_COLOR_ERROR)
    else:
        print(resp)