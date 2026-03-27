from abc import ABC, abstractmethod
from ..models.prompt import Prompt
from typing import List


class IPromptRepository(ABC):
    @abstractmethod
    def find_by_id(self, prompt_id: int) -> Prompt | None:
        pass

    @abstractmethod
    def find_all(self) -> List[Prompt]:
        pass

    @abstractmethod
    def create(self, prompt: Prompt) -> int:
        pass

    @abstractmethod
    def update(self, prompt: Prompt) -> int:
        pass

    @abstractmethod
    def delete(self, prompt_id: int) -> int:
        pass
