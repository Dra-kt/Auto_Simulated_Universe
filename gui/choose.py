import flet as ft
from flet_core import MainAxisAlignment, CrossAxisAlignment

from align_angle import main as align_angle
from gui.common import show_snack_bar, mynd, Page, open_dlg, close_dlg, run
from states import version
from utils.config import config

from gui.goRun import startConfig


def choose_view(page: Page):
    def angle(_e):
        show_snack_bar(page, "开始校准，请切换回游戏（¬､¬）", ft.colors.GREEN)
        res = run(align_angle)
        if res == 1:
            show_snack_bar(page, "校准成功（＾∀＾●）", ft.colors.GREEN)
            page.first = 0  # 不再弹出校准提示
        else:
            show_snack_bar(page, "校准失败（⊙.⊙）", ft.colors.RED)

    def start(_e):
        # 若首次运行且为设置校准值，提示需要校准
        if config.angle == '1.0' and page.first == 1:
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text('需要校准'),
                content=ft.Text('在首次运行前，推荐先进行校准操作'),
                actions=[
                    ft.TextButton('确认', on_click=lambda x: close_dlg(page))
                ]
            )
            open_dlg(page, dlg)
            page.first = 0
            return
        startConfig(page)

    def start_abyss(_e):
        page.go("/abyss")

    def stops(_e):
        show_snack_bar(page, "停止运行（>∀<）", ft.colors.GREEN)
        try:
            page.su._stop = 1
        except:
            pass
        if page.su is not None:
            run(page.su.stop)

    def go_config(_e):
        page.go("/config")

    def go_about(e=None):
        dlg = ft.AlertDialog(
            title=ft.Text("二次开发说明"),
            content=ft.Text(
                "项目原作：https://github.com/CHNZYX/Auto_Simulated_Universe"
            ),
        )
        open_dlg(page, dlg)

    # View
    page.views.append(
        ft.View(
            "/",
            [
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(
                                "AutoSimulatedUniverse",
                                size=50,
                            ),
                        ),
                        ft.Container(
                            content=ft.Text(
                                version + ' by Dra-kt (Origin from CHNZYX)',
                                size=20,
                            ),
                        ),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.ADD_TASK),
                                    ft.Text("校准", weight=ft.FontWeight.W_600),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            on_click=angle,
                            width=120,
                        ),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.LOGIN),
                                    ft.Text("运行", weight=ft.FontWeight.W_600),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            on_click=start,
                            width=120,
                        ),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.GAMEPAD),
                                    ft.Text("深渊", weight=ft.FontWeight.W_600),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            on_click=start_abyss,
                            width=120,
                        ),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.STOP),
                                    ft.Text("停止", weight=ft.FontWeight.W_600),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            on_click=stops,
                            width=120,
                        ),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.SETTINGS),
                                    ft.Text("设置", weight=ft.FontWeight.W_700),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            on_click=go_config,
                            width=120,
                        ),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.INFO),
                                    ft.Text("关于", weight=ft.FontWeight.W_600),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            on_click=go_about,
                            width=120,
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
        )
    )
