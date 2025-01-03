from .base import HTMLElement


class Table(HTMLElement):
    """
    A class for creating Bootstrap tables.

    Attributes:
            - `headers` (list[str]): The table headers.
            - `rows` (list[list[str]]): The table rows.
            - `classes` (list[str] | None): Additional CSS classes for the table.
            - `unique_id` (str | None): Unique identifier for the table.
    """

    def __init__(
        self,
        headers: list[str] | None = None,
        rows: list[list[str]] | None = None,
        classes: list[str] | None = None,
        unique_id: str | None = None,
    ):
        """
        Initializes the Table object with headers, rows, and optional CSS classes.

        Parameters:
                - `headers` (list[str] | None): The table headers (optional).
                - `rows` (list[list[str]] | None): The table rows (optional).
                - `classes` (list[str] | None): Additional CSS classes for the table (optional).
                - `unique_id` (str | None): Unique identifier for the table (optional).

        Example:
                ```
                table = Table(
                        headers=["Name", "Age", "City"],
                        rows=[["Alice", "30", "New York"], ["Bob", "25", "Los Angeles"]],
                        classes=["table-striped"]
                )
                ```
        """
        super().__init__(classes, unique_id)
        self.headers = headers or []
        self.rows = rows or []

    def add_row(self, row: list[str]):
        """
        Adds a row to the table.

        Parameters:
                - `row` (list[str]): A list of strings representing the row cells.

        Example:
                ```
                table.add_row(["Charlie", "35", "Chicago"])
                ```
        """
        self.rows.append(row)

    def construct(self) -> str:
        """
        Constructs the HTML for the table.

        Returns:
                - `str`: The HTML representation of the table.

        Example:
                ```
                html = table.construct()
                print(html)
                ```
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
