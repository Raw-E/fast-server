from fastapi import FastAPI
from fastapi.routing import APIRoute
from rich.table import Table
from rich.text import Text
from starlette.routing import Mount, WebSocketRoute

from fast_server.v1.utilities.logging_presentation import (
    COLORS,
    console,
    create_styled_table,
)
from foundation.v1 import CustomLogger

logger = CustomLogger(log_level="INFO")


def create_route_table() -> Table:
    table = create_styled_table()
    table.add_column("Type", style="cyan", width=10, justify="center")
    table.add_column("Method", style="green", width=8, justify="center")
    table.add_column("Endpoint Path", style="yellow", width=35, justify="left")
    table.add_column("Operation Class Name", style="blue", width=25, justify="left")
    table.caption = "[dim]✨ End of listed routes[/]"
    return table


def log_backend_routes(app: FastAPI) -> None:
    table = create_route_table()

    for route in app.routes:
        if isinstance(route, APIRoute):
            methods = ", ".join(route.methods)
            table.add_row("APIRoute", methods, route.path, route.name)
        elif isinstance(route, WebSocketRoute):
            table.add_row("WebSocket", "-", route.path, route.name)
        elif isinstance(route, Mount):
            table.add_row("Mount", "-", route.path, route.name)

    header = Text("🚀 FastAPI Server Routes", style=COLORS["title"])

    if len(app.routes) > 0:
        with console.capture() as capture:
            console.print(header)
            console.print(table)

        logger.info("\n" + capture.get())
    else:
        logger.info(header + "\nNo user-defined routes registered!")
