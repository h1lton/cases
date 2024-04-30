import flet as ft
import httpx

from src.controls import ErrorAlertDialog
from src.logger import logger
from src.views import BaseViewContainer
from src.views.cases.constants import CASES
from src.views.cases.controls.detail import (
    SkinGrid,
    Wheel,
    WonSkinDialog,
)
from src.views.cases.controls.list import CaseGrid
from src.views.cases.schemas import WonSkinScheme


class CaseListView(BaseViewContainer):
    """Список кейсов, является root view"""

    route = "/"
    clear = True

    def build_view(self):
        self.content = CaseGrid()


class CaseDetailView(BaseViewContainer):
    """Дельное представление кейса, его содержимое и колесо прокрутки"""

    route = "cases/:id"
    back = True

    def build_view(self):
        case = CASES[self.params.get("id")]

        self.btn_open = ft.Ref[ft.TextButton]()
        self.won_skin: WonSkinScheme | None = None

        self.wheel = Wheel(case.drop, self.show_won_skin)
        self.content = ft.Column(
            [
                ft.Container(height=80),
                self.wheel,
                ft.Container(height=80),
                ft.Row(
                    [
                        ft.TextButton(
                            "OPEN CASE",
                            on_click=self.spin,
                            ref=self.btn_open,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                SkinGrid(case.drop),
            ],
            width=500,
        )

    async def spin(self, e):
        self.btn_back.current.visible = False
        self.btn_back.current.update()

        self.btn_open.current.disabled = True
        self.btn_open.current.update()

        try:
            self.won_skin = await self.wheel.spin()
        except httpx.HTTPError as e:
            logger.error("Проблемы с подключением к серверу: " + str(e))
            self.page.dialog = ErrorAlertDialog(e)
            self.page.update()
            await self.wheel_reset()

    async def wheel_reset(self, e=None):
        await self.wheel.reset()

        self.btn_back.current.visible = True
        self.btn_back.current.update()

        self.btn_open.current.disabled = False
        self.btn_open.current.update()

    def show_won_skin(self, e: ft.ControlEvent):
        if e.control.animate_position == 0:
            logger.info("Произошел сброс позиции колеса")
        else:
            logger.info("Колесо закончило вращение")
            if self.won_skin:
                self.page.dialog = WonSkinDialog(
                    self.won_skin, self.wheel_reset
                )
                self.page.update()
                self.won_skin = None
