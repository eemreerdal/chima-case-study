import requests
from bs4 import BeautifulSoup
import json

def scrape_product_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch URL"}

    soup = BeautifulSoup(response.text, 'html.parser')

    # Title
    title_tag = soup.find("meta", property="og:title")
    title = title_tag["content"] if title_tag and title_tag.has_attr("content") else "No title found"

    # Image URLs
    image_urls = []

    # Try og:image first
    image_tag = soup.find("meta", property="og:image")
    if image_tag and image_tag.has_attr("content"):
        image_urls.append(image_tag["content"])

    # Scan all <img> tags (and srcset if available)
    for img in soup.find_all("img"):
        # Check standard src
        src = img.get("src")
        if src and src.startswith("http") and src not in image_urls:
            image_urls.append(src)

        # Also check srcset (responsive images)
        srcset = img.get("srcset")
        if srcset:
            src_items = [item.strip().split(" ")[0] for item in srcset.split(",")]
            for item in src_items:
                if item.startswith("http") and item not in image_urls:
                    image_urls.append(item)

        if len(image_urls) >= 5:
            break

    # Features from JSON-LD
    features = []
    json_ld_tag = soup.find("script", type="application/ld+json")
    if json_ld_tag:
        try:
            data = json.loads(json_ld_tag.string)
            if isinstance(data, dict):
                description = data.get("description", "")
                features = description.split(". ")[:4]
        except Exception as e:
            print("Failed to parse JSON-LD:", e)

    return {
        "title": title,
        "image_urls": image_urls,
        "features": features
    }
