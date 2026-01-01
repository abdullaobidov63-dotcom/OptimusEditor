from pathlib import Path
from textual.app import App, ComposeResult, Screen
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, DirectoryTree, TextArea, Markdown, TabbedContent, TabPane, Button, Label, Input
from textual.binding import Binding
from textual.events import Key
from core.highlight import *
import subprocess
import re

# -----------------------------
# Экран выбора папки
# -----------------------------
class OpenFolderPage(Screen):

    CSS_PATH = "./css/open_folder_page.tcss"

    def __init__(self):
        super().__init__()
        self.current_folder = None  # Хранит выбранную папку

    def compose(self) -> ComposeResult:
        yield Label("Выберите папку (только папку)")

        # Дерево папок
        yield DirectoryTree("C:/", id="tree")

        # Кнопки подтверждения и отмены
        yield Button("Выбрать", id="select")
        yield Button("Отменить", id="cancel")

    def on_button_pressed(self, event):
        # Нажатие кнопки
        if event.button.id == "select":
            if self.current_folder is not None:
                # Передаём выбранную папку в Editor
                self.app.push_screen(Editor(self.current_folder))
            else:
                self.notify("Вы не выбрали папку!")
        elif event.button.id == "cancel":
            self.app.exit()

    def on_directory_tree_file_selected(self, event):
        # Когда выбирается файл или папка в дереве
        path = Path(event.path)
        if path.is_dir():
            self.current_folder = path  # если выбрана папка — используем её
        else:
            self.current_folder = path.parent  # если файл — берём его папку
        self.notify(f"{self.current_folder} : Folder selected")


# -----------------------------
# Основной редактор
# -----------------------------
class Editor(Screen):
    CSS_PATH = "./css/editor.tcss"
    # Горячие клавиши
    BINDINGS = [
        Binding(key="ctrl+s", action="save_file", description="Сохранить файл"),
        Binding(key="ctrl+o", action="open_folder", description="Открыть Папку")
    ]

    def __init__(self, work_dir: Path):
        super().__init__()
        self.work_dir = work_dir       # Папка, открытая пользователем
        self.current_file: Path = None # Единая переменная для выбранного файла
        self.text_area_text = "print('Hello, World!')"  # Начальный текст

        self.cmd_input = "" # для ввода в терминале
        self.cmd_send = subprocess.run(self.cmd_input, shell=True, capture_output=True, text=True)
        self.cmd_output = self.cmd_send.stdout # Получаем вывод команды

    def on_mount(self):
        self._latest_text = "" # Последний текст/символ, который мы вводили
        self._highlight_timer: Timer = self.set_interval(0.05, self.check_text)
    
    def check_text(self):
        ta = self.query_one(TextArea)
        code = ta.text
        
        if code != self._latest_text:
            self.notify("Changed")
        else:
            pass

    def compose(self) -> ComposeResult:
        # Верхний и нижний колонтитулы
        yield Header()
        yield Footer()

        with Horizontal():
            # Левая панель — дерево папок
            with Vertical(id="sidebar-container"):
                if self.work_dir:
                    yield DirectoryTree(str(self.work_dir))

            # Основная панель
            with Vertical(id="main-content-container"):
                with TabbedContent():
                    # Вкладка с папкой / кодом по умолчанию
                    tab_name = str(self.work_dir.name if self.work_dir else "New Tab")
                    with TabPane(tab_name):
                        yield TextArea(self.text_area_text, language="python", id="text_area")
                    with TabPane("Terminal"):
                        yield TextArea(self.cmd_output, id="cmd_output_text_area")
                        yield TextArea(self.cmd_input, id="cmd_input_text_area")
                        yield Button("Run Command", id="cmd_run_btn")

                    # Вкладка Markdown — появится только если выбран файл .md
                    if self.current_file and self.current_file.suffix == ".md":
                        with TabPane(self.current_file.name):
                            md_text = self.current_file.read_text(encoding="utf-8")
                            yield Markdown(md_text)

    # -----------------------------
    # Сохранение файла
    # -----------------------------
    def action_save_file(self):
        if not self.current_file:
            self.notify("Выберите файл прежде чем сохранять!")
            return

        # Сохраняем содержимое TextArea в файл
        content = self.query_one(TextArea).text
        self.current_file.write_text(content, encoding="utf-8")
        self.notify(f"{self.current_file} - Сохранён успешно.")
    
    def action_open_folder(self):
        self.app.push_screen(OpenFolderPage())

    # -----------------------------
    # Выбор файла из дерева
    # -----------------------------
    def on_directory_tree_file_selected(self, event):
        path = Path(event.path)
        if path.is_file():
            self.current_file = path        # Запоминаем выбранный файл
            self.text_area_text = path.read_text(encoding="utf-8")
            text_area = self.query_one(TextArea)
            text_area.text = self.text_area_text

            # Определяем язык подсветки (для твоей функции get_file_ext)
            text_area.language = get_file_ext(str(self.current_file))

            self._latest_text = self.text_area_text

            self.notify(f"Файл выбран: {self.current_file}")

    # -----------------------------
    # Вставка таба в TextArea
    # -----------------------------
    async def on_key(self, event: Key):
        focused = self.focused
        if event.key == "tab" and focused and focused.id == "text_area":
            focused.insert_text("    ")
            event.stop()
        elif event.key == "enter" and focused and focused.id == "cmd_input_text_area":
            self.query_one("#cmd_output_text_area").insert_text(self.cmd_output)
        elif event.key != "tab" or "enter" and focused and focused.id == "text_area":
            self.highlight_code()
    
    async def on_button_pressed(self, event: Key):
        id = event.button.id
        if id == "cmd_run_btn":
            self.cmd_output = subprocess.run(self.query_one("#cmd_input_text_area").text, shell=True, capture_output=True, text=True).stdout
            self.query_one("#cmd_output_text_area").text = self.cmd_output
    
    def highlight_code(self):
        ta = self.query_one(TextArea)
        code = ta.text
        for line in code:
            print(line)


# -----------------------------
# Основное приложение
# -----------------------------
class AppEditor(App):
    async def on_ready(self):
        # При старте открываем экран выбора папки
        await self.push_screen(OpenFolderPage())


# -----------------------------
# Запуск
# -----------------------------
if __name__ == "__main__":
    app = AppEditor()
    app.run()