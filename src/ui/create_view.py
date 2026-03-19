from ..controllers.prompt_controller import PromptController
from ..dto.prompt_dto import PromptCreateDTO
from ..constants.result_code import ResultCode
import flet as ft


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
            self.snack_bar(errors[0], e)

        elif result == ResultCode.ERROR:
            self.snack_bar("保存に失敗しました", e)

        elif result == ResultCode.SUCCESS:
            self.snack_bar("保存しました。", e)
            e.page.go("/prompt_list")

    def on_back_clicked(self):
        pass

    def snack_bar(self, comment, e):
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
