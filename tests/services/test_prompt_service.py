from src.models.prompt import Prompt
from src.services.prompt_service import PromptService
from src.dto.prompt_dto import (
    PromptSummaryDTO,
    PromptDetailDTO,
    PromptUpdateDTO,
    PromptCreateDTO,
)
from src.constants.result_code import ResultCode


class FakeRepository:
    def __init__(self):
        self.last_created_prompt = None
        self.last_updated_prompt = None
        self.create_call_count = 0
        self.update_call_count = 0

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
        self.create_call_count += 1
        if prompt.title == "D" and prompt.content == "D本文":
            self.last_created_prompt = prompt
            return 1
        else:
            return 0

    def update(self, prompt):
        self.update_call_count += 1
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

    result, message = service.create_prompt(prompt_dto)
    # 確認： 戻り値をそのまま返す
    assert result == ResultCode.SUCCESS
    assert not message
    assert fake_repo.last_created_prompt.id is None
    assert fake_repo.last_created_prompt.title == "D"
    assert fake_repo.last_created_prompt.content == "D本文"


def test_update_prompt():
    service = PromptService()
    fake_repo = FakeRepository()
    service.repository = fake_repo
    prompt_dto = PromptUpdateDTO(title="E更新", content="E本文更新", id=5)

    result, message = service.update_prompt(prompt_dto)
    # 確認： 戻り値をそのまま返す
    assert result == ResultCode.SUCCESS
    assert not message
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
    assert result == ResultCode.SUCCESS


def test_abnormal_delete_prompt():
    service = PromptService()
    service.repository = FakeRepository()
    prompt_id = 999
    result = service.delete_prompt(prompt_id)

    # 確認： 戻り値をそのまま返す
    assert result == ResultCode.ERROR


def test_create_prompt_validation_error_returns_zero_and_skips_repository():
    service = PromptService()
    fake_repo = FakeRepository()
    service.repository = fake_repo
    prompt_dto = PromptCreateDTO(title="   ", content="本文")

    result, message = service.create_prompt(prompt_dto)

    assert result == ResultCode.VALIDATION_ERROR
    assert fake_repo.create_call_count == 0
    assert message[0] == "タイトルは必須です"


def test_update_prompt_validation_error_returns_zero_and_skips_repository():
    service = PromptService()
    fake_repo = FakeRepository()
    service.repository = fake_repo
    prompt_dto = PromptUpdateDTO(title="更新", content="本文", id=0)

    result, message = service.update_prompt(prompt_dto)

    assert result == ResultCode.VALIDATION_ERROR
    assert message[0] == "IDは1以上である必要があります"
    assert fake_repo.update_call_count == 0


def test_update_prompt_not_found_returns_validation_error():

    service = PromptService()
    fake_repo = FakeRepository()
    service.repository = fake_repo
    prompt_dto = PromptUpdateDTO(title="X更新", content="X本文更新", id=4)

    result, message = service.update_prompt(prompt_dto)
    # 確認： 戻り値をそのまま返す
    assert result == ResultCode.VALIDATION_ERROR
    assert message[0] == "指定されたデータが存在しません"


def test_create_prompt_repository_error_returns_zero():
    service = PromptService()
    fake_repo = FakeRepository()
    service.repository = fake_repo
    prompt_dto = PromptCreateDTO(title="x", content="x本文")

    result, message = service.create_prompt(prompt_dto)
    # 確認： 戻り値をそのまま返す
    assert result == ResultCode.ERROR
    assert not message
