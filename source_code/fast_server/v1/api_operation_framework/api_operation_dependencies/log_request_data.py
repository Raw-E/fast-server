import datetime
import json
from typing import Any, Dict, List, Union

from fastapi import Request
from rich.panel import Panel
from rich.table import Table, box
from rich.text import Text

from fast_server.v1.utilities.logging_presentation import (
    COLORS,
    calculate_column_widths,
    console,
    create_styled_table,
    get_console_width,
)
from foundation.v1 import CustomLogger

logger = CustomLogger(log_level="INFO")


async def log_request_data(request: Request) -> None:
    try:
        total_width = get_console_width()
        label_width, value_width = calculate_column_widths(total_width)

        route = request.scope.get("route")
        tables: List[Union[Text, Table, Panel]] = [Text("📝 Received API Request", style=COLORS["title"])]

        def add_section(title: str, data: Dict[str, Any]) -> None:
            if data:
                table = create_styled_table(
                    title=f"✨ {title} ✨",
                    box_type=box.ROUNDED,
                    padding=(0, 2),
                    expand=False,
                )
                table.add_column(
                    "Field" if title == "Request Metadata" else title.split()[-1],
                    style=COLORS["label"],
                    justify="right",
                    width=label_width,
                    no_wrap=True,
                    overflow="fold",
                )
                table.add_column(
                    "Value",
                    style=COLORS["value"],
                    justify="left",
                    width=value_width,
                    overflow="fold",
                )
                for key, value in data.items():
                    table.add_row(str(key), str(value))
                tables.append(table)

        add_section(
            "Request Metadata",
            {
                "Operation": route.name if route else "Unknown",
                "Endpoint": str(request.url),
                "Method": request.method,
                "Timestamp": datetime.datetime.now(datetime.UTC).isoformat() + "Z",
                "Client IP": request.client.host if request.client else "Unknown",
            },
        )

        add_section("Request Headers", dict(request.headers))
        add_section("Request Query Parameters", dict(request.query_params))

        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body_bytes = await request.body()
                body_str = json.dumps(json.loads(body_bytes.decode("utf-8")), indent=2)
            except json.JSONDecodeError:
                body_str = body_bytes.decode("utf-8")

            tables.append(
                Panel(
                    Text(body_str, style=COLORS["body"], overflow="fold", no_wrap=False),
                    title="✨ Request Body ✨",
                    border_style=COLORS["border"],
                    box=box.ROUNDED,
                    padding=(1, 2),
                    width=total_width,
                    expand=False,
                )
            )

        with console.capture() as capture:
            console.print()
            for table in tables:
                console.print(table)
                console.print()

        logger.info("\n" + capture.get())

    except Exception as error:
        logger.error(f"Error in log_request_data: {str(error)}")
