from textual.app import App, ComposeResult
from textual.widgets import Rule, Static

class RuleApp(App):
    CSS = """
    Rule {
        margin: 1 0;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Section One")
        yield Rule(line_style="thick") # Add horizontal rule
        yield Static("Section Two")

if __name__ == "__main__":
    app = RuleApp()
    app.run()
