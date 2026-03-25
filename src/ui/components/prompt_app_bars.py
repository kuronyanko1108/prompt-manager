import flet as ft
from .prompt_buttons import PromptButton
from .theme import Color, FontSize, LayoutSize
from typing import Callable


class PromptAppBars:
    @staticmethod
    def list_appbar(on_menu_click: Callable) -> ft.AppBar:
        """一覧表示画面のトップバーを生成する

        Args:
            on_menu_click (Callable): メニューボタンがクリックされた時に実行されるイベントハンドラ。
                                    通常はドロワーの表示処理を渡します。

        Returns:
            ft.AppBar: 構築済みのAppBarオブジェクト
        """
        return ft.AppBar(
            leading=PromptButton.menu_btn(on_menu_click),
            title=ft.Text(
                "Prompt Manager",
                size=FontSize.TITLE_FONT_SIZE,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=Color.TITLE_COLOR,
            ),
            center_title=True,
            actions=[
                PromptButton.search_btn(),
                ft.Container(width=LayoutSize.MARGIN_CONTAINER_WIDTH),
            ],
        )

    @staticmethod
    def create_appbar(on_back_click: Callable) -> ft.AppBar:
        """編集画面・新規作成画面のトップバーを生成する

        Args:
            on_back_click (Callable): 戻るボタンを押下されたとき実行されるイベントハンドラ

        Returns:
            ft.AppBar: 構築済みのAppBarオブジェクト
        """
        return ft.AppBar(leading=PromptButton.back_to_list_view_btn(on_back_click))

    @staticmethod
    def create_bottom_appbar(buttons: list) -> ft.BottomAppBar:
        """編集画面・新規作成画面のフッターバーを生成する

        Args:
            buttons (list): フッターに配置するボタンのリスト

        Returns:
            ft.BottomAppBar: 中央揃えで配置されたボタン群を含むBottomAppBarオブジェクト
        """
        return ft.BottomAppBar(
            ft.Row(
                controls=buttons,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
