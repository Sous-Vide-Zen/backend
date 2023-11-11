def shorten_text(full_text, n) -> str:
    """
    Shorten text to n characters with rounding by last word
    """
    short_text = full_text[:100]
    if len(full_text) > n and full_text[n] != "":
        short_text = short_text[: short_text.rfind(" ")]
    return short_text
