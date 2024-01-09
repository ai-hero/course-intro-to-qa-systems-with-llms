"""Download chats from Google Drive."""
import os

import gdown
from dotenv import load_dotenv


def download_chats_from_gdrive() -> None:
    """Download chats from Google Drive."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(base_dir, ".content", "chats")
    os.makedirs(dir_path, exist_ok=True)
    if os.path.exists(os.path.join(dir_path, "chats-embeddings-ada-002.csv")):
        print("Directory already exists. Skipping download.")
        return
    gdown.download_folder(
        os.getenv("MLOPS_DATA_URL"),
        output=dir_path,
        quiet=False,
    )


if __name__ == "__main__":
    # Load the .env file
    load_dotenv()  # Use 'dotenv_path=' arg to change this to your own .env file, if not using the venv

    assert os.getenv("MLOPS_DATA_URL") is not None, "MLOPS_DATA_URL not found in .env file"
    download_chats_from_gdrive()
