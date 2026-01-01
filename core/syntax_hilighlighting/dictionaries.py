import re

python_dictionary = {
    "comment": r"# .*",
    "keyword": r"\b(if|else|elif|while|for|try|except|def|class|print)\b",
    "number":  r"\d+",
    "string":  r"(\".*?\"|'.*?')"
}

