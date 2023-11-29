
import atexit

import flet as ft
import pyuac
import win32gui

from gui.choose import choose_view
from gui.config import config_view
from gui.abyss import abyss_view
from gui.common import cleanup, mynd, Page, init_page, check_update
from utils.config import config


def main(page: Page):
    def on_route_change(e: Page):
        page.views.clear()
        choose_view(page)
        if e.route == "/config":
            config_view(page)
        if e.route == '/abyss':
            abyss_view(page)
        page.update()

    def view_pop():
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    init_page(page)
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.PINK,
    )
    page.title = "AutoSimulatedUniverse"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.on_route_change = on_route_change
    page.on_view_pop = view_pop
    page.window_min_width = 800
    page.window_width = 800
    page.window_height = 670
    page.window_min_height = 650
    page.go(page.route)

    # check update
    if config.check_update:
        check_update(page)


if __name__ == "__main__":
    atexit.register(cleanup)
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:
        try:
            win32gui.ShowWindow(mynd, 0)
        except:
            pass
        ft.app(target=main, port=28675)
