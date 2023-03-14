from datetime import datetime

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static, Label, Placeholder, Tree
from textual.widget import Widget
from textual.messages import Message
from textual import log

import api.category as category_api
import utils.calendar as calendar_utils
from rich.table import Table

from calendar_app import CalendarApp
from calendar_container import CalendarContainer, Calendar
from sidebar import CategoryTree

class Hello(Widget):
    can_focus: True
    can_focus_children = True
    def compose(self):
        yield Static("hello")

class Entry(App):
    CSS_PATH = "./demo_dock.css"
    BINDINGS = [
        ("q", "quit", "Quit Nuro"),
        ("u", "show_previous_month", "Show prev month"),
        ("i", "show_next_month", "Show next month"),
        ("y", "show_current_month", "Show current month"),
        ("ctrl+l", "focus_on_calendar", "Move to calendar"),
        ("ctrl+g", "focus_on_sidebar", "Move to sidebar")
    ]
    def on_mount(self):
        self.set_focus(self.query_one(CategoryTree))
        
    def compose(self):
        yield CalendarApp()
        yield Footer()
        
    def action_quit(self):
        self.exit()
       
    def action_show_next_month(self):
        calendar_container = self.query_one(CalendarContainer)
        calendar_container.update_month_by_offset(1)
         
    def action_show_previous_month(self):
        calendar_container = self.query_one(CalendarContainer)
        calendar_container.update_month_by_offset(-1)
        
    def action_show_current_month(self):
        calendar_container = self.query_one(CalendarContainer)
        now = datetime.now()
        cur_year, cur_month = now.year, now.month
        calendar_container.update_year_and_month(cur_year, cur_month)
        
    def action_focus_on_calendar(self):
        self.set_focus(self.query_one(Calendar))
        log("CTRL L", self.focused)
        
    def action_focus_on_sidebar(self):
        self.set_focus(self.query_one(CategoryTree))
        log("CTRL H", self.focused)
        
        
        
                
    # def on_category_tree_category_changed(self, event):
    #     log("AAAA")
    #     wow = self.query_one(SimpleText)
    #     wow.show()
                # yield FizzBuzz()
                # with Horizontal(id="calendar-main-container"):
                #         with Vertical(classes="vertical"):
                #             yield Static("Monday", classes="weekday-name")
                #             yield Static(f"1", classes="calendar-cell")
                #             yield Static(f"8", classes="calendar-cell")
                #             yield Static(f"15", classes="calendar-cell")
                #             yield Static(f"22", classes="calendar-cell")
                #             yield Static(f"29", classes="calendar-cell")
                #         with Vertical(classes="vertical"):
                #             yield Static("Tuesday", classes="weekday-name")
                #             yield Static(f"2", classes="calendar-cell")
                #             yield Static(f"9", classes="calendar-cell")
                #             yield Static(f"16", classes="calendar-cell")
                #             yield Static(f"23", classes="calendar-cell")
                #             yield Static(f"30", classes="calendar-cell")
                #         with Vertical(classes="vertical"):
                #             yield Static("Wednesday", classes="weekday-name")
                #             yield Static(f"3", classes="calendar-cell")
                #             yield Static(f"10", classes="calendar-cell")
                #             yield Static(f"17", classes="calendar-cell")
                #             yield Static(f"24", classes="calendar-cell")
                #             yield Static(f"31", classes="calendar-cell")
                #         with Vertical(classes="vertical"):
                #             yield Static("Thursday", classes="weekday-name")
                #             yield Static(f"4", classes="calendar-cell")
                #             yield Static(f"11", classes="calendar-cell")
                #             yield Static(f"18", classes="calendar-cell")
                #             yield Static(f"25", classes="calendar-cell")
                #             yield Static(f"1", classes="calendar-cell")
                #         with Vertical(classes="vertical"):
                #             yield Static("Friday", classes="weekday-name")
                #             yield Static(f"5", classes="calendar-cell")
                #             yield Static(f"12", classes="calendar-cell")
                #             yield Static(f"19", classes="calendar-cell")
                #             yield Static(f"26", classes="calendar-cell")
                #             yield Static(f"2", classes="calendar-cell")
                #         with Vertical(classes="vertical"):
                #             yield Static("Saturday", classes="weekday-name")
                #             yield Static(f"6", classes="calendar-cell")
                #             yield Static(f"13", classes="calendar-cell")
                #             yield Static(f"20", classes="calendar-cell")
                #             yield Static(f"27", classes="calendar-cell")
                #             yield Static(f"3", classes="calendar-cell")
                #         with Vertical(classes="vertical"):
                #             yield Static("Sunday", classes="weekday-name")
                #             with Static(classes="calendar-cell"):
                #                 yield Static(f"7", classes="test")
                #             with Static(classes="calendar-cell"):
                #                 yield Static(f"14")
                #             with Static(classes="calendar-cell"):
                #                 yield Static(f"21")
                #             with Static(classes="calendar-cell"):
                #                 yield Static(f"28")
                #             with Static(classes="calendar-cell"):
                #                 yield Static(f"4")
                #         # with Container(id=f"calendar-cell-{i}", classes="calendar-cell"):
                        #     yield Static(f"cell {i}")
        # yield Footer()
            
if __name__ == '__main__':
    Entry().run()