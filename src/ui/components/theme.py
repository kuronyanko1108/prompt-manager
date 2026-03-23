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
    PROMPT_LIST_COLOR = ft.Colors.BROWN_900
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
