def join_classes(*args) -> str:
    """
    Joins multiple class names into a single space-separated string.

    Parameters:
        *args: Arbitrary number of class name strings.

    Returns:
        str: Space-separated string of class names.
    """
    return " ".join(arg for arg in args if arg)


def validate_enum(enum_class, value):
    """
    Validates if a value belongs to a specific Enum.

    Parameters:
        enum_class (Enum): The Enum class to validate against.
        value: The value to check.

    Returns:
        bool: True if the value is a valid Enum member, False otherwise.
    """
    return value in {item.value for item in enum_class}
