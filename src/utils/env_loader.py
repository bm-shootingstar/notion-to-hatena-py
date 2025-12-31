import os
import sys

from dotenv import load_dotenv


def load_env():
    """
    Loads environment variables from .env file.
    If running as a frozen executable (PyInstaller), looks for .env in the executable's directory.
    Otherwise, looks in the current working directory.
    """
    if getattr(sys, "frozen", False):
        # Running as compiled executable
        base_path = os.path.dirname(sys.executable)
        env_path = os.path.join(base_path, ".env")
        load_dotenv(env_path)
    else:
        # Running as script
        load_dotenv()
