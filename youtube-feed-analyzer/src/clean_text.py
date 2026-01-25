import re
import unicodedata

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  #emoticons
        "\U0001F300-\U0001F5FF"  #symbols & pictographs
        "\U0001F680-\U0001F6FF"  #transport
        "\U0001F1E0-\U0001F1FF"  #flags
        "]+",
        flags = re.UNICODE
                )
        return emoji_pattern.sub("", text)


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = unicode.normalize("NFKD", text)

    text = text.lower()

    text = re.sub(r"[\(\{}.*?[\)\]]", "", text)

    text = re.sub(r"[@#]\w+", "", text)

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    text = text.strip()


    return text


def clean_list_of_titles(titles):
    """Utility for cleaning an entire list at once."""
    return [clean_text(t) for t in titles]



