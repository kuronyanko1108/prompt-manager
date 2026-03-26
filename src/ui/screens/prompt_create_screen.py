import flet as ft
from ..view.create_view import PromptCreateView
from ..components.prompt_app_bars import PromptAppBars
from .base_prompt_edit_screen import BasePromptEditScreen
from typing import Optional


class PromptCreateScreen(BasePromptEditScreen):
    """新規作成画面を構築を行うクラス"""

    def __init__(self):
        super().__init__(self.on_save_clicked)
        self.prompt_create_view = PromptCreateView()

    def bottom_appbar(self) -> Optional[ft.BottomAppBar]:
        """フッターバー(bottom_appbar)を構築"""
        return PromptAppBars.create_bottom_appbar([self.save_btn])

    def build_create_screen(self) -> ft.View:
        """新規作成画面の構築を行う"""
        # 1. 入力欄を初期化する
        self._reset_input_filed()
        # 2. 作成画面遷移時の保存ボタンの無効処理
        self.save_btn.disabled = not self._is_save_enabled()

        # 入力フィールドに入力されるごとに保存ボタンの有効判定を行う
        self.input_field_monitoring()

        # 3. 新規作成画面を構築する
        return self.create_view(route="/create")

    def _reset_input_filed(self):
        """タイトル・本文の入力欄の初期化処理"""
        self.title_input.value = ""
        self.content_input.value = ""

    def on_back_clicked(self, title_input, content_input, e):
        """前の画面に戻る処理をcreate_viewに依頼する"""
        self.prompt_create_view.on_back_clicked(title_input, content_input, e)

    def on_save_clicked(self, e):
        """入力されたタイトルと内容を保存する処理をcreate_viewに依頼する"""
        self.prompt_create_view.on_save_clicked(self.title_input, self.content_input, e)
