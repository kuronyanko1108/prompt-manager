import flet as ft
from ..components.prompt_buttons import PromptButton
from ..components.prompt_input import PromptInput
from ..components.theme import Color, LayoutSize, Timing, CharLimit, DrawerIndex
from ..view.list_view import PromptListView
from ..components.prompt_app_bars import PromptAppBars
from functools import partial
import asyncio
from .base_prompt_screen import BasePromptScreen
from typing import Optional, Sequence


class PromptListScreen(BasePromptScreen):
    """一覧表示画面を構築を行うクラス"""

    def __init__(self):
        self.prompt_list_view = PromptListView()
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
                lambda _: asyncio.create_task(self.handle_show_drawer(self.page)),
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
        # プロンプト一覧画面はURLが呼ばれるたびにリストを再取得して画面生成を行う
        return self.create_view(route="/")

    def build_list_view(self):
        """プロンプト一覧リスト生成"""
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
            edit_btn = PromptButton.edit_prompt_btn(partial(self.handle_edit, prompt))
            # コピーボタン
            copy_btn = PromptButton.copy_prompt_btn(
                partial(self.copy_click_handler, prompt, row_container)
            )
            buttons = [edit_btn, copy_btn]

            # プロンプトリストの表示構成
            tile = ft.ListTile(
                leading=ft.Icon(ft.Icons.DESCRIPTION),  # 左側のアイコン
                title=ft.Text(f"{prompt.title}"),  # タイトル
                subtitle=ft.Text(f"{self.transform_text(prompt.content)}"),
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

    def handle_edit(self, prompt, e):

        asyncio.create_task(e.page.push_route(f"/edit/{prompt.id}"))

    def copy_click_handler(self, prompt, row_container, e):

        # クリップボードにコピー
        self.prompt_list_view.on_copy_clicked(prompt, e)

        # 前回行のハイライト表示を解除
        if self.container is not None:
            self.container.border = ft.Border.only(
                bottom=ft.BorderSide(
                    LayoutSize.FRAME_THICKNESS, Color.PROMPT_LIST_FRAME_COLOR
                )
            )
            e.page.update()

        # 選択行をハイライト表示
        row_container.border = ft.Border.only(
            bottom=ft.BorderSide(LayoutSize.FRAME_THICKNESS, Color.SELECT_COLOR)
        )
        self.container = row_container
        e.page.update()

        # 連打判定用トークン
        self.click_token += 1
        current_token = self.click_token

        # 500ms後の解除を予約
        e.page.run_task(
            self.clear_highlight_if_latest, current_token, e.page, row_container
        )

    async def clear_highlight_if_latest(
        self, current_token, current_page, target_container
    ):
        """非同期処理"""
        # ハイライトを0.5秒の間表示
        await asyncio.sleep(Timing.HIGHLIGHT_ANIMATION_TIME)

        """0.5秒後に動く処理"""
        # 最新クリックだけ解除する（古いタスクは何もしない）
        if self.click_token != current_token:
            return
        target_container.border = ft.Border.only(
            bottom=ft.BorderSide(
                LayoutSize.FRAME_THICKNESS, Color.PROMPT_LIST_FRAME_COLOR
            )
        )

        # 参照もクリア
        if self.container is target_container:
            self.container = None

        current_page.update()

    def transform_text(
        self, text: str, max_length: int = CharLimit.SUBTITLE_MAX_LENGTH
    ) -> str:
        """文字列から改行等を除去し、指定した文字数で切り捨てて返却する

        Args:
            text (str): 処理対象の文字列
            max_length (int, optional): 最大文字数。デフォルト値は50文字

        Returns:
            str: 正規化および、長さ調整後の文字列
        """
        #  改行/タブ/連続空白を1スペースに正規化
        normalized = " ".join((text or "").split())

        if len(normalized) <= max_length:
            return normalized
        # 最大文字数を超える場合は末尾に…を追加する
        return normalized[: max_length - 1] + "…"

    def build_drawer(self, current_page: ft.Page):
        """一覧表示画面の引き出しメニュー（NavigationDrawer）を作成し、ページに設定する。

        Args:
            current_page (ft.Page): ドロワーを設置する対象のページオブジェクト。
        """
        current_page.drawer = ft.NavigationDrawer(
            on_change=lambda e: asyncio.create_task(
                self.handle_drawer(e, current_page)
            ),
            controls=[
                ft.Container(height=LayoutSize.CONTAINER_HEIGHT),
                ft.NavigationDrawerDestination(
                    label="新規作成する",
                    icon=ft.Icons.ADD_CIRCLE_OUTLINE_OUTLINED,
                ),
            ],
        )

    async def handle_show_drawer(self, page: ft.Page):
        await page.show_drawer()

    async def handle_drawer(self, e: ft.Event[ft.NavigationDrawer], page: ft.Page):
        """引き出しメニュー内の項目選択後にページ遷移を制御する。

        Args:
            e (ft.Event[ft.NavigationDrawer]):ドロワーの選択変更イベント。
            page (ft.Page): 遷移操作を行う対象のページ。
        """
        # 1. ドロワーを閉じる
        await page.close_drawer()

        # 2. 選択されたインデックスを取得
        idx = e.control.selected_index

        # 3. インデックスの処理に応じてページ遷移する
        if idx == DrawerIndex.CREATE:
            asyncio.create_task(page.push_route("/create"))
