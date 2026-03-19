from ..mappers.prompt_mapper import PromptDTOMapper
from ..repositories.sqlite_prompt_repository import SQLitePromptRepository
from ..dto.prompt_dto import (
    PromptSummaryDTO,
    PromptDetailDTO,
    PromptCreateDTO,
    PromptUpdateDTO,
)
from ..validation.prompt_validator import PromptValidator
from ..constants.result_code import ResultCode


class PromptService:
    def __init__(self):
        self.repository = SQLitePromptRepository()
        self.validator = PromptValidator()

    def get_all_prompt(self) -> list[PromptSummaryDTO]:
        """プロンプトを一括取得"""
        prompts = self.repository.find_all()
        return [PromptDTOMapper.entity_to_summary_dto(prompt) for prompt in prompts]

    def get_prompt_by_id(self, prompt_id: int) -> PromptDetailDTO | None:
        """idから対象のプロンプトを取得"""
        prompt = self.repository.find_by_id(prompt_id)
        return PromptDTOMapper.entity_to_detail_dto(prompt)

    def create_prompt(self, prompt_dto: PromptCreateDTO) -> tuple[int, list[str]]:
        """プロンプトの新規で登録"""

        # バリデーションチェック
        errors = self.validator.validate_create(prompt_dto.title, prompt_dto.content)
        if errors:
            return ResultCode.VALIDATION_ERROR, errors

        prompt = PromptDTOMapper.create_dto_to_entity(prompt_dto)
        return self.repository.create(prompt), errors

    def update_prompt(self, prompt_dto: PromptUpdateDTO) -> tuple[int, list[str]]:
        """プロンプトの変更内容を更新"""
        # バリデーションチェック
        errors = self.validator.validate_update(
            prompt_dto.id, prompt_dto.title, prompt_dto.content
        )
        if errors:
            return ResultCode.VALIDATION_ERROR, errors

        if self.repository.find_by_id(prompt_dto.id) is None:
            errors = ["指定されたデータが存在しません"]
            return ResultCode.VALIDATION_ERROR, errors

        prompt = PromptDTOMapper.update_dto_to_entity(prompt_dto)
        return self.repository.update(prompt), errors

    def delete_prompt(self, prompt_id: int) -> int:
        """プロンプトを削除"""
        return self.repository.delete(prompt_id)
