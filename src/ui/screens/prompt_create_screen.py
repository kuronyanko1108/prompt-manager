import flet as ft
from ..components.prompt_buttons import PromptButton
from ..components.prompt_input import PromptInput
from ..components.theme import LayoutSize
from ..view.create_view import PromptCreateView
from ..components.prompt_app_bars import PromptAppBars


class PromptCreateScreen:
    def __init__(self):
        self.title_input = PromptInput.title_input_box(None)
        self.content_input = PromptInput.content_input_box(None)
        self.prompt_create_view = PromptCreateView()

    def build_create_screen(self) -> ft.View:
        """新規作成画面画面"""
        self.title_input.value = ""
        self.content_input.value = ""

        # 保存ボタン
        create_save_button = PromptButton.save_prompt_btn(
            lambda e: self.prompt_create_view.on_save_clicked(
                self.title_input,
                self.content_input,
                e,
            )
        )
        buttons = [create_save_button]

        # 入力フィールドに入力されるごとに保存ボタンの有効判定を行う
        self.title_input.on_change = lambda e: self._sync_save_button_state(
            e.page, create_save_button
        )
        self.content_input.on_change = lambda e: self._sync_save_button_state(
            e.page, create_save_button
        )
        # 新規作成画面遷移時の保存ボタンの無効処理
        create_save_button.disabled = not self._is_save_enabled()

        return ft.View(
            route="/create",
            appbar=PromptAppBars.create_appbar(
                lambda e: self.prompt_create_view.on_back_clicked(
                    self.title_input, self.content_input, e
                )
            ),
            controls=[
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
