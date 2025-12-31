from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import (
    Button, Label, Header, Footer, TabbedContent, TabPane,
    ListView, ListItem, ContentSwitcher, Input, Tab,
    Markdown, TextArea, DirectoryTree, OptionList,
    Notification
)
from textual.binding import Binding

class App(App):
    def __init(self):
        pass
    
    def compose(self) -> ComposeResult:
        yield