import flet as ft
from flet_route import Routing

from . import BaseViewContainer


class Router(Routing):
    """Руководит представлениями на базе BaseViewContainer"""

    def __init__(self, page: ft.Page, views: list[type[BaseViewContainer]]):
        super().__init__(page, [view.path() for view in views])
