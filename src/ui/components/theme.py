import flet as ft


class Color:
    """アイコン"""

    # アイコンの基本表示色
    DEFAULT_ICON_COLOR = ft.Colors.BLUE_400
    # 戻る・編集の基本色
    NAV_ICON_COLOR = ft.Colors.BROWN_100
    # 破壊操作系アイコン色
    DANGER_ICON_COLOR = ft.Colors.PINK_500

    """操作系"""

    # 正常動作
    NORMAL_OPERATION_COLOR = ft.Colors.TEAL_500
    # 破壊操作系アイコン色
    DANGER_OPERATION_COLOR = ft.Colors.PINK_500

    """入力項目"""

    # 入力欄
    INPUT_BOX_COLOR = ft.Colors.WHITE
    # 一覧リスト
    PROMPT_LIST_FRAME_COLOR = ft.Colors.BROWN_900
    # 選択されたときの色
    SELECT_COLOR = ft.Colors.LIGHT_BLUE_ACCENT_200

    """文字"""
    # 基本の文字色
    BASE_FONT_COLOR = ft.Colors.WHITE
    TITLE_COLOR = ft.Colors.BLUE_400


class IconSize:
    # アイコンの基本サイズ
    DEFAULT_ICON_SIZE = 30
    # 少し小さめのサイズ
    LITTLE_ICON_SIZE = 20


class FontSize:
    # タイトルの文字サイズ
    TITLE_FONT_SIZE = 28
    # 入力欄の文字サイズ
    INPUT_TEXT_FONT_SIZE = 16


class LayoutSize:
    # 区切り線の間隔
    DIVIDER_SMALL = 5
    DIVIDER_LARGE = 10

    # 余白をつけるためのコンテナの横幅
    MARGIN_CONTAINER_WIDTH = 10
    # コンテナの高さ
    CONTAINER_HEIGHT = 12
    # 枠線の幅
    FRAME_THICKNESS = 2


class Timing:
    # ハイライトの表示時間
    HIGHLIGHT_ANIMATION_TIME = 0.5
    # スナックバーの表示時間
    SNACKBAR_DURATION = 2000


class CharLimit:
    # タイトルの最大文字数
    TITLE_MAX_LENGTH = 100
    # サブタイトルの最大文字数
    SUBTITLE_MAX_LENGTH = 50
    # 本文の最大文字数
    CONTENT_MAX_LENGTH = 10000
    # 本文入力欄の最小行数
    INPUT_CONTENT_MIN_LINE = 15
    # 本文入力欄の高さ
    INPUT_CONTENT_HEIGHT = 400


class DrawerIndex:
    # 新規作成画面
    CREATE = 0
