import sys, os, json, requests
import numpy as np
import datetime as dt
from random import choice
from tqdm import tqdm
from time import sleep
from textual import on
from rich import print
from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Rule, Static
from textual.containers import Horizontal, Vertical, VerticalScroll

splashTexts = [
    "NOT working since 1970!",
    "Storms a' comin'!",
    "All I do is fetch, fetch, and fetch GRIBs.",
    "I'm bored with the splash text. Suggest some!",
    "You should use CAVE.",
    "Sorry man I ate the supercell.",
    "No ensembles here, sorry!",
    "This took a while to make.",
    "Life is like a box of GRIBs, you never know what you're forecasting."
]

splash = choice(splashTexts)

availableModels = ["GFS", "NAM", "HRRR", "RAP", "HiResW", "AIGFS", "NBM"]

with open("modelConfig.json", "r") as file:
    modelConfig = json.load(file)

class ModelButtons(Vertical):
    def compose(self) -> ComposeResult:
        for model in availableModels:
            yield Button(model, id=model, classes="models")

class TypeButtons(Vertical):
    pass

class MyApp(App):
    CSS_PATH = "tui.tcss"
    def compose(self) -> ComposeResult:
        with Vertical:
            yield VerticalScroll(Static("[i]Models[i]"), ModelButtons())
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.sub_title = splash


if __name__ == "__main__":
    app = MyApp()
    app.run()