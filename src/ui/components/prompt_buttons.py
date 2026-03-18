import flet as ft
from .theme import Color, IconSize


class PromptButton:
    @staticmethod
    def create_prompt_btn(go_create):
        """新規作成ボタン"""
        return ft.FloatingActionButton(
            icon=ft.icons.ADD,
            bgcolor=Color.DEFAULT_ICON_COLOR,
            tooltip="新規作成する",
            on_click=go_create,
        )

    @staticmethod
    def edit_prompt_btn(go_edit):
        """編集画面ボタン"""
        return ft.IconButton(
            icon=ft.icons.EDIT,
            icon_color=Color.REGULAR_ICON_COLOR,
            tooltip="編集へ",
            on_click=go_edit,
        )

    @staticmethod
    def save_prompt_btn(on_save):
        """保存ボタン"""
        return ft.TextButton(
            text="保存",
            tooltip="保存する",
            on_click=on_save,
        )

    @staticmethod
    def copy_prompt_btn(on_save):
        """コピーボタン"""
        return ft.IconButton(
            icon_color=Color.DEFAULT_ICON_COLOR,
            icon_size=IconSize.LITTLE_ICON_SIZE,
            icon=ft.icons.CONTENT_COPY,
            tooltip="コピーする",
            on_click=on_save,
        )

    @staticmethod
    def delete_prompt_btn(on_delete):
        """削除ボタン"""
        return ft.IconButton(
            icon=ft.icons.DELETE_OUTLINED,
            icon_color=Color.DANGER_ICON_COLOR,
            icon_size=IconSize.DEFAULT_ICON_SIZE,
            tooltip="削除する",
            on_click=on_delete,
        )

    @staticmethod
    def back_to_screen_btn(go_back):
        """戻るボタン"""
        return ft.IconButton(
            icon_color=Color.DEFAULT_ICON_COLOR,
            icon=ft.icons.ARROW_BACK,
            tooltip="一覧へ戻る",
            on_click=go_back,
        )
