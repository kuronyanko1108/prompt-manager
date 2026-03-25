from ...controllers.prompt_controller import PromptController
from ...dto.prompt_dto import PromptCreateDTO
from ...constants.result_code import ResultCode
from ..components.prompt_confirm_ui import PromptConfirmUI
from ..components.prompt_snack_bar_ui import PromptSnackBarUi
import asyncio


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
            PromptSnackBarUi.show_error_snack_bar(e.page, errors[0])

        elif result == ResultCode.ERROR:
            PromptSnackBarUi.show_error_snack_bar(e.page, "保存に失敗しました")

        elif result == ResultCode.SUCCESS:
            PromptSnackBarUi.show_success_snack_bar(e.page, "保存しました")
            asyncio.create_task(e.page.push_route("/"))

    def on_back_clicked(self, title_input, content_input, e):

        if title_input.value or content_input.value:
            PromptConfirmUI.show_confirm_dialog(
                e.page,
                "確認",
                "記入されています。\n保存せずに戻りますか？",
                on_yes_action=lambda page: asyncio.create_task(page.push_route("/")),
            )
        else:
            asyncio.create_task(e.page.push_route("/"))
