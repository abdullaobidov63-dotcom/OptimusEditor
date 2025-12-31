import ctypes
from ctypes import wintypes

def open_file_dialog_windows():
    # создаём COM объект FileOpenDialog
    from comtypes.client import CreateObject
    from comtypes.gen import Shell32

    dlg = CreateObject(Shell32.FileOpenDialog)
    dlg.SetTitle("Выберите файл")
    hr = dlg.Show(None)
    if hr != 0:
        return None  # отмена пользователем
    result = dlg.GetResult()
    return result.GetDisplayName(0)  # возвращает полный путь к файлу

# пример использования
selected_file = open_file_dialog_windows()
print("Выбран файл:", selected_file)