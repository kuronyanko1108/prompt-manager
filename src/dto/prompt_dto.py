from dataclasses import dataclass


@dataclass(frozen=True)
class PromptSummaryDTO:
    """一覧表示用DTO"""

    title: str
    id: int


@dataclass(frozen=True)
class PromptDetailDTO:
    """詳細表示用DTO"""

    title: str
    content: str
    id: int


@dataclass(frozen=True)
class PromptCreateDTO:
    """新規作成入力用DTO"""

    title: str
    content: str


@dataclass(frozen=True)
class PromptUpdateDTO:
    """更新入力用DTO"""

    title: str
    content: str
    id: int
