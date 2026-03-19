class PromptValidator:

    def validate_create(self, title: str, content: str):
        trim_title = title.strip()
        trim_content = content.strip()

        errors = []

        # title:必須チェック
        if not trim_title:
            errors.append("タイトルは必須です")

        # title:文字数上限
        if len(trim_title) > 100:
            errors.append("タイトルは100文字以内で入力してください")

        # content:必須チェック
        if not trim_content:
            errors.append("本文は必須です")

        # content:文字数上限
        if len(trim_content) > 10000:
            errors.append("本文は10000文字以内で入力してください")

        return errors

    def validate_update(self, prompt_id: int, title: str, content: str):
        errors = []
        errors = self.validate_create(title, content)

        # prompt_id:必須チェック
        if prompt_id is None:
            errors.append("IDは必須です")

        # prompt_id:数値チェック
        elif not isinstance(prompt_id, int):
            errors.append("IDは数値である必要があります")

        # prompt_id:値範囲チェック
        elif prompt_id <= 0:
            errors.append("IDは1以上である必要があります")

        return errors
