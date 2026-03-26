import flet as ft
from ..components.theme import LayoutSize, DrawerIndex
import asyncio


class PromptDrawerScreen:
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

    async def handle_drawer(self, e: ft.Event[ft.NavigationDrawer], page: ft.Page):
        """引き出しメニュー内の項目選択後にページ遷移を制御します。

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
