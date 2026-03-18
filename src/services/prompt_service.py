from ..mappers.prompt_mapper import PromptDTOMapper
from ..repositories.sqlite_prompt_repository import SQLitePromptRepository
from ..dto.prompt_dto import (
    PromptSummaryDTO,
    PromptDetailDTO,
    PromptCreateDTO,
    PromptUpdateDTO,
)


class PromptService:
    def __init__(self):
        self.repository = SQLitePromptRepository()

    def get_all_prompt(self) -> list[PromptSummaryDTO]:
        """プロンプトを一括取得"""
        prompts = self.repository.find_all()
        return [PromptDTOMapper.entity_to_summary_dto(prompt) for prompt in prompts]

    def get_prompt_by_id(self, prompt_id: int) -> PromptDetailDTO | None:
        """idから対象のプロンプトを取得"""
        prompt = self.repository.find_by_id(prompt_id)
        return PromptDTOMapper.entity_to_detail_dto(prompt)

    def create_prompt(self, prompt_dto: PromptCreateDTO) -> int:
        """プロンプトの新規で登録"""
        prompt = PromptDTOMapper.create_dto_to_entity(prompt_dto)
        return self.repository.create(prompt)

    def update_prompt(self, prompt_dto: PromptUpdateDTO) -> int:
        """プロンプトの変更内容を更新"""
        prompt = PromptDTOMapper.update_dto_to_entity(prompt_dto)
        return self.repository.update(prompt)

    def delete_prompt(self, prompt_id: int) -> int:
        """プロンプトを削除"""
        return self.repository.delete(prompt_id)
