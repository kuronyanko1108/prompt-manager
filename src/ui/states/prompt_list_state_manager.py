import flet as ft
from ..components.theme import Color, Timing
from ..utils.ui_utils import UiUtils
import asyncio


class PromptListStateManager:
    """
    PromptListStateManager: PromptListScreenの状態管理専用クラス
    """

    def __init__(self):
        self.container = None
        self.click_token = 0

    def update_highlight(self, row_container: ft.Container, e) -> None:
        # 前回行のハイライト表示を解除
        if self.container is not None:
            self.container.border = UiUtils.set_highlight()
            self.container = None
            e.page.update()

        # 選択行をハイライト表示
        row_container.border = UiUtils.set_highlight(Color.SELECT_COLOR)
        self.container = row_container
        e.page.update()

        # 連打判定用トークン
        self.click_token += 1
        current_token = self.click_token

        # 500ms後の解除を予約
        e.page.run_task(
            self.clear_highlight_if_latest, current_token, e.page, row_container
        )

    async def clear_highlight_if_latest(
        self,
        current_token: int,
        current_page: ft.Page,
        target_container: ft.Container,
    ) -> None:
        """
        指定時間待機後、最新の操作であればハイライトを解除します。
        連打された場合、古いタスクはトークン不一致により早期リターンします。
        """

        """非同期処理"""
        # 1. 指定時間待機
        await asyncio.sleep(Timing.HIGHLIGHT_ANIMATION_TIME)

        """0.5秒後に動く処理"""
        # 2. トークンチェック（最新のクリックタスクのみ実行を許可）
        if self.click_token != current_token:
            return

        # 3. ハイライトを元の状態（枠線色）に戻す
        target_container.border = UiUtils.set_highlight()

        # 4. 自身が保持しているコンテナ参照が今回の対象ならクリア
        if self.container is target_container:
            self.container = None

        # 5. UI更新
        current_page.update()
