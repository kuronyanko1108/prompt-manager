import flet as ft
from src.ui.components.prompt_buttons import PromptButton
from src.ui.components.prompt_input import PromptInput
from src.ui.list_view import PromptListView
from src.ui.create_view import PromptCreateView
from src.ui.edit_view import PromptEditView
from functools import partial


def main(page: ft.Page):
    prompt_list_view = PromptListView()
    prompt_create_view = PromptCreateView()

    def edit_view_on_copy_click(e):
        # クリップボードにコピー
        page.set_clipboard(content_input.value)
        # コピー完了をユーザーに知らせる（スナックバー）
        page.snack_bar = ft.SnackBar(
            content=ft.Text("プロンプトをコピーしました！"),
            duration=2000,  # 2秒間表示
        )
        page.snack_bar.open = True
        page.update()

    def route_change(e):
        # 現在のvalueをクリア
        page.views.clear()

        # URLに応じて表示するViewを追加
        if page.route == "/prompt_list":
            """一覧表示画面"""
            # プロンプト一覧画面はURLが呼ばれるたびにリストを再取得して画面生成を行う
            list_view = ft.View(
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
                    # プロンプト一覧リストの作成
                    build_list_view(),
                    # 新規作成ボタン
                    PromptButton.create_prompt_btn(lambda _: page.go("/create")),
                ],
            )

            page.views.append(list_view)

        elif page.route == "/create":
            """新規作成画面画面"""
            title_input.value = ""
            content_input.value = ""

            create_view = ft.View(
                "/create",
                [
                    ft.Row(
                        controls=[
                            PromptButton.back_to_screen_btn(
                                lambda e: prompt_create_view.on_back_clicked(
                                    title_input, content_input, e
                                )
                            ),
                        ]
                    ),
                    title_input,
                    ft.Divider(height=5),
                    content_input,
                    ft.Divider(height=10),
                    ft.Row(
                        controls=[
                            PromptButton.save_prompt_btn(
                                lambda e: prompt_create_view.on_save_clicked(
                                    title_input,
                                    content_input,
                                    e,
                                )
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
            )
            page.views.append(create_view)

        elif page.route == "/edit":
            """編集画面画面"""
            edit_view = ft.View(
                "/edit",
                [
                    ft.Row(
                        controls=[
                            PromptButton.back_to_screen_btn(
                                lambda e: page.data.on_back_clicked(
                                    title_input, content_input, e
                                )
                            ),
                            PromptButton.delete_prompt_btn(
                                lambda e: page.data.on_delete_clicked(e)
                            ),
                        ]
                    ),
                    title_input,
                    ft.Divider(height=5),
                    content_input,
                    ft.Divider(height=10),
                    ft.Row(
                        controls=[
                            PromptButton.copy_prompt_btn(edit_view_on_copy_click),
                            PromptButton.save_prompt_btn(
                                lambda e: page.data.on_save_clicked(
                                    title_input,
                                    content_input,
                                    e,
                                )
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
            )
            page.views.append(edit_view)

        page.update()

    def handle_edit(prompt, e):
        # 関数の外部でもインスタンスを使えるように一時保管場所（page.data）にインスタンスを生成
        page.data = PromptEditView(prompt.id)
        row = prompt_list_view.open_edit_view(prompt.id)
        title_input.value = row.title
        content_input.value = row.content
        page.go("/edit")

    def handle_copy(prompt, e):
        row = prompt_list_view.open_edit_view(prompt.id)
        # クリップボードにコピー
        page.set_clipboard(row.content)
        # コピー完了をユーザーに知らせる（スナックバー）
        page.snack_bar = ft.SnackBar(
            content=ft.Text("プロンプトをコピーしました！"),
            duration=2000,  # 2秒間表示
        )
        page.snack_bar.open = True
        page.update()

    def build_list_view():
        # プロンプト一覧リストを作るたびにDBからプロンプト一覧を取得する
        prompts = prompt_list_view.show_list()

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
                                    partial(handle_edit, prompt)
                                ),
                                PromptButton.copy_prompt_btn(
                                    partial(handle_copy, prompt)
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

    # ページ構成
    page.title = "Prompt Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 500
    page.window_height = 600
    page.window_resizable = True
    page.padding = 20

    # タイトル欄
    title_input = PromptInput.title_input_box(None)
    # 入力欄
    content_input = PromptInput.content_input_box(None)

    page.on_route_change = route_change
    page.go("/prompt_list")


if __name__ == "__main__":
    ft.app(target=main)
