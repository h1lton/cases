import flet as ft
from flet_route import Basket, Params

from src.controls import WindowTitleBar
from src.logger import logger


class BaseViewContainer(ft.Container):
    """Базовый класс для views, их нужно передавать в роутер"""

    route: str  # путь к этому view
    clear: bool = False  # очищать ли историю
    back: bool = False  # добавлять ли кнопку назад

    def __init__(self, page: ft.Page, params: Params, basket: Basket):
        logger.info(f"Building view {self.__class__.__name__}")

        super().__init__(expand=1, alignment=ft.alignment.center)

        self.page = page
        self.params = params
        self.basket = basket

        self.btn_back = ft.Ref[ft.IconButton]()

        self.build_view()

    def build_view(self):
        """
        Тут нужно строить view.
        Вызывается после инита.
        """
        raise NotImplementedError

    @classmethod
    def path(cls):
        """Этот метод нужен для построения роутера"""
        return [cls.route, cls.clear, cls.view, None]

    @classmethod
    def view(cls, page: ft.Page, params: Params, basket: Basket) -> ft.View:
        """
        Базовая оболочка, в которую помещается view,
        и возвращается готовая страница.
        """
        self = cls(page, params, basket)

        return ft.View(
            cls.route,
            [
                WindowTitleBar(page, back=self.back, ref_back=self.btn_back),
                self,
            ],
            padding=0,
            spacing=0,
        )
