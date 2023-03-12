from time import monotonic
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Welcome, Label
from textual.containers import Container
from textual.reactive import reactive
import api.task as task_api

TEXT = """I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
I will permit it to pass over me and through me.
And when it has gone past, I will turn the inner eye to see its path.
Where the fear has gone there will be nothing. Only I will remain."""

class WelcomeApp(App):
    TITLE = "DEMO APP"
    SUB_TITLE = "WOWOOOWOW"
    
    def on_mount(self):
        self.widget1.styles.background = "purple"
        self.widget2.styles.background = "blue"
        self.widget1.styles.height="3fr"
        self.widget2.styles.height="1fr"
        self.widget2.styles.padding = 3
    
    def compose(self):
        self.widget1 = Static(TEXT)
        yield self.widget1
        self.widget2 = Static(TEXT)
        yield self.widget2
        
        # yield Welcome()
    
        
    def on_button_pressed(self):
        self.exit()