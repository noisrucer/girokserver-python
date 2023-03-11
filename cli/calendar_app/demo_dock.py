from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static, Label, Placeholder

class Example(App):
    CSS_PATH = "./demo_dock.css"
    
    def compose(self):
        with Horizontal(id="app-calendar"):
            with Vertical(id="sidebar-container"):
                yield Static("Side bar title", id="sidebar-header")
                with Container(id="sidebar-main-container"):
                    yield Static("Side bar main")
            with Vertical(id="calendar-container"):
                yield Static("23 March 2023", id="calendar-header")
                with Horizontal(id="calendar-main-container"):
                        with Vertical(classes="vertical"):
                            yield Static("Monday", classes="weekday-name")
                            yield Static(f"1", classes="calendar-cell")
                            yield Static(f"8", classes="calendar-cell")
                            yield Static(f"15", classes="calendar-cell")
                            yield Static(f"22", classes="calendar-cell")
                            yield Static(f"29", classes="calendar-cell")
                        with Vertical(classes="vertical"):
                            yield Static("Tuesday", classes="weekday-name")
                            yield Static(f"2", classes="calendar-cell")
                            yield Static(f"9", classes="calendar-cell")
                            yield Static(f"16", classes="calendar-cell")
                            yield Static(f"23", classes="calendar-cell")
                            yield Static(f"30", classes="calendar-cell")
                        with Vertical(classes="vertical"):
                            yield Static("Wednesday", classes="weekday-name")
                            yield Static(f"3", classes="calendar-cell")
                            yield Static(f"10", classes="calendar-cell")
                            yield Static(f"17", classes="calendar-cell")
                            yield Static(f"24", classes="calendar-cell")
                            yield Static(f"31", classes="calendar-cell")
                        with Vertical(classes="vertical"):
                            yield Static("Thursday", classes="weekday-name")
                            yield Static(f"4", classes="calendar-cell")
                            yield Static(f"11", classes="calendar-cell")
                            yield Static(f"18", classes="calendar-cell")
                            yield Static(f"25", classes="calendar-cell")
                            yield Static(f"1", classes="calendar-cell")
                        with Vertical(classes="vertical"):
                            yield Static("Friday", classes="weekday-name")
                            yield Static(f"5", classes="calendar-cell")
                            yield Static(f"12", classes="calendar-cell")
                            yield Static(f"19", classes="calendar-cell")
                            yield Static(f"26", classes="calendar-cell")
                            yield Static(f"2", classes="calendar-cell")
                        with Vertical(classes="vertical"):
                            yield Static("Saturday", classes="weekday-name")
                            yield Static(f"6", classes="calendar-cell")
                            yield Static(f"13", classes="calendar-cell")
                            yield Static(f"20", classes="calendar-cell")
                            yield Static(f"27", classes="calendar-cell")
                            yield Static(f"3", classes="calendar-cell")
                        with Vertical(classes="vertical"):
                            yield Static("Sunday", classes="weekday-name")
                            with Static(classes="calendar-cell"):
                                yield Static(f"7", classes="test")
                            with Static(classes="calendar-cell"):
                                yield Static(f"14")
                            with Static(classes="calendar-cell"):
                                yield Static(f"21")
                            with Static(classes="calendar-cell"):
                                yield Static(f"28")
                            with Static(classes="calendar-cell"):
                                yield Static(f"4")
                        # with Container(id=f"calendar-cell-{i}", classes="calendar-cell"):
                        #     yield Static(f"cell {i}")
        yield Footer()
            