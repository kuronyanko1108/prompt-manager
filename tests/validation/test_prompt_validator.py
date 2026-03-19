from src.validation.prompt_validator import PromptValidator


# ===== 新規作成バリデーション =====
validator = PromptValidator()


def test_valid_create():
    # 正常: タイトル・本文ともに有効
    errors = validator.validate_create("タイトル", "本文")
    assert errors == []


def test_create_title_empty():
    # 異常: タイトルが空文字
    errors = validator.validate_create("", "本文")
    assert "タイトルは必須です" in errors


def test_create_title_whitespace_only():
    # 異常: タイトルが空白のみ（trim後に空になる）
    errors = validator.validate_create("   ", "本文")
    assert "タイトルは必須です" in errors


def test_create_title_too_long():
    # 異常: タイトルが100文字超
    errors = validator.validate_create("a" * 101, "本文")
    assert "タイトルは100文字以内で入力してください" in errors


def test_create_title_max_length():
    # 正常: タイトルがちょうど100文字
    errors = validator.validate_create("a" * 100, "本文")
    assert errors == []


def test_create_content_empty():
    # 異常: 本文が空文字
    errors = validator.validate_create("タイトル", "")
    assert "本文は必須です" in errors


def test_create_content_whitespace_only():
    # 異常: 本文が空白のみ（trim後に空になる）
    errors = validator.validate_create("タイトル", "\n\t  ")
    assert "本文は必須です" in errors


def test_create_content_too_long():
    # 異常: 本文が10000文字超
    errors = validator.validate_create("タイトル", "a" * 10001)
    assert "本文は10000文字以内で入力してください" in errors


def test_create_content_max_length():
    # 正常: 本文がちょうど10000文字
    errors = validator.validate_create("タイトル", "a" * 10000)
    assert errors == []


def test_create_multiple_errors():
    # 異常: タイトル・本文ともにエラー（全件検出）
    errors = validator.validate_create("", "")
    assert len(errors) == 2


# ===== 更新バリデーション =====


def test_valid_update():
    # 正常: id・タイトル・本文ともに有効
    errors = validator.validate_update(1, "タイトル", "本文")
    assert errors == []


def test_update_id_none():
    # 異常: idがNone
    errors = validator.validate_update(None, "タイトル", "本文")
    assert "IDは必須です" in errors


def test_update_id_zero():
    # 異常: idが0（1以上必須）
    errors = validator.validate_update(0, "タイトル", "本文")
    assert "IDは1以上である必要があります" in errors


def test_update_id_negative():
    # 異常: idが負の数
    errors = validator.validate_update(-1, "タイトル", "本文")
    assert "IDは1以上である必要があります" in errors


def test_update_id_string():
    # 異常: idが文字列
    errors = validator.validate_update("a", "タイトル", "本文")
    assert "IDは数値である必要があります" in errors
