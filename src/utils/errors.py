class NotionAPIKeyError(Exception):
    """
    NOTION_API_KEYが設定されていない場合に発生するカスタム例外。
    """
    pass

class NotionPageIDError(Exception):
    """
    NotionページIDが設定されていない場合に発生するカスタム例外。
    """
    pass
