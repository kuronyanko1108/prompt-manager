from src.models.prompt import Prompt


def test_create(repo):
    new_p = Prompt("テストタイトル", "テスト内容")
    count = repo.create(new_p)
    rows = repo.find_all()
    # 検証：repo.create(...) の戻り値が 1
    assert count == 1
    # 検証：repo.find_all() の件数が 1 増える
    assert len(rows) == 1
    # 検証：title,contentの内容が一致する
    assert rows[0].title == "テストタイトル"
    assert rows[0].content == "テスト内容"


def test_find_by_id(repo):
    new_p = Prompt("テストタイトル２", "テスト内容２")
    repo.create(new_p)
    last_row = repo.find_all()[-1]
    target_id = last_row.id

    result = repo.find_by_id(target_id)

    # 検証：返り値が None ではない
    assert result is not None
    # 検証：title, content が一致する
    assert result.title == "テストタイトル２"
    assert result.content == "テスト内容２"


def test_update(repo):
    new_p = Prompt("テストタイトル３", "テスト内容３")
    repo.create(new_p)
    last_row = repo.find_all()[-1]
    target_id = last_row.id

    new_p.id = target_id
    new_p.title = "テストタイトル３変更"
    new_p.content = "テスト内容３変更"

    result = repo.update(new_p)
    result_row = repo.find_by_id(target_id)

    # 検証：updateの戻り値が１
    assert result == 1
    # 検証：title, content が変更されている
    assert result_row.title == "テストタイトル３変更"
    assert result_row.content == "テスト内容３変更"


def test_delete(repo):
    new_p = Prompt("テストタイトル４", "テスト内容４")
    repo.create(new_p)
    last_row = repo.find_all()[-1]
    target_id = last_row.id

    result = repo.delete(target_id)
    # 検証：deleteの戻り値が１
    assert result == 1

    result_row = repo.find_by_id(target_id)
    # 検証：が 削除後のfind_by_id()がNone になる
    assert result_row is None

    rows = repo.find_all()
    # 検証：find_all は削除されていないデータだけ返す
    assert len(rows) == 0


def test_find_all(repo):
    new_p = [
        Prompt("テストタイトル５－１", "テスト内容５－１"),
        Prompt("テストタイトル５－２", "テスト内容５－２"),
    ]

    for x in new_p:
        repo.create(x)

    delete_target = repo.find_all()[-1]
    repo.delete(delete_target.id)

    result = repo.find_all()
    # 検証：find_all() の件数が期待どおりになる
    assert len(result) == 1

    target_id = result[-1].id
    result_row = repo.find_by_id(target_id)
    # 検証：残っているレコードが正しい
    assert result_row.title == "テストタイトル５－１"
    assert result_row.content == "テスト内容５－１"
