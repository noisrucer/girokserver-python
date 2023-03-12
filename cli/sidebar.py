from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static, Label, Placeholder, Tree
from textual.messages import Message
from textual.widget import Widget

import api.category as category_api
import utils.calendar as calendar_utils
from rich.table import Table
from textual import log


class CategoryTree(Tree):
    CSS_PATH = "./demo_dock.css"
    cats = dict()
    
    class CategoryChanged(Message):
        def __init__(self, cat_path: str):
            super().__init__()
            self.cat_path = cat_path
    
    def on_mount(self):
        self.cats = category_api.get_categories()
        self.root.expand()
        
        for cat in self.cats:
            top_cat = self.root.add(cat, expand=True)
            calendar_utils.build_category_tree(top_cat, self.cats[cat])
            
    def on_tree_node_selected(self, event: Tree.NodeSelected):
        event.stop()
        # Need to calculate full path HKU/COMP3230... here and send it to parent
        full_cat_path = calendar_utils.get_full_path_from_node(event.node)
        self.post_message(self.CategoryChanged(full_cat_path))
        
        
class SidebarMainContainer(Container):
    CSS_PATH = "./demo_dock.css"
    def compose(self):
        yield CategoryTree("Categories")
    
    
class SidebarContainer(Vertical):
    CSS_PATH = "./demo_dock.css"
    def compose(self):
        yield Static("Side bar title", id="sidebar-header")
        yield SidebarMainContainer(id="sidebar-main-container")

        

        
