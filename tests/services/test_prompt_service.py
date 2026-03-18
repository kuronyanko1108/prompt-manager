from src.models.prompt import Prompt
from src.services.prompt_service import PromptService
from src.dto.prompt_dto import (
    PromptSummaryDTO,
    PromptDetailDTO,
    PromptUpdateDTO,
    PromptCreateDTO,
)


class FakeRepository:
    def __init__(self):
        self.last_created_prompt = None
        self.last_updated_prompt = None

    def find_all(self):
        return [
            Prompt(id=1, title="A", content="A本文"),
            Prompt(id=2, title="B", content="B本文"),
        ]

    def find_by_id(self, prompt_id):
        if prompt_id == 4:
            return None

        return Prompt(
            id=prompt_id,
            title="C",
            content="C本文",
        )

    def create(self, prompt):
        if prompt.title == "D" and prompt.content == "D本文":
            self.last_created_prompt = prompt
            return 1
        else:
            return 0

    def update(self, prompt):
        if prompt.title == "E更新" and prompt.content == "E本文更新":
            self.last_updated_prompt = prompt
            return 1
        else:
            return 0

    def delete(self, prompt_id):
        if prompt_id == 5:
            return 1
        else:
            return 0


def test_get_all_prompt():
    service = PromptService()
    service.repository = FakeRepository()

    result = service.get_all_prompt()

    # 検証：件数が一致すること
    assert len(result) == 2
    # 検証：get_all_prompt が list[PromptSummaryDTO] を返す
    assert isinstance(result[0], PromptSummaryDTO)
    # 検証：repository.find_all() の結果がDTOに変換される
    assert result[0].id == 1
    assert result[0].title == "A"
    assert result[1].id == 2
    assert result[1].title == "B"


def test_normal_get_prompt_by_id():
    service = PromptService()
    service.repository = FakeRepository()
    prompt_id = 3
    result = service.get_prompt_by_id(prompt_id)

    # 検証：  PromptDetailDTOのid/title/content が一致する
    assert result.id == prompt_id
    assert result.title == "C"
    assert result.content == "C本文"
    # 検証： get_prompt_by_idがPromptDetailDTOを返すこと
    assert isinstance(result, PromptDetailDTO)


def test_abnormal_get_prompt_by_id():
    service = PromptService()
    service.repository = FakeRepository()
    prompt_id = 4
    result = service.get_prompt_by_id(prompt_id)

    # 検証： repository.find_by_id(id) が None のとき、戻り値も None
    assert result is None


def test_create_prompt():
    service = PromptService()
    fake_repo = FakeRepository()
    service.repository = fake_repo
    prompt_dto = PromptCreateDTO(title="D", content="D本文")

    result = service.create_prompt(prompt_dto)
    # 確認： 戻り値をそのまま返す
    assert result == 1
    assert fake_repo.last_created_prompt.id is None
    assert fake_repo.last_created_prompt.title == "D"
    assert fake_repo.last_created_prompt.content == "D本文"


def test_update_prompt():
    service = PromptService()
    fake_repo = FakeRepository()
    service.repository = fake_repo
    prompt_dto = PromptUpdateDTO(title="E更新", content="E本文更新", id=5)

    result = service.update_prompt(prompt_dto)
    # 確認： 戻り値をそのまま返す
    assert result == 1
    # 確認： id/title/content正しくわたり 更新されていること
    assert fake_repo.last_updated_prompt is not None
    assert fake_repo.last_updated_prompt.id == 5
    assert fake_repo.last_updated_prompt.title == "E更新"
    assert fake_repo.last_updated_prompt.content == "E本文更新"


def test_delete_prompt():
    service = PromptService()
    service.repository = FakeRepository()
    prompt_id = 5
    result = service.delete_prompt(prompt_id)

    # 確認： 戻り値をそのまま返す
    assert result == 1


def test_abnormal_delete_prompt():
    service = PromptService()
    service.repository = FakeRepository()
    prompt_id = 999
    result = service.delete_prompt(prompt_id)

    # 確認： 戻り値をそのまま返す
    assert result == 0
