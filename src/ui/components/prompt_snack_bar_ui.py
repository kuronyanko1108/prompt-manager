import flet as ft
from .theme import Color, Timing


class PromptSnackBarUi:
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
    def show_success_snack_bar(
        current_page: ft.Page,
        message: str,
        duration_time: int = Timing.SNACKBAR_DURATION,
    ) -> None:
        """成功操作時のスナックバーを構築し表示する。

        Args:
            current_page (ft.Page): current_page (ft.Page): スナックバーを表示する対象のページ。
            message (str): スナックバーに表示するテキストメッセージ。
            duration_time (int, optional):表示時間（ミリ秒単位）。デフォルトは2000ms
        Returns:
            None: 内部で表示処理を実行し、戻り値はありません。
        """
        return PromptSnackBarUi._show_snack_bar(
            current_page,
            message,
            duration_time,
            Color.BASE_FONT_COLOR,
            Color.NORMAL_OPERATION_COLOR,
        )

    @staticmethod
    def show_error_snack_bar(
        current_page: ft.Page,
        message: str,
        duration_time: int = Timing.SNACKBAR_DURATION,
    ) -> None:
        """失敗操作時のスナックバーを構築し表示する。

        Args:
            current_page (ft.Page): current_page (ft.Page): スナックバーを表示する対象のページ。
            message (str): スナックバーに表示するテキストメッセージ。
            duration_time (int, optional):表示時間（ミリ秒単位）。デフォルトは2000ms
        Returns:
            None: 内部で表示処理を実行し、戻り値はありません。
        """
        return PromptSnackBarUi._show_snack_bar(
            current_page,
            message,
            duration_time,
            Color.BASE_FONT_COLOR,
            Color.DANGER_OPERATION_COLOR,
        )
