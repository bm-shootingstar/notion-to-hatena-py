import logging
import os

from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

logger = logging.getLogger(__name__)


def fetch_notion_page(page_id: str) -> list:
    """
    Fetches all blocks from a Notion page.

    Args:
        page_id: The ID of the Notion page.

    Returns:
        A list of block objects.
    """
    notion = Client(auth=os.environ["NOTION_API_KEY"])
    response = notion.blocks.children.list(block_id=page_id)
    return response.get("results", [])


def fetch_page_title(page_id: str) -> str | None:
    """
    Fetches the title of a Notion page.

    Args:
        page_id: The ID of the Notion page.

    Returns:
        The title of the page, or None if not found.
    """
    notion = Client(auth=os.environ["NOTION_API_KEY"])
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

        logger.error(
            "Could not find a property of type 'title' in the page properties."
        )
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
        blocks = fetch_notion_page(test_page_id)
        import json

        logger.info(json.dumps(blocks, indent=2, ensure_ascii=False))
    else:
        logger.warning("Please set a test page ID in `src/notion_fetcher.py`")
