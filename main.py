import logging
import sys

from src.controllers.main_controller import process_notion_to_hatena

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to run the script.
    """
    if len(sys.argv) < 2:
        logger.error("Usage: python main.py <NOTION_PAGE_ID_OR_URL> [--publish]")
        sys.exit(1)

    input_arg = sys.argv[1]
    publish = "--publish" in sys.argv

    try:
        process_notion_to_hatena(input_arg, publish)
    except ValueError as e:
        logger.error(e)
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        sys.exit(1)


def run_gui():
    """
    Launches the GUI application.
    """
    try:
        from src.views.gui_app import launch_gui

        launch_gui()
    except ImportError as e:
        logger.error(f"Failed to import GUI module: {e}. Make sure PySide6 is installed.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        run_gui()
    else:
        main()
