from dataclasses import dataclass


@dataclass
class Prompt:
    title: str
    content: str
    id: int | None = None
    is_deleted: int = 0
    created_at: str | None = None
    updated_at: str | None = None
