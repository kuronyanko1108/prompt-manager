import flet as ft
from ..components.prompt_buttons import PromptButton
from ..components.prompt_input import PromptInput
from ..components.theme import LayoutSize
from ..view.create_view import PromptCreateView
from ..components.prompt_app_bars import PromptAppBars
from .base_prompt_screen import BasePromptScreen
from typing import Optional, Sequence


class PromptCreateScreen(BasePromptScreen):
    """新規作成画面を構築を行うクラス"""

    def __init__(self):
        # タイトル入力欄
        self.title_input = PromptInput.title_input_box(None)
        # 本文入力欄
        self.content_input = PromptInput.content_input_box(None)
        # 保存ボタン
        self.create_save_button = PromptButton.save_prompt_btn(
            lambda e: self.prompt_create_view.on_save_clicked(
                self.title_input,
                self.content_input,
                e,
            )
        )
        self.prompt_create_view = PromptCreateView()

    def appbar(self) -> Optional[ft.AppBar]:
        """トップバー（appbar）を構築"""
        return PromptAppBars.create_appbar(
            lambda e: self.prompt_create_view.on_back_clicked(
                self.title_input, self.content_input, e
            )
        )

    def controls(self) -> Sequence[ft.Control]:
        """コントロールを構築"""
        return [
            ft.ResponsiveRow(
                controls=[
                    self.title_input,
                    ft.Divider(height=LayoutSize.DIVIDER_SMALL),
                    self.content_input,
                    ft.Row(
                        controls=[],
                    ),
                ]
            ),
        ]

    def bottom_appbar(self) -> Optional[ft.BottomAppBar]:
        """フッターバー(bottom_appbar)を構築"""
        return PromptAppBars.create_bottom_appbar([self.create_save_button])

    def build_create_screen(self) -> ft.View:
        """新規作成画面の構築を行う"""
        # 1. 入力欄を初期化する
        self._reset_input_filed()
        # 2. 作成画面遷移時の保存ボタンの無効処理
        self.create_save_button.disabled = not self._is_save_enabled()

        # 入力フィールドに入力されるごとに保存ボタンの有効判定を行う
        self.title_input.on_change = lambda e: self._sync_save_button_state(
            e.page, self.create_save_button
        )
        self.content_input.on_change = lambda e: self._sync_save_button_state(
            e.page, self.create_save_button
        )

        # 3. 新規作成画面を構築する
        return self.create_view(route="/create")

    def _reset_input_filed(self):
        """タイトル・本文の入力欄の初期化処理"""
        self.title_input.value = ""
        self.content_input.value = ""

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
