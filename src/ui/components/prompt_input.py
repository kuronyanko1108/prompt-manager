import flet as ft
from .theme import Color, IconSize


class PromptInput:
    @staticmethod
    def title_input_box(title_value: str | None):
        return ft.TextField(
            value=title_value,
            label="Title",
            hint_text="Title Please!!",
            # 最大文字数
            max_length=100,
            color=Color.INPUT_BOX_COLOR,
            border_color=Color.INPUT_BOX_COLOR,
            focused_border_color=Color.SELECT_COLOR,
            keyboard_type=ft.KeyboardType.TEXT,
        )

    @staticmethod
    def content_input_box(content_value: str | None):
        return ft.TextField(
            value=content_value,
            label="Content",
            hint_text="Content Please!!",
            max_length=10000,
            # 複数行
            multiline=True,
            # 最小行数
            min_lines=10,
            # 高さ
            height=300,
            # フォントサイズ
            text_size=16,
            # シフトキーとエンターキーの有効
            shift_enter=True,
            # 入力を選択していない時の色
            border_color=Color.INPUT_BOX_COLOR,
            # 入力欄を選択した時の色
            focused_border_color=Color.SELECT_COLOR,
        )
