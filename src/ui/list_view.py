from ..controllers.prompt_controller import PromptController


class PromptListView:
    def __init__(self):
        self.controller = PromptController()

    def show_list(self):
        return self.controller.get_prompt_list()

    def on_copy_clicked(self):
        pass

    def open_edit_view(self, prompt_id):
        return self.controller.get_prompt_by_id(prompt_id)
