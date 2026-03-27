from datetime import datetime
from ..database.sqlite_db import Database
from ..mappers.prompt_mapper import PromptRowMapper
from ..interfaces.i_prompt_repository import IPromptRepository
from ..models.prompt import Prompt
from typing import List


class SQLitePromptRepository(IPromptRepository):
    def __init__(self, db_path=None):
        self.database = Database(db_path)

    def init_db(self):
        """テーブルの初期化を行う。"""
        create_prompts_table_sql = """    
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                is_deleted INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        self.database.execute(create_prompts_table_sql)

    def find_all(self) -> List[Prompt]:
        """削除されていないすべてのプロンプトを全件取得する。"""
        select_all_sql = "SELECT * FROM prompts WHERE is_deleted = 0;"
        rows = self.database.fetch_all(select_all_sql)
        return [
            entity
            for row in rows
            if (entity := PromptRowMapper.to_entity(row)) is not None
        ]

    def find_by_id(self, prompt_id) -> Prompt | None:
        """指定されたidから対象のプロンプト1件取得する"""
        select_sql = "SELECT * FROM prompts WHERE id = ? AND is_deleted = 0;"
        data = (prompt_id,)
        row = self.database.fetch_one(select_sql, data)
        return PromptRowMapper.to_entity(row)

    def create(self, prompt) -> int:
        """新しいプロンプトをデータベースに保存する。"""
        insert_sql = """
        INSERT INTO prompts (
            title, 
            content, 
            created_at, 
            updated_at
        )
        VALUES (?,?,?,?);
        """
        now = self.get_now_time()
        data = (prompt.title, prompt.content, now, now)

        return self.database.execute(insert_sql, data)

    def update(self, prompt) -> int:
        """既存のプロンプトの内容を更新する。"""
        update_sql = "UPDATE prompts SET title = ?, content = ?, updated_at = ? WHERE id = ? AND is_deleted = 0"
        data = (prompt.title, prompt.content, self.get_now_time(), prompt.id)

        return self.database.execute(update_sql, data)

    def delete(self, prompt_id) -> int:
        """プロンプトを論理削除（削除フラグを1に更新）する。"""
        delete_sql = "UPDATE prompts SET is_deleted = 1, updated_at = ? WHERE id = ? "
        data = (self.get_now_time(), prompt_id)
        return self.database.execute(delete_sql, data)

    def get_now_time(self) -> str:
        """現在時刻をISOフォーマットの文字列で取得する。"""
        return datetime.now().isoformat()
