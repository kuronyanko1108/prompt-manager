import flet as ft
from .theme import Color, FontSize, CharLimit


class PromptInput:
    @staticmethod
    def title_input_box(title_value: str | None):
        return ft.TextField(
            value=title_value or "",
            label="タイトル",
            hint_text="タイトルを記入してください",
            # 最大文字数
            max_length=CharLimit.TITLE_MAX_LENGTH,
            color=Color.INPUT_BOX_COLOR,
            border_color=Color.INPUT_BOX_COLOR,
            focused_border_color=Color.SELECT_COLOR,
            keyboard_type=ft.KeyboardType.TEXT,
            # 自動フォーカス
            autofocus=True,
        )

    @staticmethod
    def content_input_box(content_value: str | None):
        return ft.TextField(
            value=content_value or "",
            label="本文",
            hint_text="本文を入力してください",
            max_length=CharLimit.SUBTITLE_MAX_LENGTH,
            # 複数行
            multiline=True,
            # 最小行数
            min_lines=CharLimit.INPUT_CONTENT_MIN_LINE,
            # 高さ
            height=CharLimit.INPUT_CONTENT_HEIGHT,
            # フォントサイズ
            text_size=FontSize.INPUT_TEXT_FONT_SIZE,
            # シフトキーとエンターキーの有効
            shift_enter=True,
            # 入力を選択していない時の色
            border_color=Color.INPUT_BOX_COLOR,
            # 入力欄を選択した時の色
            focused_border_color=Color.SELECT_COLOR,
            expand=True,
        )
