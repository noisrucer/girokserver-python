from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static, Label, Placeholder, Tree
from textual.messages import Message
from textual.widget import Widget

import api.category as category_api
import utils.calendar as calendar_utils
from rich.table import Table
from textual import log

from sidebar import SidebarContainer
from calendar_container import CalendarContainer
        
class CalendarApp(Horizontal):
    CSS_PATH = "./demo_dock.css"
    
    def compose(self):
        yield SidebarContainer(id="sidebar-container")
        yield CalendarContainer(id="calendar-container")
                
    def on_category_tree_category_changed(self, event):
        self.query_one(CalendarContainer).update_cat_path(event.cat_path)