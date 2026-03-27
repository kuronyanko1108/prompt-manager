from abc import ABC, abstractmethod
from ..dto.prompt_dto import (
    PromptSummaryDTO,
    PromptDetailDTO,
    PromptCreateDTO,
    PromptUpdateDTO,
)
from typing import List


class IPromptService(ABC):

    @abstractmethod
    def get_prompt_by_id(self, prompt_id: int) -> PromptDetailDTO | None:
        pass

    @abstractmethod
    def get_all_prompt(self) -> List[PromptSummaryDTO]:
        pass

    @abstractmethod
    def create_prompt(self, prompt_dto: PromptCreateDTO) -> tuple[int, list[str]]:
        pass

    @abstractmethod
    def update_prompt(self, prompt_dto: PromptUpdateDTO) -> tuple[int, list[str]]:
        pass

    @abstractmethod
    def delete_prompt(self, prompt_id: int) -> int:
        pass
