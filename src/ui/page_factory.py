import flet as ft
from .components.prompt_buttons import PromptButton
from .components.prompt_input import PromptInput
from .list_view import PromptListView
from .edit_view import PromptEditView
from .create_view import PromptCreateView
from functools import partial


class PageFactory:
    def __init__(self):
        self.prompt_list_view = PromptListView()
        self.prompt_create_view = PromptCreateView()
        self.title_input = PromptInput.title_input_box(None)
        self.content_input = PromptInput.content_input_box(None)

    def prompt_list_screen(self, current_page: ft.Page):
        """一覧表示画面"""
        # プロンプト一覧画面はURLが呼ばれるたびにリストを再取得して画面生成を行う
        return ft.View(
            "/prompt_list",
            [
                ft.Text(
                    "Prompt Manager",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.colors.BLUE_400,
                ),
                ft.Divider(height=10),
                # プロンプト一覧リストの作成処理
                self.build_list_view(),
                # 新規作成ボタン
                PromptButton.create_prompt_btn(lambda _: current_page.go("/create")),
            ],
        )

    def create_view_screen(self):
        """新規作成画面画面"""
        self.title_input.value = ""
        self.content_input.value = ""

        return ft.View(
            "/create",
            [
                ft.Row(
                    controls=[
                        PromptButton.back_to_list_view_btn(
                            lambda e: self.prompt_create_view.on_back_clicked(
                                self.title_input, self.content_input, e
                            )
                        ),
                    ]
                ),
                self.title_input,
                ft.Divider(height=5),
                self.content_input,
                ft.Divider(height=10),
                ft.Row(
                    controls=[
                        PromptButton.save_prompt_btn(
                            lambda e: self.prompt_create_view.on_save_clicked(
                                self.title_input,
                                self.content_input,
                                e,
                            )
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        )

    def edit_view_screen(self):
        """編集画面画面"""
        return ft.View(
            "/edit",
            [
                ft.Row(
                    controls=[
                        PromptButton.back_to_list_view_btn(
                            lambda e: e.page.data.on_back_clicked(
                                self.title_input, self.content_input, e
                            )
                        ),
                        PromptButton.delete_prompt_btn(
                            lambda e: e.page.data.on_delete_clicked(e)
                        ),
                    ]
                ),
                self.title_input,
                ft.Divider(height=5),
                self.content_input,
                ft.Divider(height=10),
                ft.Row(
                    controls=[
                        PromptButton.copy_prompt_btn(
                            lambda e: e.page.data.on_copy_clicked(self.content_input, e)
                        ),
                        PromptButton.save_prompt_btn(
                            lambda e: e.page.data.on_save_clicked(
                                self.title_input,
                                self.content_input,
                                e,
                            )
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        )

    def build_list_view(self):
        """プロンプト一覧リスト生成"""
        # DBからプロンプト一覧を取得する
        prompts = self.prompt_list_view.show_list()

        # 画面表示用プロンプト一覧リストを作成
        return ft.ListView(
            expand=True,
            spacing=10,
            controls=[
                control
                for prompt in prompts
                for control in [
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.DESCRIPTION),  # 左側のアイコン
                        title=ft.Text(f"{prompt.title}"),  # タイトル
                        trailing=ft.Row(  # 編集ボタン + コピーボタン
                            [
                                PromptButton.edit_prompt_btn(
                                    partial(self.handle_edit, prompt)
                                ),
                                PromptButton.copy_prompt_btn(
                                    partial(
                                        self.prompt_list_view.on_copy_clicked,
                                        prompt,
                                    )
                                ),
                            ],
                            tight=True,  # ボタンの間隔を詰める
                        ),
                    ),
                    ft.Divider(
                        height=1,
                        thickness=1,
                    ),
                ]
            ],
        )

    def handle_edit(self, prompt, e):
        # 関数の外部でもインスタンスを使えるように一時保管場所（age.data）にインスタンスを生成
        e.page.data = PromptEditView(prompt.id)

        # 一覧リストで選択したプロンプトのidに紐づくタイトル、本文を入力欄に設定する
        row = self.prompt_list_view.open_edit_view(prompt.id)
        self.title_input.value = row.title
        self.content_input.value = row.content

        e.page.go("/edit")
