import flet as ft


class PromptSnackBarUI:
    @staticmethod
    def show_snack_bar(current_page: ft.Page, message: str, duration_time=2000):
        # 1. SnackBarのインスタンスを作る
        snack_bar = ft.SnackBar(
            content=ft.Text(message),
            duration=duration_time,
        )
        # 2. 現在のページ(e.page)の属性にセットする
        current_page.snack_bar = snack_bar
        # 3. オープンフラグを立てる
        current_page.snack_bar.open = True
        # 4. ページを更新して反映させる
        current_page.update()
