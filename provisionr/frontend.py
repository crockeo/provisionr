from fastapi import FastAPI
from nicegui import ui


def init_frontend(app: FastAPI) -> None:
    @ui.page("/")
    def index_page() -> None:
        ui.label("Hello World!")

    ui.run_with(
        app,
        mount_path="/",
    )
