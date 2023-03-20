from datetime import datetime
import calendar

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static, Label, Placeholder, Tree
from textual.widget import Widget
from textual.messages import Message
from textual import log
from textual.reactive import var, reactive
from rich.text import Text
from rich.table import Table
from rich.style import Style
from rich import box
from rich.table import Column

import api.category as category_api
import utils.calendar as calendar_utils
import utils.display as display_utils

from calendar_app import CalendarApp
from calendar_container import CalendarContainer, Calendar
from sidebar import CategoryTree, SidebarContainer, TagTree
import constants


class Entry(App):
    CSS_PATH = "./demo_dock.css"
    current_focused = "CategoryTree"
    is_pop_up = False
    BINDINGS = [
        ("q", "quit", "Quit Nuro"),
        ("u", "show_previous_month", "Show prev month"),
        ("i", "show_next_month", "Show next month"),
        ("y", "show_current_month", "Show current month"),
        ("ctrl+l", "focus_on_calendar", "Move to calendar"),
        ("ctrl+g", "focus_on_sidebar", "Move to sidebar"),
        ("ctrl+j", "move_down_to_tag_tree", "Move down to tag tree"),
        ("ctrl+k", "move_up_to_category_tree", "Move up to category tree"),
        ("o", 'close_pop_up', "Close pop up box")
        # ("f", "toggle_files", "Toggle Files")
    ]
    # show_sidebar = reactive(True)
    
    def on_mount(self):
        self.set_focus(self.query_one(CategoryTree))
        
    def compose(self):
        yield CalendarApp()
        # yield Footer()
        
    # Display pop-up box when selecting a cell
    def on_calendar_task_cell_selected(self, event: Calendar.TaskCellSelected):
        cell_tasks = event.cell_tasks
        year, month, day = event.year, event.month, event.day
        table = display_utils.build_task_table(cell_tasks)
        
        self.query_one(CalendarContainer).mount(
            Vertical(
                Static(Text(f"{day} {calendar.month_name[month]} {year}", style=Style(bold=True, color=constants.TABLE_HEADER_DATE_COLOR)), classes="task-pop-up-header"),
                Container(Static(table, classes="task-pop-up-table"), classes="task-pop-up-table-container"),
                classes='task-pop-up-container',
            )
        )
        self.is_pop_up = True
        
    def action_quit(self):
        self.exit()
       
    def action_show_next_month(self):
        if self.is_pop_up:
            return
        calendar_container = self.query_one(CalendarContainer)
        calendar_container.update_month_by_offset(1)
         
    def action_show_previous_month(self):
        if self.is_pop_up:
            return
        calendar_container = self.query_one(CalendarContainer)
        calendar_container.update_month_by_offset(-1)
        
    def action_show_current_month(self):
        if self.is_pop_up:
            return
        calendar_container = self.query_one(CalendarContainer)
        now = datetime.now()
        cur_year, cur_month = now.year, now.month
        calendar_container.update_year_and_month(cur_year, cur_month)
        
    def action_focus_on_calendar(self):
        if self.is_pop_up:
            return
        cal = self.query_one(Calendar)
        self.set_focus(self.query_one(Calendar))
        self.current_focused = "Calendar"
        
    def action_focus_on_sidebar(self):
        if self.is_pop_up:
            return
        self.set_focus(self.query_one(CategoryTree))
        self.current_focused = "CategoryTree"
        
        cal = self.query_one(Calendar)
        if self.is_pop_up:
            return
        calendar_utils.remove_left_arrow(cal.cur_focused_cell)
        
    def action_move_down_to_tag_tree(self):
        if self.is_pop_up:
            return
        if self.current_focused != "CategoryTree":
            return
        tag_tree = self.query_one(TagTree)
        self.set_focus(tag_tree)
        self.current_focused = "TagTree"
        category_tree = self.query_one(CategoryTree)
        calendar_utils.remove_highlight(category_tree.highlighted_node)
        calendar_utils.remove_left_arrow_tree(category_tree.highlighted_node)
        calendar_utils.add_left_arrow_tree(tag_tree.highlighted_node)
        calendar_utils.add_highlight(tag_tree.highlighted_node)
    
    def action_move_up_to_category_tree(self):
        if self.is_pop_up:
            return
        if self.current_focused != "TagTree":
            return
        category_tree = self.query_one(CategoryTree)
        self.set_focus(category_tree)
        self.current_focused = "CategoryTree"
        tag_tree = self.query_one(TagTree)
        calendar_utils.remove_highlight(tag_tree.highlighted_node)
        calendar_utils.remove_left_arrow_tree(tag_tree.highlighted_node)
        calendar_utils.add_left_arrow_tree(category_tree.highlighted_node)
        calendar_utils.add_highlight(category_tree.highlighted_node)
        
    def action_close_pop_up(self):
        if not self.is_pop_up:
            return
        self.query_one(".task-pop-up-container").remove()
        self.query_one(Calendar).is_pop_up = False
        self.is_pop_up = False
        
        
    
    # def watch_show_sidebar(self, show_sidebar: bool):
    #     sidebar_container = self.query_one(SidebarContainer)
    #     if show_sidebar:
    #         sidebar_container.styles.display = "block"
    #     else:
    #         sidebar_container.styles.display = "none"
        
    # def action_toggle_files(self):
    #     self.show_sidebar = not self.show_sidebar
    #     sidebar_container = self.query_one(SidebarContainer)
    #     if self.show_sidebar:
    #         sidebar_container.styles.display = "block"
    #     else:
    #         sidebar_container.styles.display = "none"
        
    # self.set_class(show_sidebar, "show-sidebar")
        
                
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