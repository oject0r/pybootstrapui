from .base import HTMLElement


class Table(HTMLElement):
    """
    Represents a Bootstrap-styled HTML table.

    Attributes:
        headers (list[str]): A list of table headers.
        rows (list[list[str]]): A list of rows, where each row is represented as a list of strings.
        classes (list[str] | None): Additional CSS classes for styling the table.
        id (str | None): A unique identifier for the table.
    """

    def __init__(
        self,
        headers: list[str] | None = None,
        rows: list[list[str]] | None = None,
        classes: list[str] | None = None,
        id: str | None = None,
    ):
        """
        Initializes a `Table` object with headers, rows, and optional CSS classes.

        Args:
            headers (list[str] | None): The table headers (optional).
            rows (list[list[str]] | None): The table rows (optional).
            classes (list[str] | None): Additional CSS classes for the table (optional).
            id (str | None): A unique identifier for the table (optional).

        Example:
            table = Table(
                headers=["Name", "Age", "City"],
                rows=[
                    ["Alice", "30", "New York"],
                    ["Bob", "25", "Los Angeles"]
                ],
                classes=["table-striped"]
            )
        """
        super().__init__(classes, id)
        self.headers = headers or []
        self.rows = rows or []

    def add_row(self, row: list[str]):
        """
        Adds a new row to the table.

        Args:
            row (list[str]): A list of strings representing the row cells.

        Example:
            table.add_row(["Charlie", "35", "Chicago"])
        """
        self.rows.append(row)

    def construct(self) -> str:
        """
        Constructs the HTML representation of the table.

        Returns:
            str: The HTML string representing the table.

        Example:
            html = table.construct()
            print(html)
        """
        header_html = "".join(
            [f"<th scope='col'>{header}</th>" for header in self.headers]
        )
        rows_html = "".join(
            [
                "<tr>" + "".join([f"<td>{cell}</td>" for cell in row]) + "</tr>"
                for row in self.rows
            ]
        )
        classes_str = " ".join((self.classes or []) + ["table"])
        id_attr = f'id="{self.id}"' if self.id else ""

        return f"""
        <table class="{classes_str}" {id_attr}>
            <thead>
                <tr>{header_html}</tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        """
