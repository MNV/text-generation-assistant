import re


def normalize_whitespace(text: str) -> str:
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)
    text = re.sub(r"[ \t\n\r\f\v]+", " ", text)

    return text.strip()
