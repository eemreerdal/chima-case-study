from moviepy.editor import TextClip, ImageClip, CompositeVideoClip, concatenate_videoclips, ColorClip
import os
import uuid
import requests
from PIL import Image
from io import BytesIO
import random


def clean_script(script):
    lines = []
    for line in script.split('\n'):
        line = line.strip()
        if line and line != "]":
            line = line.replace("Narrator:", "").lstrip("[").rstrip("]")
            lines.append(line)
    return lines


def download_images(image_urls):
    image_paths = []
    for i, url in enumerate(image_urls):
        try:
            print(f"⬇️ Downloading image {i+1}: {url}")
            img_data = requests.get(url, timeout=5).content
            image_path = f"temp_{uuid.uuid4().hex}.jpg"
            with open(image_path, 'wb') as handler:
                handler.write(img_data)
            image_paths.append(image_path)
        except Exception as e:
            print(f"Failed to download image {i+1}: {e}")
    print(f"Successfully downloaded {len(image_paths)} images.\n")
    return image_paths



def create_video_ad(product_data, ad_script):
    title = product_data.get("title", "")
    image_urls = product_data.get("image_urls", []) or [product_data.get("image_url", "")]
    features = product_data.get("features", [])

    # Download images
    image_paths = download_images(image_urls)
    if not image_paths:
        print("Failed to download any product image.")
        return ""

    ad_lines = clean_script(ad_script)
    ad_lines = ad_lines[:12]  # ~30 seconds cap (12 * 2.6s)

    clips = []
    for i, text in enumerate(ad_lines):
        image_path = image_paths[i % len(image_paths)]

        # Resize image
        product_img = Image.open(image_path)
        aspect = product_img.width / product_img.height
        img_clip = ImageClip(image_path)
        img_clip = img_clip.resize(width=720) if aspect > 1 else img_clip.resize(height=720)

        # Animated background color
        bg_color = random.choice([(0, 0, 0), (15, 15, 15), (25, 25, 25)])
        bg_clip = ColorClip(size=(720, 1280), color=bg_color, duration=2.6)

        # Animate image entry
        img_clip = img_clip.set_duration(2.6).set_position(("center", "top")).fadein(0.4).fadeout(0.4)

        # Text animation
        txt_clip = TextClip(
            text,
            fontsize=40,
            color='white',
            font="Arial-Bold",
            method='caption',
            size=(700, None)
        ).set_duration(2.6).set_position(("center", 920)).fadein(0.4).fadeout(0.4)

        final = CompositeVideoClip([bg_clip, img_clip, txt_clip])
        clips.append(final)

    full_video = concatenate_videoclips(clips, method="compose")

    # Save output
    output_dir = "generated"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{uuid.uuid4().hex}.mp4")
    full_video.write_videofile(output_path, fps=24)

    # Clean up
    for path in image_paths:
        os.remove(path)

    return output_path
