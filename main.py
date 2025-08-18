import logging
import re
import sys
from urllib.parse import urlparse

from src.converter import convert_to_markdown
from src.hatena_poster import post_to_hatena
from src.notion_fetcher import fetch_blocks_recursively, fetch_page_title

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    stream=sys.stdout,
)
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
        return None


def main():
    """
    Main function to run the script.
    """
    if len(sys.argv) < 2:
        logger.error("Usage: python main.py <NOTION_PAGE_ID_OR_URL> [--publish]")
        sys.exit(1)

    input_arg = sys.argv[1]
    publish = "--publish" in sys.argv

    page_id = extract_page_id(input_arg)

    if not page_id:
        logger.error(
            f"Invalid Notion page ID or URL provided: '{input_arg}'. "
            f"Please provide a valid 32-character page ID or a full Notion URL."
        )
        sys.exit(1)

    logger.info(f"Fetching content from Notion page: {page_id}")
    title = fetch_page_title(page_id)
    blocks = fetch_blocks_recursively(page_id)

    if not title or not blocks:
        logger.warning("No content or title found on the page.")
        return

    logger.info("Converting to Markdown...")
    markdown_content = convert_to_markdown(blocks)

    logger.info(f"Posting to Hatena Blog with title: {title}")
    post_to_hatena(title, markdown_content, draft=not publish)


if __name__ == "__main__":
    main()
