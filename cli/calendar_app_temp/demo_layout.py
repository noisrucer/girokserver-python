from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static

class Example(App):
    CSS_PATH = "./demo_layout.css"
    
    def compose(self):
        yield Horizontal(
            Vertical(
                Static("One"),
                Static("Two"),
                classes="column"
            ),
            Vertical(
                Static("Three"),
                Static("Four"),
                classes="column"
            )
        )