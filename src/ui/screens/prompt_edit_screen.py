import flet as ft
from ..components.prompt_buttons import PromptButton
from ..components.prompt_input import PromptInput
from ..components.theme import LayoutSize
from ..view.list_view import PromptListView
from ..view.edit_view import PromptEditView
from ..components.prompt_app_bars import PromptAppBars
from .base_prompt_screen import BasePromptScreen
from typing import Optional, Sequence


class PromptEditScreen(BasePromptScreen):
    """編集画面を構築を行うクラス"""

    def __init__(self):
        # タイトル入力欄
        self.title_input = PromptInput.title_input_box(None)
        # 本文入力欄
        self.content_input = PromptInput.content_input_box(None)
        # 保存ボタン
        self.save_btn = PromptButton.save_prompt_btn(
            lambda e: self.edit_view.on_save_clicked(
                self.title_input,
                self.content_input,
                e,
            )
        )
        self.list_view = PromptListView()
        self.edit_view: Optional[PromptEditView] = None

    def appbar(self) -> Optional[ft.AppBar]:
        """トップバー（appbar）を構築"""
        view = self.edit_view

        if view is not None:
            return PromptAppBars.create_appbar(
                lambda e: view.on_back_clicked(self.title_input, self.content_input, e)
            )

        return None

    def controls(self) -> Sequence[ft.Control]:
        """コントロールを構築"""
        return [
            ft.ResponsiveRow(
                controls=[
                    self.title_input,
                    ft.Divider(height=LayoutSize.DIVIDER_SMALL),
                    self.content_input,
                ]
            ),
            ft.Row(),
        ]

    def bottom_appbar(self) -> Optional[ft.BottomAppBar]:
        """フッターバー(bottom_appbar)を構築"""
        view = self.edit_view
        if view is not None:
            # ボタン
            copy_btn = PromptButton.copy_prompt_btn(
                lambda e: view.on_copy_clicked(self.content_input, e)
            )
            delete_btn = PromptButton.delete_prompt_btn(
                lambda e: view.on_delete_clicked(e)
            )
            buttons = [copy_btn, self.save_btn, delete_btn]

            return PromptAppBars.create_bottom_appbar(buttons)

        return None

    def build_edit_screen(self, prompt_id: int) -> ft.View:
        """編集画面画面の構築を行う"""
        # 1. idからタイトルと本文を取得し、入力欄に設定する
        self.edit_view = PromptEditView(prompt_id)
        row = self.list_view.open_edit_view(prompt_id)
        self.title_input.value = row.title
        self.content_input.value = row.content

        # 入力フィールドに入力されるごとに保存ボタンの有効判定を行う
        self.title_input.on_change = lambda e: self._sync_save_button_state(
            e.page, self.save_btn
        )
        self.content_input.on_change = lambda e: self._sync_save_button_state(
            e.page, self.save_btn
        )
        # 2. 編集画面遷移時の保存ボタン状態同期
        self.save_btn.disabled = not self._is_save_enabled()
        # 3. 編集作成画面を構築する
        return self.create_view(route="/edit")

    def _is_save_enabled(self) -> bool:
        """保存ボタン有効／無効判定処理"""
        title = (self.title_input.value or "").strip()
        content = (self.content_input.value or "").strip()
        return bool(title and content)

    def _sync_save_button_state(
        self, current_page: ft.Page, save_button: ft.TextButton
    ):
        """保存ボタン状態更新処理"""
        save_button.disabled = not self._is_save_enabled()
        current_page.update()
