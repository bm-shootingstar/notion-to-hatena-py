import logging
import re
from urllib.parse import urlparse

from src.models.converter import convert_to_markdown
from src.models.hatena_poster import post_to_hatena
from src.models.notion_fetcher import fetch_blocks_recursively, fetch_page_title
from src.utils.errors import NotionPageIDError

logger = logging.getLogger(__name__)


def extract_page_id(url_or_id: str) -> str | None:
    """
    Extracts the Notion page ID from a URL or returns the ID if it's already an ID.
    Validates that the page ID is a 32-character hexadecimal string.
    """
    # Check if it's a URL
    if url_or_id.startswith("http"):
        parsed_url = urlparse(url_or_id)
        path = parsed_url.path.strip("/")
        # The page ID is usually the last part of the path
        potential_id = path.split("-")[-1]
    else:
        potential_id = url_or_id

    # Validate the ID format (32 hex characters)
    if re.fullmatch(r"[a-fA-F0-9]{32}", potential_id):
        return potential_id
    else:
        raise NotionPageIDError(
            f"不正なNotionページIDまたはURLが提供されました: '{url_or_id}'. "
            f"有効な32文字のページIDまたは完全なNotion URLを入力してください。"
        )


def process_notion_to_hatena(input_arg: str, publish: bool = False):
    """
    Orchestrates the fetching from Notion and posting to Hatena.
    Raises ValueError if input_arg is invalid.
    """
    page_id = extract_page_id(input_arg)

    logger.info(f"Fetching content from Notion page: {page_id}")
    title = fetch_page_title(page_id)
    blocks = fetch_blocks_recursively(page_id)

    if not title:
        logger.warning("No title found on the page.")
        return

    if not blocks:
        logger.warning("No content found on the page.")
        return

    logger.info("Converting to Markdown...")
    markdown_content = convert_to_markdown(blocks)

    logger.info(f"Posting to Hatena Blog with title: {title}")
    post_to_hatena(title, markdown_content, draft=not publish)
