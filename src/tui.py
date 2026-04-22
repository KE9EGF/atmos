import sys, os, json, requests
import numpy as np
import datetime as dt
from tqdm import tqdm
from time import sleep
from textual.app import App, ComposeResult
from textual.widgets import Button, Header
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual import on

availableModels = ["GFS", "NAM", "HRRR", "RAP", "HiResW", "AIGFS", "NBM"]

with open("modelConfig.json", "r") as file:
    modelConfig = json.load(file)

class ModelButtons(Vertical):
    def compose(self) -> ComposeResult:
        for model in availableModels:
            yield Button(model, classes="model-buttons")

class TypeButtons(Vertical):
    pass

class MyApp(App):
    CSS_PATH = "tui.tcss"
    def compose(self) -> ComposeResult:
        yield VerticalScroll(ModelButtons())
        yield Header()


if __name__ == "__main__":
    app = MyApp()
    app.run()