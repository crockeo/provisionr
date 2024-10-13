from fastapi import FastAPI
from nicegui import ui

from provisionr.models import create_session
from provisionr.services import get_team, get_teams


def init_frontend(app: FastAPI) -> None:
    def page_header() -> None:
        with ui.row().classes("flex flex-row justify-between w-screen"):
            with ui.item(on_click=lambda: ui.navigate.to("/")).classes("flex flex-row align-middle rounded space-x-2 justify-center"):
                ui.icon("home").classes()
                ui.label("Provisionr")
    
    @ui.page("/")
    async def index_page() -> None:
        page_header()
        
        async with create_session() as session:
            teams, continuation_token = await get_teams(session)

            with ui.list().props("bordered"):
                ui.item_label("Teams").props("header").classes("font-bold")
                ui.separator()
                for team in teams:
                    with ui.item():
                        ui.link(team.name, target=f"/teams/{team.slug}")

    @ui.page("/teams/{team_slug:str}")
    async def team_page(team_slug: str) -> None:
        page_header()

        columns = [
            {
                "field": "maintainer",
                "label": "Maintainer",
            },
            {
                "field": "name",
                "label": "Name",
            },
            {
                "field": "username",
                "label": "Username",
            },
       ]
        
        async with create_session() as session:
            team = await get_team(session, team_slug)

        with ui.card():
            ui.label(team.name).props("header").classes("text-xl font-bold")
            with ui.list():
                with ui.row().classes("grid grid-cols-3"):
                    ui.label("Name").classes("font-bold italic")
                    ui.label("Username").classes("font-bold italic")
                    ui.label("Is Maintainer?").classes("font-bold italic")
                for member in team.members:
                    with ui.row().classes("grid grid-cols-3"):
                        ui.label(member.name)
                        ui.label(member.username).classes("italic")
                        if member.maintainer:
                            with ui.row():
                                ui.icon("star", color="gold")
                                ui.label("Maintainer")
        
        # ui.table(rows=rows, columns=columns)

    ui.run_with(
        app,
        mount_path="/",
    )
