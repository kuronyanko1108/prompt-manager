from ..controllers.prompt_controller import PromptController
from ..dto.prompt_dto import PromptSummaryDTO
from ..ui.components.prompt_snack_bar_UI import PromptSnackBarUI


class PromptListView:
    def __init__(self):
        self.controller = PromptController()

    def show_list(self):
        return self.controller.get_prompt_list()

    def on_copy_clicked(self, prompt: PromptSummaryDTO, e):
        row = self.controller.get_prompt_by_id(prompt.id)
        # クリップボードにコピー
        e.page.set_clipboard(row.content)
        # コピー完了をユーザーに知らせる（スナックバー）
        PromptSnackBarUI.show_snack_bar(e.page, "プロンプトをコピーしました！")

    def open_edit_view(self, prompt_id):
        return self.controller.get_prompt_by_id(prompt_id)
