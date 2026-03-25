import flet as ft
from .screens.prompt_list_screen import PromptListScreen
from .screens.prompt_create_screen import PromptCreateScreen
from .screens.prompt_edit_screen import PromptEditScreen


class PageFactory:
    def __init__(self):

        self.list_screen = PromptListScreen()
        self.create_screen = PromptCreateScreen()
        self.edit_screen = PromptEditScreen()

    def get_view(self, current_page: ft.Page) -> ft.View:
        """URL(route)に基づいて、対応するScreenクラスからViewを生成して返します。

        Args:
            current_page (_type_): ページ操作を行うためのPageオブジェクト

        Returns:
            ft.View: 構築されたFletのViewオブジェクト
        """

        if current_page.route == "/":
            return self.list_screen.build_list_screen(current_page)

        elif current_page.route == "/create":
            return self.create_screen.build_create_screen()

        elif current_page.route.startswith("/edit/"):
            try:
                prompt_id = int(current_page.route.split("/")[-1])
            except (ValueError, IndexError):
                # IDが不正な場合は一覧画面に戻すなどの処理
                return self.list_screen.build_list_screen(current_page)

            return self.edit_screen.build_edit_screen(prompt_id)

        # TODO  不正なroute用のエラーページを実装する
        # 現状は一時的に一覧画面へリダイレクト
        return self.list_screen.build_list_screen(current_page)

    def set_drawer(self, page: ft.Page):
        self.list_screen.build_drawer(page)
