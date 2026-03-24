import flet as ft
from .theme import Color


class PromptInput:
    @staticmethod
    def title_input_box(title_value: str | None):
        return ft.TextField(
            value=title_value or "",
            label="タイトル",
            hint_text="タイトルを記入してください",
            # 最大文字数
            max_length=100,
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
            max_length=10000,
            # 複数行
            multiline=True,
            # 最小行数
            min_lines=15,
            # 高さ
            height=400,
            # フォントサイズ
            text_size=16,
            # シフトキーとエンターキーの有効
            shift_enter=True,
            # 入力を選択していない時の色
            border_color=Color.INPUT_BOX_COLOR,
            # 入力欄を選択した時の色
            focused_border_color=Color.SELECT_COLOR,
            expand=True,
        )
