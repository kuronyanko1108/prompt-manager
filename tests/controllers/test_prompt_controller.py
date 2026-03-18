from src.controllers.prompt_controller import PromptController
from src.dto.prompt_dto import (
    PromptSummaryDTO,
    PromptDetailDTO,
    PromptUpdateDTO,
    PromptCreateDTO,
)


class FakeService:
    def __init__(self):
        self.create_called = False
        self.update_called = False

    def get_all_prompt(self):
        return [PromptSummaryDTO(id=1, title="A"), PromptSummaryDTO(id=2, title="B")]

    def get_prompt_by_id(self, prompt_id):
        if prompt_id == 999:
            return None
        else:
            return PromptDetailDTO(id=prompt_id, title="C", content="C本文")

    def create_prompt(self, prompt_dto):
        if isinstance(prompt_dto, PromptCreateDTO):
            self.create_called = True
            return 1

    def update_prompt(self, prompt_dto):
        if isinstance(prompt_dto, PromptUpdateDTO):
            self.update_called = True
            return 1

    def delete_prompt(self, prompt_id):
        if prompt_id == 6:
            return 1
        else:
            return 0


def test_get_prompt_list():
    controller = PromptController()
    controller.service = FakeService()

    result = controller.get_prompt_list()

    # 検証：get_prompt_list()がlist[PromptSummaryDTO]を返すこと
    assert isinstance(result[0], PromptSummaryDTO)
    assert result[0].id == 1
    assert result[0].title == "A"
    assert result[1].id == 2
    assert result[1].title == "B"


def test_get_prompt_by_id():
    controller = PromptController()
    controller.service = FakeService()

    prompt_id = 3
    result = controller.get_prompt_by_id(prompt_id)

    # 検証： get_prompt_by_id()がPromptDetailDTOを返すこと
    assert isinstance(result, PromptDetailDTO)
    assert result.id == 3
    assert result.title == "C"
    assert result.content == "C本文"


def test_abnormal_get_prompt_by_id():
    controller = PromptController()
    controller.service = FakeService()

    prompt_id = 999
    result = controller.get_prompt_by_id(prompt_id)

    # 検証： get_prompt_by_id()がPromptDetailDTOを返すこと
    assert result is None


def test_save_prompt_to_create_prompt():
    controller = PromptController()
    fake = FakeService()
    controller.service = fake

    prompt_dto = PromptCreateDTO(title="D", content="D本文")
    result = controller.save_prompt(prompt_dto)

    # 検証： save_prompt()がcreate_prompt()を呼ぶこと
    assert fake.create_called is True
    assert fake.update_called is False
    assert result == 1


def test_save_prompt_to_update_prompt():
    controller = PromptController()
    fake = FakeService()
    controller.service = fake
    prompt_dto = PromptUpdateDTO(id=4, title="E", content="E本文")
    result = controller.save_prompt(prompt_dto)

    # 検証： save_prompt()がupdate_prompt()を呼ぶこと
    assert fake.update_called is True
    assert fake.create_called is False
    assert result == 1


def test_delete_prompt():
    controller = PromptController()
    controller.service = FakeService()

    prompt_id = 6
    result = controller.delete_prompt(prompt_id)

    # 検証： delete_prompt()がservice.delete_prompt()を呼ぶこと
    assert result == 1


def test_abnormal_delete_prompt():
    controller = PromptController()
    controller.service = FakeService()

    prompt_id = 999
    result = controller.delete_prompt(prompt_id)

    # 検証： get_prompt_by_id()がdelete_prompt()を呼ぶこと
    assert result == 0
