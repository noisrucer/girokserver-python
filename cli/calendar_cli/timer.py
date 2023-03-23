from time import monotonic
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Container
from textual.reactive import reactive
import api.task as task_api

class TimeDisplay(Static):
    """A widget to display elapsed time"""
    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)
    
    def on_mount(self):
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)
        
    def update_time(self):
        self.time = self.total + (monotonic() - self.start_time)
        
    def watch_time(self, time: float):
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")
        
    def start(self):
        self.start_time = monotonic()
        self.update_timer.resume()
        
    def stop(self):
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total
        
    def reset(self):
        self.total = 0
        self.time = 0


class Stopwatch(Static):
    """A stopwatch widget"""
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)
        if button_id == "start":
            time_display.start()
            self.add_class("started")
        elif button_id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()
    
    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch"""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay("23")


class StopwatchApp(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "../styles/stopwatch03.css"
    TITLE = "DEMO APP"
    SUB_TITLE = "WOWOOOWOW"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("a", "add_stopwatch", "Add"),
        ("r", "remove_stopwatch", "Remove"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Container(Stopwatch(), Stopwatch(), Stopwatch(), id="timers")
        
    def action_add_stopwatch(self):
        new_stopwatch = Stopwatch()
        self.query_one("#timers").mount(new_stopwatch)
        new_stopwatch.scroll_visible()
        
    def action_remove_stopwatch(self):
        timers = self.query("Stopwatch")
        if timers:
            timers.last().remove()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
