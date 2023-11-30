import traceback

import flet as ft
import win32gui
from flet_core import MainAxisAlignment, CrossAxisAlignment

from align_angle import main as align_angle
from gui.common import show_snack_bar, mynd, Page, open_dlg, close_dlg
from states import SimulatedUniverse, version
from utils.config import config
from utils.utils import notif
import time


def choose_view(page: Page):
    def change_all_button(value: bool = True):
        cnt = 0
        for i in page.views[0].controls[0].controls:
            if isinstance(i, ft.FilledButton):
                if cnt <= 1:
                    i.disabled = value
                    cnt += 1
                else:
                    i.disabled = False
        page.update()

    def run(func, *args, **kwargs):
        try:
            change_all_button()
            res = func(*args, **kwargs)
            change_all_button(False)
            return res
        except ValueError as e:
            pass
        except Exception:
            print("E: 运行函数时出现错误")
            traceback.print_exc()
        finally:
            change_all_button(False)

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
        show_snack_bar(page, "开始运行，请切换回游戏（＾∀＾●）", ft.colors.GREEN)
        tm = time.time()
        page.su = run(
            SimulatedUniverse,
            1,
            int(config.debug_mode),
            int(config.show_map_mode),
            int(config.speed_mode),
            int(config.use_consumable),
            int(config.slow_mode),
            unlock=True,
            bonus=config.bonus,
            gui=1,
        )
        run(page.su.start)
        txt = " "
        if time.time() - tm < 20:
            go_dep()
            # txt = "请确认python+numpy已安装并正确配置环境变量"
        try:
            if page.su.validate == 0:
                txt = "版本过低，请更新"
        except:
            pass
        try:
            win32gui.SetForegroundWindow(page.su.my_nd)
        except:
            pass
        if page.su is not None:
            run(page.su.stop)
        notif("已退出自动化", txt)

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

    def hide(_e):
        try:
            if win32gui.IsWindowVisible(mynd):
                show_snack_bar(page, "隐藏命令行窗口", ft.colors.GREEN)
                win32gui.ShowWindow(mynd, 0)  # 隐藏命令行窗口
            else:
                show_snack_bar(page, "显示命令行窗口", ft.colors.GREEN)
                win32gui.ShowWindow(mynd, 1)  # 显示命令行窗口
        except:
            pass


    def go_config(_e):
        page.go("/config")

    def go_about(e=None):
        dlg = ft.AlertDialog(
            title=ft.Text("二次开发说明"),
            content=ft.Text(
                "项目原作：https://github.com/CHNZYX/Auto_Simulated_Universe"
            ),
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def go_money(e=None):
        go_about()

    def go_dep(e=None):
        dlg = ft.AlertDialog(
            title=ft.Text("异常退出"),
            content=ft.Text(" "),  # "请确认python+numpy已安装并正确配置环境变量")
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def bonus_changed(e):
        config.bonus = not config.bonus

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
                                    ft.Icon(ft.icons.HIDE_SOURCE),
                                    ft.Text("显隐", weight=ft.FontWeight.W_800),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            on_click=hide,
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
                ft.Row(
                    [
                        ft.Container(width=315),
                        ft.Switch(
                            label="沉浸奖励", on_change=bonus_changed, value=config.bonus, label_position='left',
                            scale=1.2
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.Container(),
                        ft.IconButton(
                            icon=ft.icons.THUMB_UP,
                            tooltip="赞赏",
                            icon_size=35,
                            on_click=go_money,
                        ),
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.END,
                ),
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
        )
    )
