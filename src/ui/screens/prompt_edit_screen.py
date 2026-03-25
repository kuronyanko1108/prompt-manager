import flet as ft
from ..components.prompt_buttons import PromptButton
from ..components.prompt_input import PromptInput
from ..components.theme import LayoutSize
from ..view.list_view import PromptListView
from ..view.edit_view import PromptEditView
from ..components.prompt_app_bars import PromptAppBars
import asyncio


class PromptEditScreen:
    def __init__(self):
        self.list_view = PromptListView()
        self.title_input = PromptInput.title_input_box(None)
        self.content_input = PromptInput.content_input_box(None)

    def build_edit_screen(self, prompt_id: int) -> ft.View:
        """編集画面画面"""

        # idからタイトルと本文を取得し、入力欄に設定する
        edit_view = PromptEditView(prompt_id)
        row = self.list_view.open_edit_view(prompt_id)
        self.title_input.value = row.title
        self.content_input.value = row.content

        # ボタン
        copy_btn = PromptButton.copy_prompt_btn(
            lambda e: edit_view.on_copy_clicked(self.content_input, e)
        )
        save_btn = PromptButton.save_prompt_btn(
            lambda e: edit_view.on_save_clicked(
                self.title_input,
                self.content_input,
                e,
            )
        )
        delete_btn = PromptButton.delete_prompt_btn(
            lambda e: edit_view.on_delete_clicked(e)
        )
        buttons = [copy_btn, save_btn, delete_btn]

        self.title_input.on_change = lambda e: self._sync_save_button_state(
            e.page, save_btn
        )
        self.content_input.on_change = lambda e: self._sync_save_button_state(
            e.page, save_btn
        )
        # 編集画面遷移時の保存ボタン状態同期
        save_btn.disabled = not self._is_save_enabled()

        return ft.View(
            route="/edit",
            appbar=PromptAppBars.create_appbar(
                lambda e: edit_view.on_back_clicked(
                    self.title_input, self.content_input, e
                )
            ),
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        self.title_input,
                        ft.Divider(height=LayoutSize.DIVIDER_SMALL),
                        self.content_input,
                        ft.Divider(height=LayoutSize.DIVIDER_LARGE),
                    ]
                ),
                ft.Row(),
            ],
            bottom_appbar=PromptAppBars.create_bottom_appbar(buttons),
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
