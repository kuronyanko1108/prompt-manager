# フォルダ構成仕様書

# 1. 目的

本ドキュメントは、本アプリケーションのフォルダ構成と各ディレクトリの責務を定義する。  
開発時にコードの配置ルールを統一し、可読性と保守性を高めることを目的とする。

---

# 2. プロジェクト構成

```
prompt_manager/
├── main.py                         # アプリケーション起動エントリーポイント
├── requirements.txt                # 依存ライブラリ
├── README.md                       # プロジェクト説明
│
├── assets/                         # 画像・アイコンなど静的ファイル
│
├── config/                         # アプリケーション設定
│   └── logging_config.py           # logging設定
│
├── logs/                           # ログ出力ディレクトリ（Git管理対象外）
│   └── app.log
│
│
├── docs/                           # 設計書
│   ├── 01_requirements.md
│   ├── 02_usecase_diagram.md
│   ├── 03_screen_transition_diagram.md
│   ├── 04_ER_diagram.md
│   ├── 05_class_diagram.md
│   ├── 06_sequence_diagram.md
│   ├── 07_system_architecture.md
│   └── 08_folder_structure.md
│
├── src/                            # アプリケーション本体
│   │
│   ├── exceptions/                 # カスタム例外
│   │   ├── app_exception.py
│   │   ├── database_exception.py
│   │   └── prompt_exception.py
│   │
│   ├── validation/                 # 入力チェック
│   │   └── prompt_validator.py
│   │
│   ├── database/                   # DB接続管理
│   │   └── sqlite_db.py
│   │
│   ├── models/                     # Entity（DBデータ構造）
│   │   └── prompt.py
│   │
│   ├── dto/                        # DTO（データ転送オブジェクト）
│   │   └── prompt_dto.py
│   │
│   ├── mappers/                    # Entity ⇄ DTO 変換
│   │   └── prompt_mapper.py
│   │
│   ├── repositories/               # DBアクセス層
│   │   ├── base_repository.py
│   │   └── sqlite_prompt_repository.py
│   │
│   │
│   ├── services/                   # ビジネスロジック
│   │   └── prompt_service.py
│   │
│   ├── controllers/                # UIイベント制御
│   │   └── prompt_controller.py
│   │
│   ├── interfaces/                 # 抽象基底クラス
│   │   ├── i_prompt_repository.py
│   │   └── i_prompt_service.py
│   │
│   ├── ui/                         # Flet UI
│   │   ├── components/             # 共通UIコンポーネント
│   │   ├── list_view.py
│   │   ├── create_view.py
│   │   └── edit_view.py
│
└── tests/                          # テストコード
```

---

# 3. 各ディレクトリの役割

## main.py

アプリケーションのエントリーポイント。  
初期設定、ログ設定、UI起動などを行う。

---

## config/

アプリケーション設定ファイルを管理する。

例

```
config/
    logging_config.py
```

| ファイル          | 役割         |
| ----------------- | ------------ |
| logging_config.py | ログ出力設定 |

---

## logs/

ログファイルの出力先ディレクトリ。

例

```
logs/
    app.log
```

アプリケーションの実行ログを保存する。

※ Git管理対象外とする。

---

## exceptions/

アプリケーション共通のカスタム例外を定義する。

例

```
exceptions/
    app_exception.py
    database_exception.py
    prompt_exception.py
```

| ファイル              | 役割                     |
| --------------------- | ------------------------ |
| app_exception.py      | アプリケーション共通例外 |
| database_exception.py | データベース関連例外     |
| prompt_exception.py   | プロンプト操作例外       |

---

## validation/

空文字チェックや文字数制限などの入力チェックを定義する。

例

```
validation/
    prompt_validator.py
```

## database/

データベース接続管理を担当する。

例

```
database/
    sqlite_db.py
```

| 責務         |
| ------------ |
| DB接続管理   |
| DB初期化処理 |

---

## models/

データベーステーブルに対応するEntityを定義する。

例

```
models/
    prompt.py
```

| 種類   | 説明                       |
| ------ | -------------------------- |
| Entity | DBテーブル構造を表すモデル |

---

## dto/

データ転送用オブジェクトを定義する。

例

```
dto/
    prompt_dto.py
```

| 種類 | 説明                        |
| ---- | --------------------------- |
| DTO  | ServiceやUIで使用するデータ |

---

## mappers/

DBの生データをEntityに変換、
EntityとDTOの変換処理を担当する。

例

```
mappers/
    prompt_mapper.py
```

| 責務              |
| ----------------- |
| Row ⇄ Entity 変換 |
| Entity ⇄ DTO 変換 |

---

## repositories/

データベース操作を担当する。

例

```
repositories/
    sqlite_prompt_repository.py
```

| 責務       |
| ---------- |
| DBアクセス |
| CRUD処理   |

---

## services/

アプリケーションのビジネスロジックを実装する。

例

```
services/
    prompt_service.py
```

| 責務                     |
| ------------------------ |
| アプリケーションロジック |
| Repositoryの呼び出し     |

---

## controllers/

UIイベントを受け取り、Service層へ処理を依頼する。

例

```
controllers/
    prompt_controller.py
```

| 責務            |
| --------------- |
| UI操作の受付    |
| Service呼び出し |

---

## interfaces/

アプリケーションの各レイヤー間の規約（インターフェース）を定義する。
「何ができるか」を定義し、具体的な実装（どうやるか）とは分離させる。

例

```
interfaces/
    ├── i_prompt_service.py
    └── i_prompt_repository.py
```

| 責務                                                   |
| ------------------------------------------------------ |
| 責務メソッド名と引数・戻り値の定義（abc.ABCを使用）    |
| レイヤー間の結合度を下げ、実装の差し替えを容易にする   |
| 具象クラス（Service/Repository）が守るべきルールの提示 |

---

## ui/

画面表示およびUIコンポーネントを管理する。

例

```
ui/
    list_view.py
    create_view.py
    edit_view.py
```

| 責務             |
| ---------------- |
| 画面表示         |
| ユーザー入力受付 |

---

---

## docs/

設計書や仕様書を管理する。

---

## tests/

テストコードを管理する。

---

# 4. レイヤー構造

本アプリケーションは以下のレイヤー構造を採用する。

```
UI
↓
Controller
↓
Service
↓
Repository
↓
Database
```

| レイヤー   | 責務             |
| ---------- | ---------------- |
| UI         | 画面表示・入力   |
| Controller | UIイベント処理   |
| Service    | ビジネスロジック |
| Repository | DB操作           |
| Database   | DB接続           |

---

# 5. Git管理ルール

以下のファイルはGit管理対象外とする。

```
logs/
*.log
__pycache__/
```

---

# 6. 今後追加予定

### フェーズ2：検索・整理機能

- **タグ管理**: プロンプトの分類とタグによる絞り込み
- **キーワード検索**: タイトル・本文を対象とした全文検索
- **お気に入り**: よく使うプロンプトの固定表示（ピン留め）
- **日時表示**: 一覧画面での作成日・更新日の表示

### フェーズ3：高度な運用・連携

- **テンプレート変数**: プロンプト内の一部を動的に変更（例：`{{target}}`）
- **履歴管理**: 過去の更新内容の保存と復元

### フェーズ4：拡張機能

- **外部連携**: ショートカットキー等による呼び出し機能
  - 特定のショートカットキーでプロンプトを呼び出せるデスクトップ連携機能。
- **AI自動入力**: コピー時にChatGPT/Geminiの入力欄へ自動ペースト
