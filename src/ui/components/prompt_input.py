import flet as ft
from .theme import Color, FontSize, CharLimit


class PromptInput:
    """プロンプト入力に関連する入力フィールドを作成するクラス"""

    @staticmethod
    def _create_base_input_box(
        value: str | None,
        label: str,
        hint_text: str,
        max_length: int,
        text_size: int = FontSize.INPUT_TEXT_FONT_SIZE,
        border_color: str = Color.INPUT_BOX_COLOR,
        focused_border_color: str = Color.SELECT_COLOR,
        **kwargs,
    ) -> ft.TextField:
        """
        TextFieldの基底メソッド。共通のスタイルや設定を適用します。

        Args:
            value (Optional[str]): 初期値。Noneの場合は空文字になります。
            label (str): 入力欄のラベルテキスト。
            hint_text (str): 未入力時に表示されるヒントテキスト。
            max_length (int): 入力可能な最大文字数。
            text_size (int): 入力テキストのフォントサイズ（デフォルトは16px）。
            border_color (str): 通常時の枠線の色（デフォルトは白色）。
            focused_border_color (str): フォーカス時の枠線の色(デフォルトは青色)。
            **kwargs: その他の ft.TextField に渡す任意の引数（multiline, autofocusなど）。

        Returns:
            ft.TextField: 設定済みのTextFieldインスタンス。
        """
        return ft.TextField(
            value=value or "",
            label=label,
            hint_text=hint_text,
            text_size=text_size,
            max_length=max_length,
            border_color=border_color,
            focused_border_color=focused_border_color,
            **kwargs,
        )

    @staticmethod
    def title_input_box(title_value: str | None) -> ft.TextField:
        """
        プロンプトのタイトル入力用の1行テキストフィールドを作成します。

        Args:
            title_value (Optional[str]): タイトルの初期値。

        Returns:
            ft.TextField: タイトル入力用のTextField。
        """
        return PromptInput._create_base_input_box(
            value=title_value,
            label="タイトル",
            hint_text="タイトルを記入してください",
            max_length=CharLimit.TITLE_MAX_LENGTH,
            autofocus=True,
        )

    @staticmethod
    def content_input_box(content_value: str | None) -> ft.TextField:
        """
        プロンプトの本文入力用の複数行テキストフィールドを作成します。

        Args:
            content_value (Optional[str]): 本文の初期値。

        Returns:
            ft.TextField: 本文入力用の多機能TextField。
        """
        return PromptInput._create_base_input_box(
            value=content_value,
            label="本文",
            hint_text="本文を入力してください",
            max_length=CharLimit.CONTENT_MAX_LENGTH,
            # 複数行
            multiline=True,
            # 最小行数
            min_lines=CharLimit.INPUT_CONTENT_MIN_LINE,
            # 高さ
            height=CharLimit.INPUT_CONTENT_HEIGHT,
            # シフトキーとエンターキーの有効
            shift_enter=True,
            expand=True,
        )
