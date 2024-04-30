import flet as ft

from src.views.cases import constants


class CaseGrid(ft.GridView):
    def __init__(self):
        super().__init__(
            runs_count=5,
            width=500,
            spacing=5,
            run_spacing=15,
        )
        for case in constants.CASES.values():
            self.controls.append(
                ft.Container(
                    content=ft.Image(case.image),
                    on_click=lambda e: e.page.go(f"cases/{e.control.data}"),
                    data=case.id,
                )
            )
