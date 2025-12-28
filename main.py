from textual.app import App
from textual.widgets import *

class AppEditor(App):
    CSS_FILE_PATH = "css/main_page.tcss"

    # Метод "саздания" виджетов(т.е. внутри метода создаются виджеты)
    def compose(self) -> ComposeResult:
        yield Label("Welcome to OptimusEditor!")
        yield Button("Get Started ->", id="get_started_btn", variant="primary")
    
    def on_button_pressed(self) -> None:
        self.exit()

if __name__ == "__main__":
    app = AppEditor()
    app.run()