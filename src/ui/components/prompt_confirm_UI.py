import flet as ft


class PromptConfirmUI:
    @staticmethod
    def show_confirm_dialog(
        current_page: ft.Page, dialog_title: str, dialog_content: str, on_yes_action
    ):
        # ダイアログを閉じるための補助関数
        def close_dlg(is_yes):
            modal_dialog.open = False
            current_page.update()
            if is_yes:
                on_yes_action(current_page)

        modal_dialog = ft.AlertDialog(
            modal=False,
            title=ft.Text(dialog_title),
            content=ft.Text(dialog_content),
            actions=[
                ft.TextButton("Yes", on_click=lambda _: close_dlg(True)),
                ft.TextButton("No", on_click=lambda _: close_dlg(False)),
            ],
            # アクションの水平方向のレイアウト
            actions_alignment=ft.MainAxisAlignment.END,
        )

        current_page.overlay.append(modal_dialog)  # ダイアログをページにセット
        modal_dialog.open = True  # ダイアログを開く
        current_page.update()
