from ..controllers.prompt_controller import PromptController
from ..dto.prompt_dto import PromptCreateDTO
from ..constants.result_code import ResultCode
from ..ui.components.prompt_confirm_UI import PromptConfirmUI
from ..ui.components.prompt_snack_bar_UI import PromptSnackBarUI


class PromptCreateView:
    def __init__(self):
        self.controller = PromptController()

    def on_save_clicked(self, input_title, input_content, e):
        prompt_dto = PromptCreateDTO(
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
            e.page.go("/prompt_list")

    def on_back_clicked(self, title_input, content_input, e):

        if title_input.value or content_input.value:
            PromptConfirmUI.show_confirm_dialog(
                e.page,
                "確認",
                "記入されています。\n保存せずに戻りますか？",
                on_yes_action=lambda page: page.go("/prompt_list"),
            )
        else:
            e.page.go("/prompt_list")
