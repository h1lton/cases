import flet as ft

from src import constants
from src.logger import logger


class WindowTitleBar(ft.Row):
    """Верхняя часть приложения"""

    btn_maximize = ft.Ref[ft.IconButton]()

    def __init__(
        self,
        page: ft.Page,
        maximizable: bool = True,
        back: bool = False,
        ref_back: ft.Ref[ft.IconButton] | None = None,
    ):

        self.page = page
        self.page.on_window_event = self.on_window_event
        self.maximizable = maximizable
        super().__init__(
            spacing=0,
            height=35,
            controls=[
                ft.IconButton(
                    ft.icons.ARROW_BACK_IOS,
                    on_click=lambda e: e.page.go(
                        "/"
                    ),  # FIXME: работает не корректно
                    icon_size=17.6,
                    style=self.btn_style(),
                    width=45,
                    visible=back,
                    ref=ref_back,
                ),
                ft.WindowDragArea(content=ft.Container(), expand=True),
                ft.IconButton(
                    ft.icons.HORIZONTAL_RULE_OUTLINED,
                    on_click=self.minimize,
                    icon_size=15.2,
                    style=self.btn_style(),
                    width=45,
                ),
                ft.IconButton(
                    ft.icons.CHECK_BOX_OUTLINE_BLANK_OUTLINED,
                    on_click=self.maximize,
                    icon_size=13.6,
                    style=self.btn_style(),
                    ref=self.btn_maximize,
                    width=45,
                    visible=self.maximizable,
                ),
                ft.IconButton(
                    ft.icons.CLOSE_OUTLINED,
                    on_click=self.finalize,
                    icon_size=17.6,
                    style=self.btn_style(True),
                    width=45,
                ),
            ],
        )

    def maximize(self, e):
        logger.info("maximize")
        self.page.window_maximized = not e.page.window_maximized
        self.page.update()

    def minimize(self, e):
        logger.info("minimize")
        self.page.window_minimized = True
        self.page.update()

    def finalize(self, e):
        logger.info("finalize")
        self.page.window_close()

    @staticmethod
    def btn_style(is_close_btn: bool = False):
        return ft.ButtonStyle(
            color={
                ft.MaterialState.DEFAULT: ft.colors.with_opacity(
                    0.3, ft.colors.ON_BACKGROUND
                ),
                ft.MaterialState.HOVERED: ft.colors.ON_BACKGROUND,
            },
            padding=0,
            shape=ft.RoundedRectangleBorder(radius=0),
            overlay_color=ft.colors.RED if is_close_btn else None,
        )

    def on_window_event(self, e):
        if e.data == "close":
            e.page.window_close()
        elif e.data == "unmaximize" or e.data == "maximize":
            if e.page.window_maximized:
                self.btn_maximize.current.icon = ft.icons.FILTER_NONE
                self.btn_maximize.current.icon_size = 12
                for view in e.page.views:
                    view.controls[0].margin = 0
            else:
                self.btn_maximize.current.icon = (
                    ft.icons.CHECK_BOX_OUTLINE_BLANK_ROUNDED
                )
                self.btn_maximize.current.icon_size = 13.6
                for view in e.page.views:
                    view.margin = constants.SHADOW_SIZE
            e.page.update()


class ErrorAlertDialog(ft.AlertDialog):
    def __init__(self, error: Exception):
        super().__init__(
            open=True,
            bgcolor=ft.colors.ERROR_CONTAINER,
            title=ft.Text(
                str(error.__class__.__name__),
                color=ft.colors.ON_ERROR_CONTAINER,
            ),
            content=ft.Text(str(error), color=ft.colors.ON_ERROR_CONTAINER),
        )
