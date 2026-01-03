from pathlib import Path
from textual.app import App, ComposeResult, Screen
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, DirectoryTree, TextArea, Markdown, TabbedContent, TabPane, Button, Label, Input, Static
from textual.timer import Timer
from textual.binding import Binding
from textual.events import Key
from core.highlight import *
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.formatters import TerminalFormatter
from pygments import highlight as pyg_highlight
from pygments.util import ClassNotFound
from rich.text import Text
import subprocess
import re

"""
FIXME: Сделать адекватные вкладки, а не только с терминалом.
TODO: При починке компа, начать изучение трёхлетнего RoadMap по изучению IT в целом.
TODO: И ещё, до конца сделать комменты для кода. 
"""

# Класс для отображения подсвеченного кода
class CodeView(Static):
    # Метод для обновления самого текста, Text из Rich
    def update_code(self, rich_text: Text):
        self.update(rich_text)

# -----------------------------
# Экран выбора папки
# -----------------------------

# Экран выбора Папки(если пользователь выберет файл, то редактор откроет папку, в котором находится сам файл)
class OpenFolderPage(Screen):
    # Стили для самой странички
    CSS = """
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
    # Название окна, наименование.  
    TITLE = "OptimusEditor"
    SUBTITLE = "File"

    # Горячие клавиши
    BINDINGS = [
        Binding(key="ctrl+alt+p", action="command_palette", description="Палитра Команд")
    ]

    # Метод инициализации класса
    def __init__(self):
        super().__init__()
        #  Для открытых файлов.
        self.open_files = {}
        # Текст в редакторе.
        self.text_area_text = '''print("Hello, World!")'''
        # Директория, в которой будем находится
        self.work_dir = "./"

    # Распологаем элементы(просто для отрисовки)
    def compose(self) -> ComposeResult:
        # Верхний колонтитул
        yield Header(id="header")
        # Текст
        yield Label("Выберите папку (только папку)")

        # Дерево папок
        yield DirectoryTree("C:/", id="tree")

        # Кнопки подтверждения и отмены
        yield Button("Выбрать", id="select")
        yield Button("Отменить", id="cancel")

    # Метод, срабатывающий при нажатии всех кнопок в приложении.
    def on_button_pressed(self, event):
        # Нажатие кнопки
        # Проверяем какая кнопка нажата
        if event.button.id == "select":
            # Если это кнопка "Выбрать папку", то --\
            if self.current_folder is not None: #   |
                # Передаём выбранную папку в Editor/
                self.app.push_screen(Editor(self.current_folder))
            else:
                # Если папка/файл не выбран.
                self.notify("Вы не выбрали папку!")
        # Нажата кнопка "Отменить", выходим из программы.
        elif event.button.id == "cancel":
            self.app.exit()

    # Метод, вызывающийся, когда пользователь выбрал элемент из DirectoryTree(выбрал папку/файл)
    def on_directory_tree_file_selected(self, event):
        # Когда выбирается файл или папка в дереве
        # Узнаём местонахождение данного выбранного файла на диске, и конвертируем его в класс Path.
        path = Path(event.path)
        # Если выбранный эелемент -- Папка
        if path.is_dir():
            self.current_folder = path  # если выбрана папка — используем её
        else:
            self.current_folder = path.parent  # если файл — берём его папку
        # Уведомление о выборе определённого объекта из DirectoryTree.
        self.notify(f"{self.current_folder} : Folder selected")

# -----------------------------
# Основной редактор
# -----------------------------
class Editor(Screen):
    # Стили для редактора
    CSS_PATH = "./css/editor.tcss"
    # Горячие клавиши
    BINDINGS = [
        Binding(key="ctrl+s", action="save_file", description="Сохранить файл"),
        Binding(key="ctrl+o", action="open_folder", description="Открыть Папку")
    ]

    # Метод инициализации класса
    def __init__(self, work_dir: Path):
        super().__init__()
        self.work_dir = work_dir       # Папка, открытая пользователем
        self.current_file: Path = None # Единая переменная для выбранного файла
        self.text_area_text = "print('Hello, World!')"  # Начальный текст

        self.cmd_input = "" # для ввода в терминале
        self.cmd_send = subprocess.run(self.cmd_input, shell=True, capture_output=True, text=True)# Для ввода комманд в терминале
        self.cmd_output = self.cmd_send.stdout # Получаем вывод команды

    # Метод, вызывается только тогда, когда приложение отобразило элементы интерфейса
    def on_mount(self):
        self._latest_text = "" # Последний текст/символ, который мы вводили
        # Обновляем подсветку каждые 0.25 секунды
        self._highlight_timer: Timer = self.set_interval(0.25, self.highlight_code) # Таймер

    def compose(self) -> ComposeResult:
        # Верхний и нижний колонтитулы
        yield Header()
        yield Footer()
            # Основная панель
        # Основное содержимое
        with Vertical(id="main-content-container"):
            # Табы
            with TabbedContent():
                # Вкладка с папкой / кодом по умолчанию
                tab_name = str(self.work_dir.name if self.work_dir else "New Tab")
                with TabPane(tab_name):
                    with Horizontal():
                        # Виджет, позволяющий отображать, и редактировать текст.
                        yield TextArea(self.text_area_text, language="python", id="text_area")
                        # Также виджет, но нужен для подсветки синтаксиса.
                        yield CodeView(id="code_view")
                # Вкладка с терминалом
                with TabPane("Terminal"):
                    # Распологаем TextArea, содержимое которого будет вывод консоли
                    yield TextArea(self.cmd_output, id="cmd_output_text_area")
                    # Так же TextArea, но содержимое будет введённая пользователем команда в терминале
                    yield TextArea(self.cmd_input, id="cmd_input_text_area")
                    # Кнопка запуска введённой команды
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
        elif focused and focused.id == "text_area":
            # Любая клавиша в текстовой области — запустить обновление подсветки
            self.highlight_code()
    
    async def on_button_pressed(self, event: Key):
        id = event.button.id
        if id == "cmd_run_btn":
            self.cmd_output = subprocess.run(self.query_one("#cmd_input_text_area").text, shell=True, capture_output=True, text=True).stdout
            self.query_one("#cmd_output_text_area").text = self.cmd_output
    
    def highlight_code(self):
        try:
            ta = self.query_one(TextArea)
        except Exception:
            return

        code = ta.text or ""
        # определяем язык подсветки: сначала используем свойство TextArea, иначе guess по текущему файлу
        lang = getattr(ta, "language", None) or (get_file_ext(str(self.current_file)) if self.current_file else "text")

        try:
            lexer = get_lexer_by_name(lang)
        except ClassNotFound:
            lexer = PythonLexer()

        ansi = pyg_highlight(code, lexer, TerminalFormatter())
        rich_text = Text.from_ansi(ansi)

        try:
            self.query_one(CodeView).update(rich_text)
        except Exception:
            # если нет CodeView — игнорируем
            pass


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

