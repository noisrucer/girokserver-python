from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static

class GridLayout(App):
    CSS_PATH = "./demo_grid.css"
    
    def compose(self):
        # for i in range(6):
        #     yield Static(f"Cell {i}", classes="box")
        yield Static("One", classes="box")
        yield Static("Two [b](column-span: 2)", classes="box", id="two")
        yield Static("Three", classes="box")
        yield Static("Four", classes="box")
        yield Static("Five", classes="box")