import random
from asyncio import sleep
from pathlib import Path

import flet as ft

from src.backend import client
from src.utils import blend_colors, extime, assets

from src.logger import logger
from src.views.cases.constants import (
    CASE_CUM_WEIGHTS,
    ITEM_CONF,
    RARITY_COLOR,
    SKIN_GRID_CONF,
    SKINS,
    WHEEL_ITEM_CONF,
    GOLD_GROUPS,
    WHEEL_ANIMATION_TIME,
)
from src.views.cases.schemas import CaseDropScheme, WonSkinScheme


@extime("Время выполнения запроса выигранного скина")
async def get_won_skin(
    case_route: str,
) -> WonSkinScheme:
    res = await client.get(f"{case_route}/open", timeout=4)
    return WonSkinScheme.model_validate(res.json())


class Item(ft.Stack):
    def __init__(
        self,
        image: str | Path,
        rarity_color: RARITY_COLOR,
    ):
        super().__init__(
            width=ITEM_CONF.WIDTH,
            height=ITEM_CONF.HEIGHT + ITEM_CONF.HEIGHT_DESC,
            controls=[
                ft.Container(
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=[
                            "#505050",
                            "#b0b0b0",
                        ],
                    ),
                    opacity=0.75,
                    width=ITEM_CONF.WIDTH,
                    height=ITEM_CONF.HEIGHT,
                    top=0,
                ),
                ft.Container(
                    bgcolor=rarity_color.value,
                    height=3,
                    bottom=ITEM_CONF.HEIGHT_DESC,
                    left=0,
                    right=0,
                ),
                ft.Image(
                    image,
                    width=ITEM_CONF.WIDTH,
                    height=ITEM_CONF.HEIGHT,
                    top=0,
                ),
                ft.Container(
                    height=ITEM_CONF.HEIGHT_DESC,
                    bottom=0,
                    right=0,
                    left=0,
                    padding=ft.padding.only(top=6),
                    content=ft.Column(
                        [
                            ft.Container(
                                expand=1,
                                width=30,
                                bgcolor="white,0.25",
                                border_radius=25,
                            ),
                            ft.Container(
                                expand=1,
                                width=52,
                                bgcolor="white,0.15",
                                border_radius=25,
                            ),
                        ],
                        expand=1,
                        spacing=6,
                    ),
                ),
            ],
        )


class GoldItem(ft.Stack):
    def __init__(self, image: str | Path):
        super().__init__(
            width=ITEM_CONF.WIDTH,
            height=ITEM_CONF.HEIGHT + ITEM_CONF.HEIGHT_DESC,
            controls=[
                ft.Image(
                    "gold_bg.gif",
                    width=ITEM_CONF.WIDTH,
                    height=ITEM_CONF.HEIGHT,
                    top=0,
                    color=RARITY_COLOR.GOLD.value,
                    color_blend_mode=ft.BlendMode.OVERLAY,
                ),
                ft.Container(
                    bgcolor=RARITY_COLOR.GOLD.value,
                    height=3,
                    bottom=ITEM_CONF.HEIGHT_DESC,
                    left=0,
                    right=0,
                ),
                ft.Image(
                    image,
                    width=ITEM_CONF.WIDTH,
                    height=ITEM_CONF.HEIGHT,
                    top=0,
                ),
                ft.Container(
                    height=ITEM_CONF.HEIGHT_DESC,
                    bottom=0,
                    right=0,
                    left=0,
                    padding=ft.padding.only(top=6),
                    content=ft.Column(
                        [
                            ft.Container(
                                expand=1,
                                width=30,
                                bgcolor="white,0.25",
                                border_radius=25,
                            ),
                            ft.Container(
                                expand=1,
                                width=52,
                                bgcolor="white,0.15",
                                border_radius=25,
                            ),
                        ],
                        expand=1,
                        spacing=6,
                    ),
                ),
            ],
        )


class SkinGrid(ft.Row):
    def __init__(self, drop: CaseDropScheme):
        super().__init__(
            wrap=True,
            run_spacing=SKIN_GRID_CONF.SPACING,
            spacing=SKIN_GRID_CONF.SPACING,
            width=SKIN_GRID_CONF.WIDTH,
        )

        for skins_by_rarity, rarity_color in [
            [drop.rare, RARITY_COLOR.RARE],
            [drop.mythical, RARITY_COLOR.MYTHICAL],
            [drop.legendary, RARITY_COLOR.LEGENDARY],
            [drop.ancient, RARITY_COLOR.ANCIENT],
        ]:
            for skin in skins_by_rarity:
                self.controls.append(
                    Item(
                        SKINS[skin].image,
                        rarity_color,
                    )
                )

        # FIXME: должен быть золотой фон
        self.controls.append(
            GoldItem(
                GOLD_GROUPS[drop.gold_group].image,
            )
        )


class WheelItem(ft.Stack):
    def __init__(
        self,
        image: str,
        rarity_color: RARITY_COLOR,
    ):
        super().__init__(
            width=WHEEL_ITEM_CONF.WIDTH,
            height=WHEEL_ITEM_CONF.HEIGHT,
            controls=[
                ft.Container(
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=[
                            "#b0b0b0",
                            blend_colors("#505050", rarity_color.value),
                        ],
                        stops=[0.60, 0.95],
                    ),
                    opacity=0.75,
                    width=WHEEL_ITEM_CONF.WIDTH,
                    height=WHEEL_ITEM_CONF.HEIGHT,
                    top=0,
                ),
                ft.Container(
                    bgcolor=rarity_color.value,
                    height=5,
                    bottom=0,
                    left=0,
                    right=0,
                ),
                ft.Image(
                    image,
                    width=WHEEL_ITEM_CONF.WIDTH,
                    height=WHEEL_ITEM_CONF.HEIGHT,
                    top=0,
                ),
            ],
        )


class WheelRow(ft.Row):
    def __init__(
        self, drop: CaseDropScheme, parent_width: int, on_animation_end
    ):
        super().__init__(
            on_animation_end=on_animation_end,
            top=0,
            bottom=0,
            animate_position=ft.Animation(
                WHEEL_ANIMATION_TIME,
                ft.AnimationCurve.EASE_OUT_SINE,
            ),
        )
        self.skin_width = WHEEL_ITEM_CONF.WIDTH
        self.spacing = 10

        # общее кол-во скинов в колесе
        self.skins = 37

        # индекс выигранного скина, должен быть меньше общего кол-ва скинов
        self.win_skin_index = 33

        self.parent_width = parent_width
        self.drop = drop

        self.skin_with_space = self.skin_width + self.spacing

        self.width = self.skin_with_space * self.skins - self.spacing

        self.win_skin_start = self.skin_with_space * self.win_skin_index

    def fill(self):
        """Наполняет колесо скинами."""
        controls = []
        for i in range(self.skins):
            if i == self.win_skin_index:
                controls.append(
                    WheelItem(
                        "econ/logo.png",
                        RARITY_COLOR.GOLD,
                    )
                )
            else:
                skin_id = self.random_skin()

                if skin_id == "gold":
                    controls.append(
                        WheelItem(
                            GOLD_GROUPS[self.drop.gold_group].image,
                            RARITY_COLOR.GOLD,
                        )
                    )
                else:
                    skin_id = SKINS[skin_id]
                    controls.append(
                        WheelItem(
                            skin_id.image,
                            RARITY_COLOR[skin_id.rarity[7:-7].upper()],
                            # FIXME: нужно отредактировать skin_id.rarity
                        )
                    )

        self.controls = controls

    def random_skin(self) -> str:
        """Вернет рандомный id скина из кейса"""
        skins_by_rarity: str | list[str] = random.choices(
            [
                "gold",
                self.drop.ancient,
                self.drop.legendary,
                self.drop.mythical,
                self.drop.rare,
            ],
            cum_weights=CASE_CUM_WEIGHTS,
        )[0]

        if skins_by_rarity == "gold":
            return skins_by_rarity

        return random.choice(skins_by_rarity)

    async def set_won_skin(self):
        res = await get_won_skin(self.page.route)

        logger.info(
            f"Выигранный скин: id={res.skin_id}, is_gold={res.is_gold}"
        )

        if res.is_gold:
            self.controls[self.win_skin_index] = WheelItem(
                GOLD_GROUPS[self.drop.gold_group].image,
                RARITY_COLOR.GOLD,
            )

        else:
            skin = SKINS[res.skin_id]
            self.controls[self.win_skin_index] = WheelItem(
                skin.image,
                RARITY_COLOR[skin.rarity[7:-7].upper()],
                # FIXME: нужно отредактировать skin.rarity
            )

        self.update()

        return res

    def random_position(self):
        """
        Возвращает позицию выигранного скина
        с рандомной остановкой по его ширине.
        """
        return self.win_skin_start + random.randrange(self.skin_width)

    async def animate(self):
        """Наполнение и запуск анимации вращения колеса."""
        self.left = 0
        # self.animate_position = 0
        self.fill()
        self.update()

        await sleep(0.05)

        self.left = -self.random_position() + self.parent_width / 2
        self.animate_position = ft.Animation(
            WHEEL_ANIMATION_TIME,
            ft.AnimationCurve.EASE_OUT_SINE,
        )


class Wheel(ft.Stack):
    """
    Колесо — это верхняя часть детального view кейса.
    Крутиться с рандомно наполненными скинами.
    """

    def __init__(self, drop: CaseDropScheme, on_animation_end):
        super().__init__(
            height=WHEEL_ITEM_CONF.HEIGHT,
            width=500,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            opacity=0,
            animate_opacity=150,
        )
        self.wheel_row = WheelRow(drop, self.width, on_animation_end)
        self.controls = [
            self.wheel_row,
            ft.Container(
                # Тени
                # FIXME: сделано убого,
                #  надо найти более правильный способ
                gradient=ft.LinearGradient(
                    colors=[
                        ft.colors.BACKGROUND,
                        ft.colors.TRANSPARENT,
                        ft.colors.TRANSPARENT,
                        ft.colors.BACKGROUND,
                    ],
                    stops=[0, 0.2, 0.8, 1],
                ),
                expand=1,
            ),
            ft.Container(  # Жёлтая чёрточка посередине
                ft.Container(
                    ft.VerticalDivider(
                        color=ft.colors.YELLOW,
                        thickness=2,
                    ),
                    width=2,
                    alignment=ft.alignment.center,
                    height=self.wheel_row.skin_width / 4 * 3,
                ),
                expand=1,
                alignment=ft.alignment.center,
            ),
        ]

    async def spin(self) -> WonSkinScheme:
        self.opacity = 1

        await self.wheel_row.animate()
        self.update()
        logger.info("Колесо начало вращение")

        won_skin = await self.wheel_row.set_won_skin()
        return won_skin

    async def reset(self):
        logger.info("Сброс колеса")

        self.opacity = 0
        self.update()

        await sleep(0.15)

        self.wheel_row.left = 0
        self.wheel_row.animate_position = 0
        self.update()


class WonSkinDialog(ft.AlertDialog):
    def __init__(self, skin: WonSkinScheme, on_dismiss):
        skin = SKINS[skin.skin_id]
        super().__init__(
            title=ft.Text("You won"),
            content=ft.Column(
                [
                    ft.Container(
                        height=5,
                        bgcolor=RARITY_COLOR[skin.rarity[7:-7].upper()].value,
                        border_radius=5,
                    ),
                    ft.Image(skin.image, expand=1),
                ],
                height=170,
                width=130,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            actions=[
                ft.TextButton(
                    "SELL",
                    on_click=self.close,
                ),
                ft.TextButton("CONTINUE", on_click=self.close),
            ],
            open=True,
            on_dismiss=on_dismiss,
        )

    def close(self, e):
        self.open = False
        self.update()
