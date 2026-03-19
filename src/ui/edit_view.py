from ..controllers.prompt_controller import PromptController
from ..dto.prompt_dto import PromptUpdateDTO
import flet as ft

VALIDATION_ERROR = -1
ERROR = 0
SUCCESS = 1


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

        if result == VALIDATION_ERROR:
            self.snack_bar(errors[0], e)
        elif result == ERROR:
            self.snack_bar("保存に失敗しました", e)
        elif result == SUCCESS:
            self.snack_bar("保存しました。", e)

    def on_copy_clicked(self):
        pass

    def on_delete_clicked(self, e):
        result = self.controller.delete_prompt(self.prompt_id)

        if result == 1:
            self.snack_bar("削除しました", e)
            e.page.go("/prompt_list")
        else:
            self.snack_bar("削除に失敗しました", e)

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
