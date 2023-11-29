from typing import Optional
import os

import flet as ft
import win32gui

from states import SimulatedUniverse
from abyss import Abyss
from update import is_have_update


class Page(ft.Page):
    su: Optional[SimulatedUniverse]
    ab: Optional[Abyss]
    first: int
    bonus: bool


def open_dlg(page: Page, dlg):
    page.dialog = dlg
    dlg.open = True
    page.update()


def close_dlg(page):
    if page.dialog:
        page.dialog.open = False
        page.update()


def update_handle(_):  # 运行更新程序
    os.system("../update.bat")
    exit(0)


def check_update(page: Page):
    have_new, latest_version = False, '0.0'
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
                ft.TextButton('取消', on_click=lambda _: close_dlg(page))
            ]
        )
        open_dlg(page, dlg)
    else:
        show_snack_bar(page, "当前已是最新版本", ft.colors.GREEN)


def init_page(page: Page):
    page.su = None
    page.ab = None
    page.first = 1


def show_snack_bar(page, text, color, selectable=False):
    return page.show_snack_bar(
        ft.SnackBar(
            open=True,
            content=ft.Text(text, selectable=selectable),
            bgcolor=color,
        )
    )


def cleanup():
    try:
        win32gui.ShowWindow(mynd, 1)
    except:
        pass


def enum_windows_callback(hwnd, hwnds):
    class_name = win32gui.GetClassName(hwnd)
    name = win32gui.GetWindowText(hwnd)
    try:
        if (
                class_name == "ConsoleWindowClass"
                and win32gui.IsWindowVisible(hwnd)
                and "gui" in name[-7:]
        ):
            hwnds.append(hwnd)
    except:
        pass
    return True


def list_handles():
    hwnds = []
    win32gui.EnumWindows(enum_windows_callback, hwnds)
    hwnds.append(0)
    return hwnds


mynd = list_handles()[0]
