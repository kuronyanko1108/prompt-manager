import flet as ft
from .base_prompt_screen import BasePromptScreen
from ..components.prompt_buttons import PromptButton
from ..components.prompt_input import PromptInput
from ..components.prompt_app_bars import PromptAppBars
from ..components.theme import LayoutSize
from typing import Sequence, Optional


class BasePromptEditScreen(BasePromptScreen):
    """新規作成・編集画面作成の基底クラス。"""

    def __init__(self, on_save):
        # タイトル入力欄
        self.title_input = PromptInput.title_input_box(None)
        # 本文入力欄
        self.content_input = PromptInput.content_input_box(None)
        # 保存ボタン
        self.save_btn = PromptButton.save_prompt_btn(on_save)

    def appbar(self) -> Optional[ft.AppBar]:
        return PromptAppBars.create_appbar(
            lambda e: self.on_back_clicked(self.title_input, self.content_input, e)
        )

    def controls(self) -> Sequence[ft.Control]:
        return [
            ft.ResponsiveRow(
                controls=[
                    self.title_input,
                    ft.Divider(height=LayoutSize.DIVIDER_SMALL),
                    self.content_input,
                ]
            )
        ]

    def bottom_appbar(self) -> Optional[ft.BottomAppBar]:
        """
        フッターバーをサブクラスで実装してください
        Raises:
            NotImplementedError: サブクラスで実装してください

        Returns:
            Optional[ft.BottomAppBar]: ボタンを設定するようにしてください
        """
        raise NotImplementedError("サブクラスで実装してください")

    def input_field_monitoring(self):
        # 入力フィールドに入力されるごとに保存ボタンの有効判定を行う
        self.title_input.on_change = lambda e: self._sync_save_button_state(
            e.page, self.save_btn
        )
        self.content_input.on_change = lambda e: self._sync_save_button_state(
            e.page, self.save_btn
        )

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

    def on_back_clicked(
        self, title_input: ft.TextField, content_input: ft.TextField, e
    ) -> None:
        """
        戻るボタン押下時のコールバック関数を実装してください
        Args:
            title_input (ft.TextField): タイトル入力欄
            content_input (ft.TextField): 本文入力欄
            e : コントロールイベント

        Raises:
            NotImplementedError: サブクラスで実装してください
        """
        raise NotImplementedError("サブクラスで実装してください")
