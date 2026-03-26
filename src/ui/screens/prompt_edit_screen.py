import flet as ft
from ..components.prompt_buttons import PromptButton
from ..view.list_view import PromptListView
from ..view.edit_view import PromptEditView
from ..components.prompt_app_bars import PromptAppBars
from .base_prompt_edit_screen import BasePromptEditScreen
from typing import Optional


class PromptEditScreen(BasePromptEditScreen):
    """編集画面を構築を行うクラス"""

    def __init__(self):
        super().__init__(self.on_save_clicked)
        self.list_view = PromptListView()
        self.edit_view: Optional[PromptEditView] = None

    def bottom_appbar(self) -> Optional[ft.BottomAppBar]:
        """フッターバー(bottom_appbar)を構築"""
        copy_btn = PromptButton.copy_prompt_btn(
            lambda e: self.on_copy_clicked(self.content_input, e)
        )
        delete_btn = PromptButton.delete_prompt_btn(self.on_delete_clicked)
        buttons = [copy_btn, self.save_btn, delete_btn]

        return PromptAppBars.create_bottom_appbar(buttons)

    def build_edit_screen(self, prompt_id: int) -> ft.View:
        """編集画面画面の構築を行う"""
        # 1. idからタイトルと本文を取得し、入力欄に設定する
        self.edit_view = PromptEditView(prompt_id)
        row = self.list_view.open_edit_view(prompt_id)
        self.title_input.value = row.title
        self.content_input.value = row.content

        # 2. 編集画面遷移時の保存ボタン状態同期
        self.save_btn.disabled = not self._is_save_enabled()

        # 入力フィールドに入力されるごとに保存ボタンの有効判定を行う
        self.input_field_monitoring()

        # 3. 編集作成画面を構築する
        return self.create_view(route="/edit")

    def on_back_clicked(self, title_input, content_input, e):
        """前の画面に戻る処理をedit_viewに依頼する"""
        self.edit_view.on_back_clicked(title_input, content_input, e)

    def on_save_clicked(self, e):
        """入力されたタイトルと内容を保存する処理をedit_viewに依頼する"""
        self.edit_view.on_save_clicked(self.title_input, self.content_input, e)

    def on_delete_clicked(self, e):
        """現在のデータの削除処理をedit_viewに依頼する"""
        self.edit_view.on_delete_clicked(e)

    def on_copy_clicked(self, content_input, e):
        """本文の入力内容をクリップボードにコピーする"""
        self.edit_view.on_copy_clicked(content_input, e)
