from textual.app import ComposeResult
from textual.widget import (
    Widget,
    Button,
    Label
)

class DialogWindow(Widget):
    def __init__(self, text=""):
        self.text = text
    
    def compose(self) -> ComposeResult:
        text = Label(self.text)

        confirm_button = Button("Confirm", id="confirm_button")
        cancel_button = Button("Cancel", id="cancel_button")
        return "returned str value"