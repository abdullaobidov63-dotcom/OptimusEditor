from pathlib import Path

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
    """Return a language key for pygments/get_lexer_by_name or 'text'. Uses pathlib to be OS-independent."""
    p = Path(file_path)
    ext = p.suffix.lower()
    if not ext:
        return "text"
    return LANG_MAP.get(ext, "text")