""" Download blogs in the URLS """
import asyncio
import os
from typing import Any, List

import html2text
from pyppeteer import launch


async def fetch_page(url: str) -> Any:
    """Launch a browser, navigate to the URL, and return the HTML content."""
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, waitUntil="networkidle0")
    content = await page.content()
    await browser.close()
    return content


def download_and_save_in_markdown(url: str, dir_path: str) -> None:
    """Download the HTML content from the web page and save it as a markdown file."""
    # Extract a filename from the URL
    if url.endswith("/"):
        url = url[:-1]
    filename = url.split("/")[-1] + ".md"
    print(f"Downloading {url} into {filename}...")

    # Fetch the page content using pyppeteer
    html_content = asyncio.get_event_loop().run_until_complete(fetch_page(url))

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
    "https://raw.githubusercontent.com/run-llama/llama_index/main/examples/paul_graham_essay/data/paul_graham_essay.txt",
]

if __name__ == "__main__":
    download(PAGES)
