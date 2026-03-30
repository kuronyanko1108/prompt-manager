class AppException(Exception):
    """アプリケーションの基底例外クラス"""

    def __init__(self, message: str = "Internal Application Error"):
        super().__init__(message)
        self.message = message


class SystemException(AppException):
    """システム起因の基底例外"""

    pass


class DatabaseException(SystemException):
    """データベース操作に関する例外"""

    pass


class BusinessException(AppException):
    """業務ロジック（想定内）に関する例外"""

    pass


class ValidationException(BusinessException):
    """入力値チェックに関する例外"""

    pass


class PromptException(BusinessException):
    """プロンプト操作に関する例外"""

    pass
