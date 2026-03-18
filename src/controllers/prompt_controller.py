from ..services.prompt_service import PromptService
from ..dto.prompt_dto import (
    PromptSummaryDTO,
    PromptDetailDTO,
    PromptCreateDTO,
    PromptUpdateDTO,
)


class PromptController:
    def __init__(self):
        self.service = PromptService()

    def get_prompt_list(self) -> list[PromptSummaryDTO]:
        """サービス層からプロンプトの一覧を取得"""
        return self.service.get_all_prompt()

    def get_prompt_by_id(self, prompt_id: int) -> PromptDetailDTO | None:
        """idに紐づくプロンプトを取得する"""
        return self.service.get_prompt_by_id(prompt_id)

    def save_prompt(self, prompt_dto: PromptCreateDTO | PromptUpdateDTO) -> int:
        """プロンプトの新規登録／更新処理を行う"""

        # 引数の型に応じて新規登録か更新処理を決める
        if isinstance(prompt_dto, PromptCreateDTO):
            return self.service.create_prompt(prompt_dto)
        else:
            return self.service.update_prompt(prompt_dto)

    def delete_prompt(self, prompt_id: int) -> int:
        """プロンプトの削除を行う"""
        return self.service.delete_prompt(prompt_id)
