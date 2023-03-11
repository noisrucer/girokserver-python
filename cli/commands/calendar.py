import typer
from rich import print
import calendar_app.calendar_app as calendar_app
import calendar_app.demo1 as demo1
import calendar_app.demo_css as demo_css
import calendar_app.demo_layout as demo_layout
import calendar_app.demo_grid as demo_grid
import calendar_app.demo_dock as demo_dock
import calendar_app.test as test

app = typer.Typer(rich_markup_mode='rich')

@app.command("cal")
def show_calendar():
    # app = calendar_app.StopwatchApp()
    demo_dock.Example().run()