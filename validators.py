def is_valid_name(name: str) -> bool:
    if not name:
        return False
    for char in name:
        if not (char.isalpha() or char == " "):
            return False
    return True
