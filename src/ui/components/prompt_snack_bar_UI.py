import flet as ft
from .theme import Color


class PromptSnackBarUI:
    @staticmethod
    def _show_snack_bar(
        current_page: ft.Page,
        message: str,
        duration_time,
        font_color,
        back_ground_color,
    ):
        # 1. SnackBarのインスタンスを作る
        snack_bar = ft.SnackBar(
            content=ft.Text(message, color=font_color),
            duration=duration_time,
            bgcolor=back_ground_color,
        )
        # 2. スナックバーを表示する
        current_page.show_dialog(snack_bar)
        # 3. ページを更新して反映させる
        current_page.update()

    @staticmethod
    def success_snack_bar(current_page: ft.Page, message: str, duration_time=2000):
        print()
        return PromptSnackBarUI._show_snack_bar(
            current_page,
            message,
            duration_time,
            Color.BASE_FONT_COLOR,
            Color.NORMAL_OPERATION_COLOR,
        )

    @staticmethod
    def error_snack_bar(current_page: ft.Page, message: str, duration_time=2000):
        return PromptSnackBarUI._show_snack_bar(
            current_page,
            message,
            duration_time,
            Color.BASE_FONT_COLOR,
            Color.DANGER_OPERATION_COLOR,
        )
