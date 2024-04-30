from asyncio import sleep

import flet as ft

from src.constants import PAGE_HEIGHT, PAGE_WIDTH
from src.views.cases.views import CaseDetailView, CaseListView
from src.views.router import Router


async def main(page: ft.Page):
    page.title = "Cases"
    page.window_height = PAGE_HEIGHT
    page.window_width = PAGE_WIDTH
    page.window_frameless = True
    page.window_resizable = False

    page.window_center()

    await sleep(0.1)  # для того что бы не было белого окна вначале

    Router(page, [CaseListView, CaseDetailView])

    page.go("/")


if __name__ == "__main__":
    ft.app(main, view=ft.FLET_APP_HIDDEN)
