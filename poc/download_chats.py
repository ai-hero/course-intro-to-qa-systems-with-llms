"""Download chats from Google Drive."""
import os

import gdown


def download_chats_from_gdrive() -> None:
    """Download chats from Google Drive."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(base_dir, ".content", "chats")
    os.makedirs(dir_path, exist_ok=True)
    if os.path.exists(os.path.join(dir_path, "chats-embeddings-ada-002.csv")):
        print("Directory already exists. Skipping download.")
        return
    gdown.download_folder(
        "https://drive.google.com/drive/folders/1TmNPMr15Iw_HnqKJWWpDJFVSMqaBXy9m?usp=sharing",
        output=dir_path,
        quiet=False,
    )
