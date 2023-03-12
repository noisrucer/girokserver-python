from datetime import datetime, timedelta
import calendar

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static, Label, Placeholder, Tree
from textual.messages import Message
from textual.widget import Widget

import api.category as category_api
import utils.calendar as calendar_utils
import utils.task as task_utils
from rich.table import Table
from textual import log


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
    cat_path = None # If none, show all categories
    
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
        self.update(f"{self.year} {self.month} {self.cat_path}")
        
        
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
        