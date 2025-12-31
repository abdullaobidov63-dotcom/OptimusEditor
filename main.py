from pathlib import Path
from textual.app import App, ComposeResult, Screen
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import (
    Button, Label, Header, Footer, TabbedContent, TabPane,
    ListView, ListItem, ContentSwitcher, Input, Tab,
    Markdown, TextArea, DirectoryTree
)
from textual.binding import Binding
#from textual.command import command
from core.highlight import *
from textual.events import Key

open_folder = None

class OpenFolderPage(Screen):
    def __init__(self):
        super().__init__()
        self.selected_folder = None

    
    def compose(self) -> ComposeResult:
        yield Label("Выберите папку(только папку)")
        yield DirectoryTree("C:/", id="tree")
        yield Button(label="Выбрать", id="select")
        yield Button(label="Отменить", id="cancel")

    def on_button_pressed(self, event):
        global open_folder
        id = event.button.id
        if id == "select":
            global open_folder
            if open_folder is not None:
                self.push_screen(AppEditor, Editor)
            else:
                self.notify("Вы не выбрали файл!")
        elif id == "cancel":
            self.app.exit()
    
    def on_directory_tree_file_selected(self, event):
        global open_folder
        open_folder = event.path

class Editor(Screen):
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
        Binding(key="ctrl+alt+p", action="command_palette", description="Палитра Команд"),
        Binding(key="ctrl+s", action="save_file", description="Save writted code")
    ]

    def __init__(self):
        super().__init__()
        self.open_files = {}
        self.text_area_text = '''print("Hello, World!")'''
        self.work_dir = open_folder
        self.current_file = None # Initialization

    def compose(self) -> ComposeResult:
        yield Header(id="header")
        with Horizontal():
            with Vertical(id="sidebar-container"):
                if self.work_dir != "":
                    yield DirectoryTree(self.work_dir)
            with Vertical(id="main-content-container"):
                yield TextArea(self.text_area_text, language="python", id="text_area")
        yield Footer()

    def action_save_file(self):
        if self.current_file == None:
            self.notify("Выберите файл прежде чем его сохранить!")
        
        f = open(self.current_file, "w", encoding="UTF-8")

        try:
            f.write(self.query_one(TextArea).text)
        finally:
            f.close()
            self.notify(f"{self.current_file} - Сохранён успешно.")
    
    def on_directory_tree_file_selected(self, event):
        self.current_file = event.path
        self.text_area_text = self.current_file.read_text(encoding="UTF-8")
        text_area = self.query_one(TextArea)
        text_area.text = self.text_area_text

        file_language = get_file_ext(str(self.current_file))
        text_area.language = file_language

        self.notify(f"{self.current_file}")
    
    async def on_key(self, event: Key):
        focused = self.focused
        if event.key == "tab" and focused and focused.id == "text_area":
            focused.insert_text("    ")
            event.stop()

class AppEditor(App):
    async def on_ready(self):
        await self.push_screen(OpenFolderPage())

if __name__ == "__main__":
    app = AppEditor()
    app.run()

