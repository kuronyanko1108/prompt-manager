from pathlib import Path
import pytest
from src.repositories.sqlite_prompt_repository import SQLitePromptRepository


@pytest.fixture
# tmp_path テスト用の一時フォルダ、テスト終了するとpytest側でクリーンにする
def repo(tmp_path: Path):
    # テスト用のDBファイル名を決める
    test_db = tmp_path / "test_prompt_manager.db"

    # リポジトリのインスタンス作成（Databaseクラスがパスを受け取れる想定）
    test_repository = SQLitePromptRepository(db_path=test_db)
    # テスト用のテーブルの作成
    test_repository.init_db()

    yield test_repository
