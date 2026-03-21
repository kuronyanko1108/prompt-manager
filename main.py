import flet as ft
from src.ui.page_factory import PageFactory


def main(page: ft.Page):
    prompt_factory = PageFactory()

    def route_change(e):
        page.views.clear()

        if page.route == "/prompt_list":
            view = prompt_factory.prompt_list_screen(page)

        elif page.route == "/create":
            view = prompt_factory.create_view_screen()

        elif page.route == "/edit":
            view = prompt_factory.edit_view_screen()

        page.views.append(view)
        page.update()

    # ページ構成
    page.title = "Prompt Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 500
    page.window_height = 600
    page.window_resizable = True
    page.padding = 20

    page.on_route_change = route_change
    page.go("/prompt_list")


if __name__ == "__main__":
    ft.app(target=main)
