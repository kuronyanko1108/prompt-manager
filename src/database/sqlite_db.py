from pathlib import Path
import sqlite3


class Database:
    def __init__(self, db_path=None):
        # データベースファイルのパスを定義
        if db_path:
            self.DB_PATH = Path(db_path)
        else:
            # region 解説
            # __file__: 自身のフルパス　/home/sakan/dev/prompt_manager/src/database/db_manager.py
            # .resolve(): 「絶対パス」に変換
            # .parents[2]: 現在の階層から[]に記述された階層の下まで遡る。/home/sakan/dev/prompt_manager/
            # endregion
            self.DB_PATH = (
                Path(__file__).resolve().parents[2] / "data" / "prompt_manager.db"
            )

    def connect(self) -> sqlite3.Connection:
        # 1. データベースに接続（存在しない場合は新規作成）
        connection = sqlite3.connect(self.DB_PATH)

        # region 解説
        # row_factory: クエリの結果をどのような形式で返すかを指定
        # sqlite3.Row: クエリの結果を辞書のようにアクセスできる形式で返す
        # endregion
        connection.row_factory = sqlite3.Row
        return connection

    # 4. 変更を確定（コミット）して閉じる
    def fetch_all(self, sql, params=None):
        # region 解説
        # with構文: ブロックを抜けると自動的にリソースを解放 **connection.close()**が自動的に呼び出される
        # endregion
        with self.connect() as connection:
            return connection.execute(sql, params or ()).fetchall()

    def fetch_one(self, sql, params=None):
        with self.connect() as connection:
            return connection.execute(sql, params or ()).fetchone()

    def execute(self, sql, params=None):
        with self.connect() as connection:
            cursor = connection.execute(sql, params or ())
            # with connectionは、Python の sqlite3 では自動コミットするためcommit省略
            return cursor.rowcount
