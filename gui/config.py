from flet_core import MainAxisAlignment, ControlEvent, CrossAxisAlignment, TextStyle
import flet as ft

from gui.common import show_snack_bar, Page
from utils.config import config
import os

from update import is_have_update


def config_view(page: Page):
    def back_choose(_):
        page.go("/")
        page.update()

    def save(_):
        config.save()
        show_snack_bar(page, "保存成功", ft.colors.GREEN)
        page.go("/")
        page.update()

    def open_dlg(dlg):  # 显示弹窗
        page.dialog = dlg
        dlg.open = True
        page.update()

    def close_dlg(_):  # 关闭弹窗
        if page.dialog:
            page.dialog.open = False
            page.update()

    def update_handle(_):  # 运行更新程序
        os.system("../update.bat")

    def check_update(_):
        try:
            have_new, latest_version = is_have_update()
        except:
            show_snack_bar(page, "更新检查失败", ft.colors.RED)
            return
        if have_new:
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text('发现新版本'),
                content=ft.Text(f'最新版本为: {latest_version}'),
                actions=[
                    ft.TextButton('更新', on_click=update_handle),
                    ft.TextButton('取消', on_click=close_dlg)
                ]
            )
            open_dlg(dlg)
        else:
            show_snack_bar(page, "当前已是最新版本", ft.colors.GREEN)



    def show_map_checkbox_changed(_e):
        config.show_map_mode = (config.show_map_mode + 1) % 2

    def debug_checkbox_changed(_e):
        config.debug_mode = not config.debug_mode

    def speed_checkbox_changed(_e):
        config.speed_mode = not config.speed_mode

    def slow_checkbox_changed(_e):
        config.slow_mode = not config.slow_mode

    def update_checkbox_changed(_e):  # 是否自动检查更新
        config.check_update = not config.check_update

    def difficult_changed(e: ControlEvent):
        config.difficult = e.data

    def fate_changed(e: ControlEvent):
        config.fate = e.data

    def timezone_changed(e: ControlEvent):
        config.timezone = e.data

    def textbox_changed(e):
        config.order_text = e.control.value

    def get_info_mode(d):
        ls = [False, True, None]
        return ls[d]

    def go_del(e=None):
        try:
            if page.su._stop == 0:
                show_snack_bar(page, "请先退出自动化", ft.colors.RED)
                return
        except:
            pass
        nonlocal txt
        file_name = 'logs/notif.txt'
        cnt='0'
        if os.path.exists(file_name):
            with open(file_name, 'w', encoding="utf-8") as file:
                file.write(f"0\n已清空\n计数:0\n0")
            show_snack_bar(page, "清空成功", ft.colors.GREEN)
            txt.value = '本周已通关0次'
            page.update()

    def getnum():
        file_name = 'logs/notif.txt'
        cnt='0'
        if os.path.exists(file_name):
            try:
                with open(file_name, 'r', encoding="utf-8",errors='ignore') as file:
                    s=file.readlines()
                    cnt=s[0].strip('\n')
            except:
                pass
        return cnt

    txt = ft.Text('本周已通关'+getnum()+'次',weight=ft.FontWeight.W_600,size=20)
    page.views.append(
        ft.View(
            "/config",
            [
                ft.Stack(
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Text(
                                        value="设置",
                                        size=30,
                                    ),
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "返回",
                                                icon=ft.icons.ARROW_BACK,
                                                on_click=back_choose,
                                            ),
                                            ft.ElevatedButton(
                                                "保存",
                                                icon=ft.icons.DONE,
                                                on_click=save,
                                            ),
                                        ],
                                        alignment=MainAxisAlignment.CENTER,
                                        spacing=50,
                                    ),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            padding=10,
                        ),
                    ]
                ),
                ft.Divider(
                    height=1,
                ),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Column(
                                    [
                                        # ft.Checkbox(
                                        #     label="显示地图",
                                        #     value=get_info_mode(config.show_map_mode),
                                        #     on_change=show_map_checkbox_changed,
                                        # ),
                                        ft.Container(height=8),
                                        ft.Switch(
                                            label="调试模式",
                                            value=get_info_mode(config.debug_mode),
                                            on_change=debug_checkbox_changed,
                                            label_position='left',
                                            scale=1.2
                                        ),
                                        ft.Switch(
                                            label="速通模式",
                                            value=get_info_mode(config.speed_mode),
                                            on_change=speed_checkbox_changed,
                                            label_position='left',
                                            scale=1.2
                                        ),
                                        ft.Switch(
                                            label="慢速模式",
                                            value=get_info_mode(config.slow_mode),
                                            on_change=slow_checkbox_changed,
                                            label_position='left',
                                            scale=1.2
                                        ),
                                        ft.Switch(
                                            label="自动检查更新",
                                            value=get_info_mode(config.check_update),
                                            on_change=update_checkbox_changed,
                                            label_position='left',
                                            scale=1.2
                                        ),
                                        ft.ElevatedButton(
                                            content=ft.Row(
                                                [
                                                    ft.Icon(ft.icons.UPDATE),
                                                    ft.Text('检查更新', weight=ft.FontWeight.W_600),
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                            ),
                                            on_click=check_update,
                                            width=120
                                        )
                                    ]
                                ),
                                ft.Container(height=20),
                                ft.Row(
                                    [
                                        ft.Dropdown(
                                            width=100,
                                            label="难度",
                                            hint_text="选择世界难度",
                                            options=[
                                                ft.dropdown.Option("1"),
                                                ft.dropdown.Option("2"),
                                                ft.dropdown.Option("3"),
                                                ft.dropdown.Option("4"),
                                                ft.dropdown.Option("5"),
                                            ],
                                            text_style=TextStyle(color=ft.colors.PINK,weight=ft.FontWeight.W_600),
                                            value=config.difficult,
                                            on_change=difficult_changed,
                                        ),
                                        ft.Dropdown(
                                            width=100,
                                            label="命途",
                                            hint_text="选择命途",
                                            options=[
                                                ft.dropdown.Option("存护"),
                                                ft.dropdown.Option("记忆"),
                                                ft.dropdown.Option("虚无"),
                                                ft.dropdown.Option("丰饶"),
                                                ft.dropdown.Option("巡猎"),
                                                ft.dropdown.Option("毁灭"),
                                                ft.dropdown.Option("欢愉"),
                                                ft.dropdown.Option("繁育"),
                                            ],
                                            text_style=TextStyle(color=ft.colors.PINK,weight=ft.FontWeight.W_600),
                                            value=config.fate,
                                            on_change=fate_changed,
                                        ),
                                        ft.Dropdown(
                                            width=150,
                                            label="时区",
                                            hint_text="影响计数刷新时间",
                                            options=[
                                                ft.dropdown.Option("Default"),
                                                ft.dropdown.Option("Asia"),
                                                ft.dropdown.Option("America"),
                                                ft.dropdown.Option("Europe"),
                                            ],
                                            text_style=TextStyle(color=ft.colors.PINK,weight=ft.FontWeight.W_600),
                                            value=config.timezone,
                                            on_change=timezone_changed,
                                        ),
                                    ]
                                ),
                                ft.Container(height=20),
                                ft.Row(
                                    [
                                        txt,
                                        ft.IconButton(
                                            icon=ft.icons.DELETE,
                                            tooltip="清空通关计数",
                                            icon_size=35,
                                            on_click=go_del,
                                        ),
                                    ]
                                )
                            ],
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
            ],
            padding=20,
            spacing=0,
        )
    )
