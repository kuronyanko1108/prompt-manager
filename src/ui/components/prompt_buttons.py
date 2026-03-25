import flet as ft
from .theme import Color, IconSize
from typing import Callable, Optional


class PromptButton:
    "アイコンボタン作成基底メソッド"

    @staticmethod
    def _create_base_icon_button(
        icon: ft.IconData,
        color: str,
        tooltip: str,
        action: Optional[Callable] = None,
        size: int = IconSize.DEFAULT_ICON_SIZE,
        **kwargs,
    ):
        # memo:何か一括で機能を追加したいなら以下のように記述する
        # kwargs.setdefault("hover_color", ft.Colors.AMBER)

        return ft.IconButton(
            icon=icon,
            icon_color=color,
            icon_size=size,
            tooltip=tooltip,
            on_click=action,
            **kwargs,
        )

    "テキストボタン作成基底メソッド"

    @staticmethod
    def _create_base_text_button(
        content: str,
        action: Optional[Callable] = None,
        **kwargs,
    ):
        return ft.TextButton(
            content=content,
            on_click=action,
            **kwargs,
        )

    @staticmethod
    def create_prompt_btn(go_create):
        """新規作成ボタン"""
        return ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor=Color.DEFAULT_ICON_COLOR,
            tooltip="新規作成する",
            on_click=go_create,
        )

    @staticmethod
    def edit_prompt_btn(go_edit):
        """編集画面ボタン"""
        return PromptButton._create_base_icon_button(
            ft.Icons.EDIT,
            Color.NAV_ICON_COLOR,
            "編集へ",
            go_edit,
        )

    @staticmethod
    def save_prompt_btn(on_save):
        """保存ボタン"""
        return PromptButton._create_base_text_button(
            content="保存",
            action=on_save,
            tooltip="保存する",
        )

    @staticmethod
    def copy_prompt_btn(on_copy):
        """コピーボタン"""
        return PromptButton._create_base_icon_button(
            icon=ft.Icons.CONTENT_COPY,
            color=Color.DEFAULT_ICON_COLOR,
            tooltip="コピーする",
            action=on_copy,
            size=IconSize.LITTLE_ICON_SIZE,
        )

    @staticmethod
    def delete_prompt_btn(on_delete):
        """削除ボタン"""
        return PromptButton._create_base_icon_button(
            icon=ft.Icons.DELETE_OUTLINED,
            color=Color.DANGER_ICON_COLOR,
            tooltip="削除する",
            action=on_delete,
        )

    @staticmethod
    def back_to_list_view_btn(go_back):
        """戻るボタン"""
        return PromptButton._create_base_icon_button(
            icon=ft.Icons.ARROW_BACK,
            color=Color.NAV_ICON_COLOR,
            tooltip="一覧へ戻る",
            action=go_back,
        )

    @staticmethod
    def search_btn():
        """検索ボタン"""
        return PromptButton._create_base_icon_button(
            icon=ft.Icons.SEARCH,
            color=Color.NAV_ICON_COLOR,
            tooltip="フェーズ2に開放",
            action=None,
        )

    @staticmethod
    def menu_btn(on_menu_click):
        """メニューボタン"""
        return PromptButton._create_base_icon_button(
            icon=ft.Icons.MENU,
            color=Color.NAV_ICON_COLOR,
            tooltip="メニュー",
            action=on_menu_click,
        )

    @staticmethod
    def dialog_confirm_btn(message, on_confirm_click):
        """ダイアログ確認選択ボタン"""
        return PromptButton._create_base_text_button(
            content=message, action=on_confirm_click
        )
