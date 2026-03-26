import flet as ft
from ..components.theme import Color, LayoutSize, CharLimit


class UiUtils:
    @staticmethod
    def transform_text(
        text: str, max_length: int = CharLimit.SUBTITLE_MAX_LENGTH
    ) -> str:
        """文字列から改行等を除去し、指定した文字数で切り捨てて返却する

        Args:
            text (str): 処理対象の文字列
            max_length (int, optional): 最大文字数。デフォルト値は50文字

        Returns:
            str: 正規化および、長さ調整後の文字列
        """
        #  改行/タブ/連続空白を1スペースに正規化
        normalized = " ".join((text or "").split())

        if len(normalized) <= max_length:
            return normalized
        # 最大文字数を超える場合は末尾に…を追加する
        return normalized[: max_length - 1] + "…"

    @staticmethod
    def set_highlight(
        color: str = Color.PROMPT_LIST_FRAME_COLOR,
    ) -> ft.Border:
        """
        コンテナのハイライト表示を行います
        Args:
            color (str): ハイライト表示させる色
        Return:
            ft.Border:ハイライト表示色を付与した枠線情報
        """
        return ft.Border.only(bottom=ft.BorderSide(LayoutSize.FRAME_THICKNESS, color))
