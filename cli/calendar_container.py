from datetime import datetime, timedelta
import calendar

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static, Label, Placeholder, Tree
from textual.messages import Message
from textual.widget import Widget
from rich.text import Text
from textual import log

import api.task as task_api
import api.category as category_api
import utils.calendar as calendar_utils
import utils.general as general_utils
import utils.display as display_utils
import utils.task as task_utils
import constants as constants


class CalendarHeader(Static):
    year = datetime.now().year
    month = datetime.now().month
    
    def on_mount(self):
        self.display_date()
        
    def update_year_and_month(self, year, month):
        self.year, self.month = year, month
        self.display_date()
    
    def display_date(self):
        month_name = task_utils.get_month_name_by_number(self.month)
        self.update(f"{month_name} {self.year}")


class Calendar(Static):
    year = datetime.now().year
    month = datetime.now().month
    cat_path = "" # If "", show all categories
    can_focus = True
    
    def on_mount(self):
        self.update_calendar()
        
    def update_year_and_month(self, year, month):
        self.year, self.month = year, month
        self.update_calendar()
        
    def update_cat_path(self, new_cat_path: str):
        self.cat_path = new_cat_path
        self.update_calendar()
        
    def update_calendar(self):
        """
        If val == "", then "root category" is selected
        """
        if self.cat_path == "": # all categories
            cat_list = None
        elif self.cat_path == "No Category":
            pass
        else:
            cat_list = self.cat_path[:-1].split('/')
            
        start_date, end_date = task_utils.build_time_window_by_year_and_month(self.year, self.month)
        resp = task_api.get_tasks(
            cats=cat_list,
            start_date=start_date,
            end_date=end_date,
            min_pri=None,
            max_pri=None,
            tag=None,
            view="list"
        )
        
        if resp.status_code == 200:
            tasks = general_utils.bytes2dict(resp.content)['tasks']
            # task_tree = display_utils.display_tasks_by_category(tasks)
        elif resp.status_code == 400:
            err_msg = general_utils.bytes2dict(resp.content)['detail']
            exit(err_msg)
            # self.exit(err_msg)
        else:
            # self.exit(resp)
            exit(resp)
        self.update(str(tasks))
        # self.update(f"{self.year} {self.month} {self.cat_path} {tasks}")
        
        
class CalendarContainer(Vertical):
    year = datetime.now().year
    month = datetime.now().month
    cat_path = None # If none, show all categories
    
    def update_month_by_offset(self, offset: int):
        new_year, new_month = task_utils.get_year_and_month_by_month_offset(
            month_offset=offset,
            year=self.year,
            month=self.month
        )
        self.year, self.month = new_year, new_month
        calendar_header = self.query_one(CalendarHeader)
        cal = self.query_one(Calendar)
        
        calendar_header.update_year_and_month(self.year, self.month)
        cal.update_year_and_month(self.year, self.month)
        
    def update_year_and_month(self, year: int, month: int):
        self.year, self.month = year, month
        calendar_header = self.query_one(CalendarHeader)
        cal = self.query_one(Calendar)
        
        calendar_header.update_year_and_month(self.year, self.month)
        cal.update_year_and_month(self.year, self.month)
        
    def update_cat_path(self, cat_path: str):
        """
        cat_path: ex) HKU/COMP3230 or ""
        """
        self.cat_path = cat_path
        cal = self.query_one(Calendar)
        cal.update_cat_path(new_cat_path=cat_path)
        
    def compose(self):
        yield CalendarHeader(id="calendar-header")
        yield Calendar()
        # with Horizontal(id="calendar-main-container"):
        #     with Vertical(classes="vertical"):
        #         yield Static("Monday", classes="weekday-name")
        #         yield Static(f"1", classes="calendar-cell")
        #         yield Static(f"8", classes="calendar-cell")
        #         yield Static(f"15", classes="calendar-cell")
        #         yield Static(f"22", classes="calendar-cell")
        #         yield Static(f"29", classes="calendar-cell")
        #     with Vertical(classes="vertical"):
        #         yield Static("Tuesday", classes="weekday-name")
        #         yield Static(f"2", classes="calendar-cell")
        #         yield Static(f"9", classes="calendar-cell")
        #         yield Static(f"16", classes="calendar-cell")
        #         yield Static(f"23", classes="calendar-cell")
        #         yield Static(f"30", classes="calendar-cell")
        #     with Vertical(classes="vertical"):
        #         yield Static("Wednesday", classes="weekday-name")
        #         yield Static(f"3", classes="calendar-cell")
        #         yield Static(f"10", classes="calendar-cell")
        #         yield Static(f"17", classes="calendar-cell")
        #         yield Static(f"24", classes="calendar-cell")
        #         yield Static(f"31", classes="calendar-cell")
        #     with Vertical(classes="vertical"):
        #         yield Static("Thursday", classes="weekday-name")
        #         yield Static(f"4", classes="calendar-cell")
        #         yield Static(f"11", classes="calendar-cell")
        #         yield Static(f"18", classes="calendar-cell")
        #         yield Static(f"25", classes="calendar-cell")
        #         yield Static(f"1", classes="calendar-cell")
        #     with Vertical(classes="vertical"):
        #         yield Static("Friday", classes="weekday-name")
        #         yield Static(f"5", classes="calendar-cell")
        #         yield Static(f"12", classes="calendar-cell")
        #         yield Static(f"19", classes="calendar-cell")
        #         yield Static(f"26", classes="calendar-cell")
        #         yield Static(f"2", classes="calendar-cell")
        #     with Vertical(classes="vertical"):
        #         yield Static("Saturday", classes="weekday-name")
        #         yield Static(f"6", classes="calendar-cell")
        #         yield Static(f"13", classes="calendar-cell")
        #         yield Static(f"20", classes="calendar-cell")
        #         yield Static(f"27", classes="calendar-cell")
        #         yield Static(f"3", classes="calendar-cell")
        #     with Vertical(classes="vertical"):
        #         yield Static("Sunday", classes="weekday-name")
        #         with Static(classes="calendar-cell"):
        #             yield Static(f"7", classes="test")
        #         with Static(classes="calendar-cell"):
        #             yield Static(f"14")
        #         with Static(classes="calendar-cell"):
        #             yield Static(f"21")
        #         with Static(classes="calendar-cell"):
        #             yield Static(f"28")
        #         with Static(classes="calendar-cell"):
        #             yield Static(f"4")        