from textual.app import (
    App, 
    ComposeResult
)

# from loguru import logger
from core.text_data import texts
#from textual.events import Button.Pressed
# from textual.events import Button.Pressed
from textual.widgets import (
    Button, 
    Label, 
    Header, 
    TabbedContent,
    TabPane,
    ListView,
    ListItem, 
    ContentSwitcher,
    Input,
    Tab,
    Markdown
)

try:
    from core.custom_widgets.dialog_window import DialogWindow
    print("Widget DialogWindow secussfully imported from core.custom_diwgets.dialog_window.py")
except:
    print("ImportError")

#from textual.containters import (
#    Horizontal,
#    Vertical
#)

class AppEditor(App):
    CSS = """
    Screen {
        align-horizontal: center;
        align-vertical: middle;
    }

    #get_started_btn {
        width: 30%;
    }

    #welcome-label {
        align: center middle;
        margin-bottom: 2;
    }

    TabbedContent {
        height: 50%;
        margin-bottom: 1;
    }
    """
    TITLE = "OptimusEditor"
    SUBTITLE = "File"

    def __init__(self):
        super().__init__()
        self.open_files = {}
        self.dialog_window_text = texts["dialog"]["create_file"]["text"]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Welcome to OptimusEditor!", id="welcome-label")
        yield Button("Start Coding -->", id="get_started_btn", variant="primary")

        yield Button("Open File", id="open_button")
        yield Button("Close File", id="close_button")
        yield Button("Create File", id="create_file")
        yield Button("Delete File", id="delete_file")
        
        """ 
        |======================================================|
        |                   RIGHT                              |
        |======================================================|
        """

        """ 
        |======================================================|
        |                    LEFT                              |
        |======================================================|
        """
        yield ListView(
            ListItem(Label(self.dialog_window_text)),
            id="listview"
        )
        """ 
        |======================================================|
        |                   CENTER                             |
        |======================================================|
        """
        """
            tab_name: {
                in_tab: "wadasdwads",
            }
        """
        # Вкладка, которая будет открыта по умолчанию
        #                    |
        with TabbedContent(initial="Welcome"):
            with TabPane("Welcome"):
                yield Markdown("# Welcome To Optimus Editor")
            with TabPane("Second Tab"):
                yield Markdown("# Second Page")
        yield Input(id="input")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "open_button":
            self.open_file()
        elif event.button.id == "close_button":
            self.close_current_tab()
        elif event.button.id == "":
            pass

    def on_tabbed_content_tab_activated(self, event) -> None:
        self.notify(f"Переключено на вкладку: {event.tab.label_text}")
    
    def open_file(self, file_name):
        # Проверяем, есть ли вкладка с таким файлом, если есть, то просто меняем активную вкладку на существующцую
        for tab in self.query(TabPane):
            if tab.id == filename:
                self.query(TabbedContent).active = filename
            else:
                pass
    
    def close_current_tab():
        pass
    
    def create_file(self, filename):
        pass
    
    def delete_file(self, filename):
        pass

if __name__ == "__main__":
    app = AppEditor()
    app.run()
