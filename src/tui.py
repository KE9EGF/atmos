import sys, os, json, requests
import numpy as np
import datetime as dt
from tqdm import tqdm
from time import sleep
from textual.app import App, ComposeResult
from textual.widgets import Button, Header
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual import on

class MyApp(App):
    CSS_PATH = "tui.tcss"
    def compose(self) -> ComposeResult:
        yield Button("Hello!", id="test", variant="error")
        yield Header()


if __name__ == "__main__":
    app = MyApp()
    app.run()