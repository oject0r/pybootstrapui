def join_classes(*args) -> str:
    """Joins multiple class names into a single
    space-separated string.
    """
    return " ".join(arg for arg in args if arg)


def validate_enum(enum_class, value):
    """Validates if a value belongs to a specific
    Enum.
    """
    return value in {item.value for item in enum_class}
