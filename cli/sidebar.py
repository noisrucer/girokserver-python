from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static, Label, Placeholder, Tree
from textual.messages import Message
from textual.widget import Widget

import api.category as category_api
import utils.calendar as calendar_utils
from rich.style import Style
from rich.text import Text
from textual import log


class CategoryTree(Tree):
    CSS_PATH = "./demo_dock.css"
    cats = dict()
    can_focus = True
    can_focus_children = True
    auto_expand=False
    
    class CategoryChanged(Message):
        def __init__(self, cat_path: str):
            super().__init__()
            self.cat_path = cat_path
    
    def on_mount(self):
        self.cats = category_api.get_categories()
        self.root.expand()
        
        for cat in self.cats:
            top_cat = self.root.add(cat, expand=True)
            top_cat.allow_expand = True
            calendar_utils.build_category_tree(top_cat, self.cats[cat])
            
    def on_key(self, evt):
        if evt.key == "j":
            self.action_cursor_down()
        elif evt.key == "k":
            self.action_cursor_up()
        elif evt.key == "o":
            self.action_select_cursor()
            
    def render_label(self, node, base_style: Style, style: Style):
        node_label = node._label.copy()
        node_label.stylize(style)
        icon = "📂 " if node.children._wrap else "📄 "
        if node.parent is None:
            icon = "📖 "
        log("QQQQ", node.parent)
        prefix = (icon, base_style)
        text = Text.assemble(prefix, node_label)
        return text
        
            
    def on_tree_node_selected(self, event: Tree.NodeSelected):
        event.stop()
        # Need to calculate full path HKU/COMP3230... here and send it to parent
        full_cat_path = calendar_utils.get_full_path_from_node(event.node)
        self.post_message(self.CategoryChanged(full_cat_path))
        
        
class SidebarMainContainer(Container):
    CSS_PATH = "./demo_dock.css"
    def compose(self):
        yield CategoryTree("All Categories")
    
    
class SidebarContainer(Vertical):
    CSS_PATH = "./demo_dock.css"
    def compose(self):
        yield Static("Side bar title", id="sidebar-header")
        yield SidebarMainContainer(id="sidebar-main-container")

        

        
