LANG_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".java": "java",
    ".rb": "ruby",
    ".html": "html",
    ".css": "css",
    ".md": "markdown",
    ".c": "c",
    ".cs": "csharp",
    ".cpp": "c++",
    ".ts": "typescript",
    ".json": "json"
}

def get_file_ext(file_path: str) -> str:
    # ищем точку в последней части пути
    parts = file_path.rsplit("/", 1)  # разделяем путь на dirs и имя файла
    file_name = parts[-1]             # берём только имя файла

    if "." not in file_name:
        return "text"                 # нет расширения → plain text

    # берём расширение с точки до конца
    ext = "." + file_name.split(".")[-1].lower()

    if ext in LANG_MAP:
        return LANG_MAP[ext]
    else:
        return "text"