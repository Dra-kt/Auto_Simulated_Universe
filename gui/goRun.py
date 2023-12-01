import time

import flet as ft
import win32gui
from flet_core import ControlEvent, TextStyle, MainAxisAlignment, CrossAxisAlignment
from utils.config import config
from gui.common import Page, open_dlg, close_dlg, get_info_mode, show_snack_bar, run
from states import SimulatedUniverse
from utils.utils import notif

shutdown = False  # 自动关机
nums = '10000'  # 次数，显示在输入框中


def startConfig(page: Page):
    # 检查nums合法性
    def _check_nums():
        global nums
        try:
            nums = int(nums)
        except ValueError:
            nums = '10000'  # 恢复数值
            return False
        if nums > 0:
            return True
        return False

    def go_dep(e=None):
        dlg1 = ft.AlertDialog(
            title=ft.Text("异常退出"),
            content=ft.Text(" "),  # "请确认python+numpy已安装并正确配置环境变量")
        )
        open_dlg(page, dlg1)

    def startRun():
        show_snack_bar(page, "开始运行，请切换回游戏（＾∀＾●）", ft.colors.GREEN)
        tm = time.time()
        run(page.su.start)
        txt = " "
        if time.time() - tm < 20:
            go_dep()
            # txt = "请确认python+numpy已安装并正确配置环境变量"
        try:
            win32gui.SetForegroundWindow(page.su.my_nd)
        except:
            pass
        if page.su is not None:
            run(page.su.stop)
        notif("已退出自动化", txt)

    def setConfig(_):
        close_dlg(page)  # 关闭配置窗口
        if not _check_nums():
            show_snack_bar(page, '您输入的次数不合法', ft.colors.RED)
            return
        page.su = SimulatedUniverse(
            1,
            config.debug_mode,
            config.show_map_mode,
            config.speed_mode,
            config.use_consumable,
            config.slow_mode,
            unlock=True,
            bonus=config.bonus,
            gui=1,
            shutdown=shutdown,
            nums=nums
        )
        startRun()

    # 配置文件变更
    def bonus_checkbox_changed(_e):
        config.bonus = not config.bonus

    # 速通模式
    def speed_checkbox_changed(_e):
        config.speed_mode = not config.speed_mode

    # 自动关机
    def shutdown_checkbox_changed(_e):
        global shutdown
        shutdown = not shutdown

    # 次数
    def nums_changed(e: ControlEvent):
        global nums
        nums = e.data

    # 启动运行前弹出窗口，显示配置选项
    global shutdown, nums
    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("开始运行"),
        actions=[
            ft.TextButton("开始", on_click=setConfig),
            ft.TextButton("取消", on_click=lambda _: close_dlg(page))
        ],
        content=ft.Column(
            [
                ft.Switch(
                    label='沉浸奖励',
                    value=get_info_mode(config.bonus),
                    on_change=bonus_checkbox_changed,
                    scale=1.0,
                    label_position=ft.LabelPosition.LEFT
                ),
                ft.Switch(
                    label='速通模式',
                    value=get_info_mode(config.speed_mode),
                    on_change=speed_checkbox_changed,
                    scale=1.0,
                    label_position=ft.LabelPosition.LEFT
                ),
                ft.Checkbox(
                    label='完成后自动关机',
                    value=shutdown,
                    on_change=shutdown_checkbox_changed,
                    scale=1.0,
                    label_position=ft.LabelPosition.LEFT
                ),
                ft.TextField(
                    label='次数',
                    value=str(nums),
                    on_change=nums_changed,
                    text_style=TextStyle(color=ft.colors.PINK, weight=ft.FontWeight.W_600)
                )
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            tight=True
        )
    )
    open_dlg(page, dlg)
