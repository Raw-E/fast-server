from rich.console import Console
from rich.table import Table, box

# Shared console instance
console = Console()

# Common color scheme for logging presentation
COLORS = {
    "title": "bold cyan",
    "header": "bold magenta",
    "border": "bright_blue",
    "label": "cyan1",
    "value": "bright_yellow",
    "body": "yellow3",
}


def create_styled_table(
    *,
    title: str | None = None,
    header_style: str = COLORS["header"],
    border_style: str = COLORS["border"],
    box_type=box.SIMPLE_HEAD,
    padding: tuple = (0, 1),
    expand: bool = False,
) -> Table:
    """Creates a styled Rich table with consistent styling across the application."""
    return Table(
        title=title,
        show_header=True,
        header_style=header_style,
        box=box_type,
        padding=padding,
        expand=expand,
        border_style=border_style,
    )


def get_console_width() -> int:
    """Returns a standardized console width for consistent table sizing."""
    return min(console.width - 6, 160)


def calculate_column_widths(total_width: int, label_ratio: float = 0.3) -> tuple[int, int]:
    """Calculates standardized column widths for two-column tables."""
    label_width = max(30, int(total_width * label_ratio))
    value_width = total_width - label_width - 6
    return label_width, value_width
