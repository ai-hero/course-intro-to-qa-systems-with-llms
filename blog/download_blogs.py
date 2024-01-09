import os
from typing import Any, List

import html2text
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def setup_headless_chrome() -> webdriver.Chrome:
    """Set up headless Chrome for Selenium."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def fetch_page_selenium(url: str) -> Any:
    """Use Selenium to fetch the page content."""
    driver = setup_headless_chrome()
    driver.get(url)
    content = driver.page_source
    driver.quit()
    return content


def download_and_save_in_markdown(url: str, dir_path: str) -> None:
    """Download the HTML content from the web page and save it as a markdown file."""
    # Extract a filename from the URL
    if url.endswith("/"):
        url = url[:-1]
    filename = url.split("/")[-1] + ".txt"
    print(f"Downloading {url} into {filename}...")

    # Fetch the page content using Selenium
    html_content = fetch_page_selenium(url)

    # Convert the HTML content to markdown
    h = html2text.HTML2Text()
    markdown_content = h.handle(html_content)

    # Write the markdown content to a file
    filename = os.path.join(dir_path, filename)
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)


def download(pages: List[str]) -> str:
    """Download the HTML content from the pages and save them as markdown files."""
    # Create the content/notion directory if it doesn't exist
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(base_dir, ".content", "blogs")
    os.makedirs(dir_path, exist_ok=True)
    for page in pages:
        download_and_save_in_markdown(page, dir_path)
    return dir_path


PAGES = [
    "https://mlops.community/building-the-future-with-llmops-the-main-challenges/",
]

if __name__ == "__main__":
    print("NOTE: This demo doesn't work in Github codespaces.")
    download(PAGES)
