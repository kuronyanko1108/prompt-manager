from ..controllers.prompt_controller import PromptController
from ..dto.prompt_dto import PromptUpdateDTO
from ..constants.result_code import ResultCode
from ..ui.components.prompt_confirm_UI import PromptConfirmUI
from ..ui.components.prompt_snack_bar_UI import PromptSnackBarUI


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
            PromptSnackBarUI.show_snack_bar(e.page, errors[0])

        elif result == ResultCode.ERROR:
            PromptSnackBarUI.show_snack_bar(e.page, "保存に失敗しました")

        elif result == ResultCode.SUCCESS:
            PromptSnackBarUI.show_snack_bar(e.page, "保存しました。")

    def on_copy_clicked(self, content_input, e):
        # クリップボードにコピー
        e.page.set_clipboard(content_input.value)
        # コピー完了をユーザーに知らせる（スナックバー）
        PromptSnackBarUI.show_snack_bar(e.page, "プロンプトをコピーしました！")

    def on_delete_clicked(self, e):
        PromptConfirmUI.show_confirm_dialog(
            e.page,
            "確認",
            "削除しますか？\nこの操作は取り消しできません",
            lambda current_page: self.execute_delete(current_page),
        )

    def execute_delete(self, current_page):

        result = self.controller.delete_prompt(self.prompt_id)

        if result == ResultCode.ERROR:
            PromptSnackBarUI.show_snack_bar(current_page, "削除に失敗しました")

        elif result == ResultCode.SUCCESS:
            PromptSnackBarUI.show_snack_bar(current_page, "削除しました")
            current_page.go("/prompt_list")

    def on_back_clicked(self, title_input, content_input, e):
        prompt_data = self.controller.get_prompt_by_id(self.prompt_id)

        if prompt_data is None:
            PromptSnackBarUI.show_snack_bar(e.page, "変更対象がありません")
            e.page.go("/prompt_list")
            return

        # 変更がある場合は、確認ダイアログを表示する
        if (prompt_data.title != title_input.value) or (
            prompt_data.content != content_input.value
        ):
            PromptConfirmUI.show_confirm_dialog(
                e.page,
                "確認",
                "内容が変更されています。\n内容を保存せずに戻りますか？",
                on_yes_action=lambda page: page.go("/prompt_list"),
            )
        else:
            e.page.go("/prompt_list")
