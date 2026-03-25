import flet as ft
from abc import ABC, abstractmethod
from typing import Sequence, Optional


class BasePromptScreen(ABC):
    """画面作成の抽象基底クラス。"""

    @abstractmethod
    def appbar(self) -> Optional[ft.AppBar]:
        """実装クラスでAppBarを返すようにします。"""
        pass

    @abstractmethod
    def controls(self) -> Sequence[ft.Control]:
        """実装クラスでControlのリストを返すようにします。"""
        pass

    @abstractmethod
    def bottom_appbar(self) -> Optional[ft.BottomAppBar]:
        """実装クラスでBottomAppBarを返すようにします。"""
        pass

    def create_view(self, route: str) -> ft.View:
        """
        実装された各パーツを組み立てて ft.View を生成します。

        Args:
            route (str): 画面のルートパス

        Returns:
            ft.View: Fletのビューオブジェクト
        """
        return ft.View(
            route=route,
            appbar=self.appbar(),
            controls=list(self.controls()),
            bottom_appbar=self.bottom_appbar(),
        )
