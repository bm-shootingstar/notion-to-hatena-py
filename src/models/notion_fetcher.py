import logging
import os

from notion_client import Client

from src.utils.env_loader import load_env
from src.utils.errors import NotionAPIKeyError

load_env()

logger = logging.getLogger(__name__)

_notion_client_instance = None  # Notionクライアントインスタンスを保持するための変数


def _get_notion_client() -> Client:
    """
    Notionクライアントインスタンスを取得または初期化する。
    NOTION_API_KEYがない場合はNotionAPIKeyErrorを発生させる。
    """
    global _notion_client_instance
    if _notion_client_instance is None:
        notion_api_key = os.environ.get("NOTION_API_KEY")
        if not notion_api_key:
            error_message = (
                "環境変数 'NOTION_API_KEY' が設定されていません。\n"
                "'.env' ファイルが実行ファイルと同じディレクトリに存在するか、\n"
                "またはシステム環境変数に 'NOTION_API_KEY' が設定されていることを確認してください。"
            )
            logger.error(error_message)
            raise NotionAPIKeyError(error_message)
        _notion_client_instance = Client(auth=notion_api_key)
    return _notion_client_instance


def fetch_blocks_recursively(block_id: str) -> list:
    """
    Fetches all blocks from a Notion page recursively.

    Args:
        block_id: The ID of the Notion block (or page).

    Returns:
        A list of block objects with their children.
    """
    notion = _get_notion_client()  # ここでクライアントを取得し、必要であればNotionAPIKeyErrorをraise
    blocks = []
    response = notion.blocks.children.list(block_id=block_id)
    results = response.get("results", [])
    blocks.extend(results)

    for block in results:
        if block.get("has_children"):
            block["children"] = fetch_blocks_recursively(block["id"])

    return blocks


def fetch_page_title(page_id: str) -> str | None:
    """
    Fetches the title of a Notion page.

    Args:
        page_id: The ID of the Notion page.

    Returns:
        The title of the page, or None if not found.
    """
    notion = _get_notion_client()  # ここでクライアントを取得し、必要であればNotionAPIKeyErrorをraise
    try:
        page = notion.pages.retrieve(page_id=page_id)
        properties = page.get("properties")
        if not properties:
            logger.error("Page object does not contain 'properties'.")
            return None

        for prop_data in properties.values():
            if isinstance(prop_data, dict) and prop_data.get("type") == "title":
                title_list = prop_data.get("title", [])
                if title_list:
                    return title_list[0].get("plain_text")

        logger.error("Could not find a property of type 'title' in the page properties.")
        return None

    except Exception as e:
        logger.error(
            f"An exception occurred while fetching the Notion page title: {e}",
            exc_info=True,
        )
        return None


if __name__ == "__main__":
    # Replace with a test page ID
    test_page_id = "YOUR_TEST_PAGE_ID"
    if test_page_id != "YOUR_TEST_PAGE_ID":
        title = fetch_page_title(test_page_id)
        if title:
            logger.info(f"Title: {title}")
        else:
            logger.warning("Could not fetch title.")
        blocks = fetch_blocks_recursively(test_page_id)
        import json

        logger.info(json.dumps(blocks, indent=2, ensure_ascii=False))
    else:
        logger.warning("Please set a test page ID in `src/notion_fetcher.py`")
