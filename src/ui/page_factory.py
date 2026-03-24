import flet as ft
from .components.prompt_buttons import PromptButton
from .components.prompt_input import PromptInput
from .list_view import PromptListView
from .edit_view import PromptEditView
from .create_view import PromptCreateView
from .components.theme import Color
from functools import partial
import asyncio


class PageFactory:
    def __init__(self):
        self.prompt_list_view = PromptListView()
        self.prompt_create_view = PromptCreateView()
        self.title_input = PromptInput.title_input_box(None)
        self.content_input = PromptInput.content_input_box(None)

        # 一覧リスト用
        self.container = None
        self.click_token = 0

    def prompt_list_screen(self, current_page: ft.Page) -> ft.View:
        """一覧表示画面"""
        top_bar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.MENU,
                on_click=lambda _: asyncio.create_task(
                    self.handle_show_drawer(current_page)
                ),
            ),
            title=ft.Text(
                "Prompt Manager",
                size=28,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=Color.TITLE_COLOR,
            ),
            center_title=True,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.SEARCH,
                    disabled=True,
                    tooltip="フェーズ２作成予定！",
                ),
                ft.Container(width=10),
            ],
        )

        # プロンプト一覧画面はURLが呼ばれるたびにリストを再取得して画面生成を行う
        return ft.View(
            route="/",
            appbar=top_bar,
            controls=[
                # プロンプト一覧リストの作成処理
                self.build_list_view(),
                PromptButton.create_prompt_btn(
                    lambda _: asyncio.create_task(current_page.push_route("/create"))
                ),
            ],
        )

    def create_view_screen(self):
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
            appbar=ft.AppBar(
                leading=PromptButton.back_to_list_view_btn(
                    lambda e: self.prompt_create_view.on_back_clicked(
                        self.title_input, self.content_input, e
                    )
                )
            ),
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        self.title_input,
                        ft.Divider(height=5),
                        self.content_input,
                        ft.Row(
                            controls=[],
                        ),
                    ]
                ),
            ],
            bottom_appbar=ft.BottomAppBar(
                ft.Row(
                    controls=[
                        create_save_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ),
        )

    def edit_view_screen(self):
        """編集画面画面"""

        edit_save_button = PromptButton.save_prompt_btn(
            lambda e: e.page.data.on_save_clicked(
                self.title_input,
                self.content_input,
                e,
            )
        )
        self.title_input.on_change = lambda e: self._sync_save_button_state(
            e.page, edit_save_button
        )
        self.content_input.on_change = lambda e: self._sync_save_button_state(
            e.page, edit_save_button
        )

        # 編集画面遷移時の保存ボタン状態同期
        edit_save_button.disabled = not self._is_save_enabled()

        return ft.View(
            route="/edit",
            appbar=ft.AppBar(
                leading=PromptButton.back_to_list_view_btn(
                    lambda e: e.page.data.on_back_clicked(
                        self.title_input, self.content_input, e
                    )
                ),
                actions=[],
            ),
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        self.title_input,
                        ft.Divider(height=5),
                        self.content_input,
                        ft.Divider(height=10),
                    ]
                ),
                ft.Row(),
            ],
            bottom_appbar=ft.BottomAppBar(
                ft.Row(
                    controls=[
                        PromptButton.copy_prompt_btn(
                            lambda e: e.page.data.on_copy_clicked(self.content_input, e)
                        ),
                        edit_save_button,
                        PromptButton.delete_prompt_btn(
                            lambda e: e.page.data.on_delete_clicked(e)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ),
        )

    def build_list_view(self):
        """プロンプト一覧リスト生成"""
        # DBからプロンプト一覧を取得する
        prompts = self.prompt_list_view.show_list()

        prompt_item_list = []
        for prompt in prompts:
            row_container = ft.Container(
                border=ft.Border.only(bottom=ft.BorderSide(2, Color.PROMPT_LIST_COLOR)),
            )

            """ボタン"""
            # 編集ボタン
            edit_btn = PromptButton.edit_prompt_btn(partial(self.handle_edit, prompt))
            # コピーボタン
            copy_btn = PromptButton.copy_prompt_btn(
                partial(self.copy_click_handler, prompt, row_container)
            )
            buttons = [edit_btn, copy_btn]

            # コンテナ構成
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
        # 関数の外部でもインスタンスを使えるように一時保管場所（age.data）にインスタンスを生成
        e.page.data = PromptEditView(prompt.id)

        # 一覧リストで選択したプロンプトのidに紐づくタイトル、本文を入力欄に設定する
        row = self.prompt_list_view.open_edit_view(prompt.id)
        self.title_input.value = row.title
        self.content_input.value = row.content

        asyncio.create_task(e.page.push_route("/edit"))

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

    def copy_click_handler(self, prompt, row_container, e):

        # クリップボードにコピー
        self.prompt_list_view.on_copy_clicked(prompt, e)

        # 前回行のハイライト表示を解除
        if self.container is not None:
            self.container.border = ft.Border.only(
                bottom=ft.BorderSide(2, Color.PROMPT_LIST_COLOR)
            )
            e.page.update()

        # 選択行をハイライト表示
        row_container.border = ft.Border.only(
            bottom=ft.BorderSide(2, Color.SELECT_COLOR)
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
        await asyncio.sleep(0.5)

        """0.5秒後に動く処理"""
        # 最新クリックだけ解除する（古いタスクは何もしない）
        if self.click_token != current_token:
            return
        target_container.border = ft.Border.only(
            bottom=ft.BorderSide(2, Color.PROMPT_LIST_COLOR)
        )

        # 参照もクリア
        if self.container is target_container:
            self.container = None

        current_page.update()

    def transform_text(self, text: str, max_length: int = 50) -> str:
        """文字列から改行等を除去し、指定した文字数で切り捨てて返却する

        Args:
            text (str): 処理対象の文字列
            max_length (int, optional): 最大文字数。デフォルト値は50

        Returns:
            str: 正規化および、長さ調整後の文字列
        """
        #  改行/タブ/連続空白を1スペースに正規化
        normalized = " ".join((text or "").split())

        if len(normalized) <= max_length:
            return normalized
        # 最大文字数を超える場合は末尾に…を追加する
        return normalized[: max_length - 1] + "…"

    def create_drawer(self, current_page: ft.Page):
        """一覧表示画面の引き出しメニュー（NavigationDrawer）を作成し、ページに設定する。

        Args:
            current_page (ft.Page): ドロワーを設置する対象のページオブジェクト。
        """
        current_page.drawer = ft.NavigationDrawer(
            on_change=lambda e: asyncio.create_task(
                self.handle_drawer(e, current_page)
            ),
            controls=[
                ft.Container(height=12),
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
        if idx == 0:
            asyncio.create_task(page.push_route("/create"))
