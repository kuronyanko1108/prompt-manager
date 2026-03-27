import flet as ft
from ..components.prompt_buttons import PromptButton
from ..components.prompt_input import PromptInput
from ..components.theme import Color, LayoutSize
from ..view.list_view import PromptListView
from ..components.prompt_app_bars import PromptAppBars
from functools import partial
import asyncio
from .base_prompt_screen import BasePromptScreen
from typing import Optional, Sequence
from ..handlers.prompt_list_event_handlers import PromptListEventHandlers
from ..utils.ui_utils import UiUtils


class PromptListScreen(BasePromptScreen):
    """一覧表示画面を構築を行うクラス"""

    def __init__(self, view: PromptListView):
        self.prompt_list_view = view
        self.title_input = PromptInput.title_input_box(None)
        self.content_input = PromptInput.content_input_box(None)
        self.page: Optional[ft.Page] = None

        # 一覧リスト用
        self.container = None
        self.click_token = 0

    def appbar(self) -> Optional[ft.AppBar]:
        """トップバー（appbar）を構築"""
        if self.page is not None:
            return PromptAppBars.list_appbar(
                lambda e: asyncio.create_task(
                    PromptListEventHandlers.on_drawer_click_handle(self.page)
                ),
            )
        return None

    def controls(self) -> Sequence[ft.Control]:
        """コントロールを構築"""
        if self.page is not None:
            return [
                # プロンプト一覧リストの作成処理
                self.build_list_view(),
                PromptButton.create_prompt_btn(
                    lambda _: asyncio.create_task(self.page.push_route("/create"))
                ),
            ]
        return []

    def bottom_appbar(self) -> Optional[ft.BottomAppBar]:
        """フッターバー(bottom_appbar)を構築"""
        return None

    def build_list_screen(self, current_page: ft.Page) -> ft.View:
        """一覧表示画面の構築"""
        self.page = current_page
        # 2. 一覧表示画面を構築する
        return self.create_view(route="/")

    def build_list_view(self):
        """プロンプト一覧リスト生成"""
        handlers = PromptListEventHandlers()

        # DBからプロンプト一覧を取得する
        prompts = self.prompt_list_view.show_list()

        prompt_item_list = []
        for prompt in prompts:
            row_container = ft.Container(
                border=ft.Border.only(
                    bottom=ft.BorderSide(
                        LayoutSize.FRAME_THICKNESS, Color.PROMPT_LIST_FRAME_COLOR
                    )
                ),
            )

            """ボタン"""
            # 編集ボタン
            edit_btn = PromptButton.edit_prompt_btn(
                partial(handlers.on_edit_click_handle, prompt)
            )
            # コピーボタン
            copy_btn = PromptButton.copy_prompt_btn(
                partial(
                    handlers.on_copy_click_handle,
                    self.prompt_list_view,
                    prompt,
                    row_container,
                )
            )
            buttons = [edit_btn, copy_btn]

            # プロンプトリストの表示構成
            tile = ft.ListTile(
                leading=ft.Icon(ft.Icons.DESCRIPTION),  # 左側のアイコン
                title=ft.Text(f"{prompt.title}"),  # タイトル
                subtitle=ft.Text(f"{UiUtils.transform_text(prompt.content)}"),
                trailing=ft.Row(
                    buttons,
                    tight=True,  # ボタンの間隔を詰める
                ),
            )
            row_container.content = tile

            prompt_item_list.append(row_container)

        # 画面表示用プロンプト一覧リストを作成
        return ft.ListView(
            controls=prompt_item_list,
            expand=True,
        )
