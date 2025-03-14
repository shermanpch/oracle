import os

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from coordinate import COORDINATE
from hexagram import HEXAGRAM


def fetch_and_parse(url):
    """Fetch a URL and return a BeautifulSoup object."""
    response = requests.get(url)
    response.encoding = "utf-8"  # Ensure correct decoding for Chinese
    html = response.text
    return BeautifulSoup(html, "html.parser")


def download_image(img_url, save_path):
    """Download and save an image from a given URL."""
    try:
        response = requests.get(img_url, stream=True)
        response.raise_for_status()

        # Save the image
        with open(save_path, "wb") as img_file:
            for chunk in response.iter_content(1024):
                img_file.write(chunk)
        print(f"Saved image: {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download image {img_url}: {e}")


# Total number of coordinates to scrape for progress tracking
total_coordinates = len(COORDINATE)

# Process each coordinate with progress tracking using tqdm
for coordinate in tqdm(COORDINATE, total=total_coordinates, desc="Scraping Hexagrams"):
    hex_name = COORDINATE[coordinate]

    if hex_name not in HEXAGRAM:
        print(f"Hexagram '{hex_name}' not found in HEXAGRAM mapping, skipping...")
        continue

    url = HEXAGRAM[hex_name]
    soup = fetch_and_parse(url)

    # Find title and body divs
    title_divs = soup.find_all("div", class_="guatt cf f14 fb tleft")
    body_divs = soup.find_all("div", class_="gualist tleft f14 lh25")

    # Combine each pair as before
    for idx, (title_div, body_div) in enumerate(zip(title_divs, body_divs)):
        title_text = title_div.get_text(separator="\n", strip=True)
        body_text = body_div.get_text(separator="\n", strip=True)
        combined = f"{title_text}\n{body_text}"

        # Extract the first image URL from body_div
        img_tag = body_div.find("img")
        img_url = img_tag["src"] if img_tag else None

        # Define storage paths
        if idx == 0:
            folder = os.path.join("data", f"{coordinate[0]}-{coordinate[1]}", "html")
            img_folder = os.path.join(
                "data", f"{coordinate[0]}-{coordinate[1]}", "images"
            )
        else:
            folder = os.path.join(
                "data", f"{coordinate[0]}-{coordinate[1]}", str(idx % 6), "html"
            )
            img_folder = os.path.join(
                "data", f"{coordinate[0]}-{coordinate[1]}", str(idx % 6), "images"
            )

        # Make sure the folders exist
        os.makedirs(folder, exist_ok=True)
        os.makedirs(img_folder, exist_ok=True)

        # Save the body text
        file_path = os.path.join(folder, "body.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(combined)
        print(f"Saved {hex_name} body {idx} to {file_path}")

        # Save the image if it exists
        if img_url:
            img_path = os.path.join(img_folder, "image.jpg")
            download_image(img_url, img_path)
