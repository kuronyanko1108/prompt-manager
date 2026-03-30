from src.exceptions.exceptions import AppException, SystemException, DatabaseException
from src.exceptions.exceptions import (
    BusinessException,
    PromptException,
    ValidationException,
)


def test_AppException():
    """アプリケーションの基底例外クラス"""
    try:
        raise AppException("テスト用Exception")
    except AppException as e:
        assert str(e) == "テスト用Exception"
        assert isinstance(e, AppException)


def test_AppException_default_message():
    """アプリケーションの基底例外クラス"""
    try:
        raise AppException
    except AppException as e:
        assert str(e) == "Internal Application Error"
        assert isinstance(e, AppException)


def test_SystemException():
    """システム起因の基底例外"""

    try:
        raise SystemException("テスト用Exception")
    except SystemException as e:
        assert str(e) == "テスト用Exception"
        assert isinstance(e, AppException)
        assert isinstance(e, SystemException)


def test_DatabaseException():
    """データベース操作に関する例外"""
    try:
        raise DatabaseException("テスト用Exception")
    except DatabaseException as e:
        assert str(e) == "テスト用Exception"
        assert isinstance(e, AppException)
        assert isinstance(e, SystemException)
        assert isinstance(e, DatabaseException)


def test_BusinessException():
    """業務ロジック（想定内）に関する例外"""
    try:
        raise BusinessException("テスト用Exception")
    except BusinessException as e:
        assert str(e) == "テスト用Exception"
        assert isinstance(e, AppException)
        assert isinstance(e, BusinessException)


def test_ValidationException():
    """入力値チェックに関する例外"""
    try:
        raise ValidationException("テスト用Exception")
    except ValidationException as e:
        assert str(e) == "テスト用Exception"
        assert isinstance(e, AppException)
        assert isinstance(e, BusinessException)
        assert isinstance(e, ValidationException)


def test_PromptException():
    """プロンプト操作に関する例外"""
    try:
        raise PromptException("テスト用Exception")
    except PromptException as e:
        assert str(e) == "テスト用Exception"
        assert isinstance(e, AppException)
        assert isinstance(e, BusinessException)
        assert isinstance(e, PromptException)
