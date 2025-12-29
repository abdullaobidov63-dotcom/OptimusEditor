from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import (
    Button, Label, Header, Footer, TabbedContent, TabPane,
    ListView, ListItem, ContentSwitcher, Input, Tab,
    Markdown, TextArea, DirectoryTree
)
from textual.binding import Binding
#from textual.command import command

class AppEditor(App):
    CSS = """
    Screen {
        align-horizontal: center;
        align-vertical: middle;
    }

    #sidebar-container {
        width: 20%;
    }

    TabbedContent {
        height: 50%;
        margin-bottom: 1;
    }

    Vertical#center-container {
        dock: top;
        border: white;
        align: center middle;
        height: 20;
        width: 25;
    }
    """
    TITLE = "OptimusEditor"
    SUBTITLE = "File"

    # 2. ИСПРАВЛЕНО: action="command_palette" (без опечатки)
    BINDINGS = [
        Binding(key="ctrl+alt+p", action="command_palette", description="Палитра Команд")
    ]

    def __init__(self):
        super().__init__()
        self.open_files = {}
        self.text_area_text = '''print("Hello, World!")'''
        self.work_dir = "./"

    def compose(self) -> ComposeResult:
        yield Header(id="header")
        with Horizontal():
            with Vertical(id="sidebar-container"):
                if self.work_dir != "":
                    yield DirectoryTree(self.work_dir)
            with Vertical(id="main-content-container"):
                yield TextArea(self.text_area_text, language="python")
        yield Footer()

    def action_create_file(self):
        self.notify("File Created")

    def action_open_file(self):
        self.notify("File Opened")

if __name__ == "__main__":
    app = AppEditor()
    app.run()

