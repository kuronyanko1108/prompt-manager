import flet as ft


class PromptConfirmUI:
    @staticmethod
    def show_confirm_dialog(e, dialog_title, dialog_content, on_yes_action):
        # ダイアログを閉じるための補助関数
        def close_dlg(is_yes, e):
            modal_dialog.open = False
            e.page.update()
            if is_yes:
                on_yes_action(e)

        modal_dialog = ft.AlertDialog(
            modal=False,
            title=ft.Text(dialog_title),
            content=ft.Text(dialog_content),
            actions=[
                ft.TextButton("Yes", on_click=lambda e: close_dlg(True, e)),
                ft.TextButton("No", on_click=lambda e: close_dlg(False, e)),
            ],
            # アクションの水平方向のレイアウト
            actions_alignment=ft.MainAxisAlignment.END,
        )

        e.page.dialog = modal_dialog  # ダイアログをページにセット
        modal_dialog.open = True  # ダイアログを開く
        e.page.update()
