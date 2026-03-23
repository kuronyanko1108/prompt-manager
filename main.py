import flet as ft
from src.ui.page_factory import PageFactory
import asyncio


def main(page: ft.Page):
    prompt_factory = PageFactory()

    def route_change():
        page.views.clear()
        if page.route == "/":
            view = prompt_factory.prompt_list_screen(page)

        elif page.route == "/create":
            view = prompt_factory.create_view_screen()

        elif page.route == "/edit":
            view = prompt_factory.edit_view_screen()

        # page.views.append(
        #     ft.View(
        #         route="/",
        #         controls=[
        #             ft.AppBar(
        #                 title=ft.Text("Flet app"),
        #             ),
        #         ],
        #     )
        # )

        page.views.append(view)
        # page.update()

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
