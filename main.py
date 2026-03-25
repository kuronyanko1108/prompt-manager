import flet as ft
from src.ui.page_factory import PageFactory


def main(page: ft.Page):
    prompt_factory = PageFactory()

    def route_change():
        page.views.clear()

        view = prompt_factory.get_view(page)
        page.views.append(view)
        if page.route == "/":
            prompt_factory.set_drawer(page)

    # ページ構成
    page.title = "Prompt Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.width = 900
    page.height = 700
    page.window.resizable = True
    page.padding = 20

    async def view_pop(e):
        if e.view is not None:
            print("View pop:", e.view)
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()


if __name__ == "__main__":
    ft.run(main)
