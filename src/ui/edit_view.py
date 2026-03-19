from ..controllers.prompt_controller import PromptController
from ..dto.prompt_dto import PromptUpdateDTO
from ..constants.result_code import ResultCode
from ..ui.components.prompt_confirm_UI import PromptConfirmUI
import flet as ft


class PromptEditView:
    def __init__(self, prompt_id: int):
        self.controller = PromptController()
        self.prompt_id = prompt_id

    def on_save_clicked(self, input_title, input_content, e):

        prompt_dto = PromptUpdateDTO(
            id=self.prompt_id,
            title=input_title.value,
            content=input_content.value,
        )
        result, errors = self.controller.save_prompt(prompt_dto)

        if result == ResultCode.VALIDATION_ERROR:
            self.show_snack_bar(errors[0], e)

        elif result == ResultCode.ERROR:
            self.show_snack_bar("保存に失敗しました", e)

        elif result == ResultCode.SUCCESS:
            self.show_snack_bar("保存しました。", e)

    def on_copy_clicked(self):
        pass

    def on_delete_clicked(self, e):
        PromptConfirmUI.show_confirm_dialog(
            e,
            "内容が変更されています",
            "削除しますか？",
            lambda e: self.execute_delete(e),
        )

    def execute_delete(self, e):

        result = self.controller.delete_prompt(self.prompt_id)

        if result == ResultCode.ERROR:
            self.show_snack_bar("削除に失敗しました", e)

        elif result == ResultCode.SUCCESS:
            self.show_snack_bar("削除しました", e)
            e.page.go("/prompt_list")

    def on_back_clicked(self, title_input, content_input, e):
        prompt_data = self.controller.get_prompt_by_id(self.prompt_id)

        if prompt_data is None:
            self.show_snack_bar("変更対象がありません", e)
            e.page.go("/prompt_list")
            return

        # 変更がある場合は、確認ダイアログを表示する
        if (prompt_data.title != title_input.value) or (
            prompt_data.content != content_input.value
        ):
            PromptConfirmUI.show_confirm_dialog(
                e,
                "内容が変更されています",
                "内容を保存せずに戻りますか？",
                on_yes_action=lambda e: e.page.go("/prompt_list"),
            )
        else:
            e.page.go("/prompt_list")

    def show_snack_bar(self, comment, e):
        # 1. SnackBarのインスタンスを作る
        snack_bar = ft.SnackBar(
            content=ft.Text(comment),
            duration=2000,
        )
        # 2. 現在のページ(e.page)の属性にセットする
        e.page.snack_bar = snack_bar
        # 3. オープンフラグを立てる
        e.page.snack_bar.open = True
        # 4. ページを更新して反映させる
        e.page.update()
