class GridHelper:
    """A helper class for generating Bootstrap
    grid classes."""

    @staticmethod
    def generate_column_class(size: str, columns: int) -> str:
        """Generates a grid column class for a
        specific size and column count.
        """
        if not (1 <= columns <= 12):
            raise ValueError("Columns must be between 1 and 12.")
        return f"col-{size}-{columns}"

    @staticmethod
    def generate_gap_class(size: str, gap: int) -> str:
        """Generates a grid gap class for a
        specific size.
        """
        if not (0 <= gap <= 5):
            raise ValueError("Gap size must be between 0 and 5.")
        return f"gap-{size}-{gap}"
