import sqlite3
from src.models.prompt import Prompt
from src.dto.prompt_dto import (
    PromptSummaryDTO,
    PromptDetailDTO,
    PromptCreateDTO,
    PromptUpdateDTO,
)


class PromptRowMapper:
    @staticmethod
    def to_entity(row: sqlite3.Row | None) -> Prompt | None:
        """DBの生データからエンティティに変換"""
        if row is None:
            return None

        return Prompt(
            id=row["id"],
            title=row["title"],
            content=row["content"],
            is_deleted=row["is_deleted"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )


class PromptDTOMapper:
    @staticmethod
    def entity_to_summary_dto(entity: Prompt) -> PromptSummaryDTO:
        """エンティティから一覧表示用DTOに変換"""
        if entity.id is None:
            raise ValueError("idが設定されていません")

        return PromptSummaryDTO(
            id=entity.id,
            title=entity.title,
            content=entity.content,
        )

    @staticmethod
    def entity_to_detail_dto(entity: Prompt | None) -> PromptDetailDTO | None:
        """エンティティから詳細表示用DTOに変換"""
        if entity is None:
            return None

        if entity.id is None:
            raise ValueError("idが設定されていません")

        return PromptDetailDTO(
            id=entity.id,
            title=entity.title,
            content=entity.content,
        )

    @staticmethod
    def create_dto_to_entity(prompt_dto: PromptCreateDTO) -> Prompt:
        """新規作成入力用DTOからエンティティに変換"""
        return Prompt(
            id=None,
            title=prompt_dto.title,
            content=prompt_dto.content,
        )

    @staticmethod
    def update_dto_to_entity(prompt_dto: PromptUpdateDTO) -> Prompt:
        """更新入力用DTOからエンティティに変換"""
        return Prompt(
            id=prompt_dto.id,
            title=prompt_dto.title,
            content=prompt_dto.content,
        )
