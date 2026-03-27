import flet as ft
from src.ui.page_factory import PageFactory
from src.ui.screens.prompt_list_screen import PromptListScreen
from src.ui.screens.prompt_create_screen import PromptCreateScreen
from src.ui.screens.prompt_edit_screen import PromptEditScreen
from src.ui.screens.prompt_drawer_screen import PromptDrawerScreen
from src.ui.view.list_view import PromptListView
from src.ui.view.create_view import PromptCreateView
from src.ui.view.edit_view import PromptEditView
from src.controllers.prompt_controller import PromptController
from src.services.prompt_service import PromptService
from src.repositories.sqlite_prompt_repository import SQLitePromptRepository


def main(page: ft.Page):

    repository = SQLitePromptRepository()

    service = PromptService(repository)

    controller = PromptController(service)

    list_view = PromptListView(controller)
    create_view = PromptCreateView(controller)
    edit_view = PromptEditView(controller, 0)  # IDはダミーで設定

    list_screen = PromptListScreen(list_view)
    create_screen = PromptCreateScreen(create_view)
    list_view = PromptListView(controller)
    edit_screen = PromptEditScreen(edit_view)
    drawer_screen = PromptDrawerScreen()

    def route_change():
        page.views.clear()

        factory = PageFactory(list_screen, create_screen, edit_screen, drawer_screen)

        view = factory.get_view(page)
        page.views.append(view)
        if page.route == "/":
            factory.set_drawer(page)

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
