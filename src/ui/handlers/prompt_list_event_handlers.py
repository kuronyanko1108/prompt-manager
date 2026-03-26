import flet as ft
from ...dto.prompt_dto import PromptSummaryDTO
from ..view.list_view import PromptListView
from ..states.prompt_list_state_manager import PromptListStateManager
import asyncio


class PromptListEventHandlers:
    """
    prompt_list_event_handlers: PromptListScreenのイベントハンドラ専用モジュール
    """

    def on_edit_click_handle(self, prompt: PromptSummaryDTO, e) -> None:
        """
        編集ボタンクリック時のイベントハンドラ。
        指定されたプロンプトの編集画面へ遷移します。

        Args:
            prompt (PromptSummaryDTO): 編集対象のプロンプト情報
            e(ControlEvent) :コントロールイベント
        """
        asyncio.create_task(e.page.push_route(f"/edit/{prompt.id}"))

    def on_copy_click_handle(
        self,
        prompt_list_view: PromptListView,
        prompt: PromptSummaryDTO,
        row_container: ft.Container,
        e,
    ) -> None:
        """
        コピーボタンクリック時のイベントハンドラ。
        選択対象のプロンプトの本文をクリップボードにコピーします。
        また、コピー対象のリストをハイライト表示します。

        Args:
            prompt_list_view (PromptListView): コピー処理を委譲するビュー
            prompt (PromptSummaryDTO): コピー対象のプロンプト情報
            row_container (ft.Container): ハイライトを適用するUIコンテナ
            e(ft.ControlEvent) :コントロールイベント
        """
        # クリップボードにコピー
        prompt_list_view.on_copy_clicked(prompt, e)

        # ハイライト表示
        state = PromptListStateManager()
        state.update_highlight(row_container, e)

    @staticmethod
    async def on_drawer_click_handle(page: ft.Page) -> None:
        """
        ドロワーボタンクリック時のイベントハンドラ。
        ナビゲーションドロワーを表示します。

        Args:
            page (ft.Page): 操作対象のページオブジェクト
        """
        await page.show_drawer()
