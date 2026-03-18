import os
import math

from PIL import Image, ImageDraw, ImageFont
from natsort import natsorted

STICKERS_DIR = "stickers"
OUTPUT_DIR = "assets/preview"
THUMB_SIZE = (150, 150)
PADDING = 20
TEXT_HEIGHT = 40
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_SIZE = 12
FONT_INDEX = 6

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

try:
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE, index=FONT_INDEX)
except IOError:
    print(f"Error loading {FONT_PATH}")
    font = ImageFont.load_default()

collections = []
collection_count = {}

for collection_name in os.listdir(STICKERS_DIR):
    images = []

    collection_path = os.path.join(STICKERS_DIR, collection_name)
    if not os.path.isdir(collection_path):
        continue

    files = sorted([f for f in os.listdir(collection_path) if f.endswith(".webp")])
    if not files:
        continue

    for filename in files:
        img_path = os.path.join(collection_path, filename)
        try:
            with Image.open(img_path) as img:
                img = img.convert("RGBA")
                img.thumbnail(THUMB_SIZE)

                container = Image.new(
                    "RGBA",
                    (THUMB_SIZE[0], THUMB_SIZE[1] + TEXT_HEIGHT + 5),
                    (255, 255, 255, 0),
                )

                x_offset = (THUMB_SIZE[0] - img.width) // 2
                y_offset = (THUMB_SIZE[1] - img.height) // 2
                container.paste(img, (x_offset, y_offset), img)

                images.append((container, filename))
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    if not images:
        continue

    num_images = len(images)
    cols = math.ceil(math.sqrt(num_images))
    rows = math.ceil(num_images / cols)

    cell_width = THUMB_SIZE[0] + PADDING
    cell_height = THUMB_SIZE[1] + TEXT_HEIGHT + PADDING

    final_width = (cols * cell_width) + PADDING
    final_height = (rows * cell_height) + PADDING

    preview_img = Image.new("RGB", (final_width, final_height), BG_COLOR)
    draw = ImageDraw.Draw(preview_img)

    for index, (img_obj, fname) in enumerate(images):
        col = index % cols
        row = index // cols

        x = PADDING + (col * cell_width)
        y = PADDING + (row * cell_height)

        preview_img.paste(img_obj, (x, y), img_obj)

        text_bbox = draw.textbbox((0, 0), fname, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x + (THUMB_SIZE[0] - text_width) // 2
        text_y = y + THUMB_SIZE[1] + 5

        draw.text((text_x, text_y), fname, fill=TEXT_COLOR, font=font)

    output_path = os.path.join(OUTPUT_DIR, f"{collection_name}.webp")
    preview_img.save(output_path)

    collections.append(collection_name)
    collection_count[collection_name] = len(images)

with open("PREVIEW.md", "w") as f:
    f.write("# 表情包预览\n\n")
    for collection in natsorted(collections):
        f.writelines(
            [
                f"## {collection}\n\n",
                f"共 {collection_count[collection]} 枚\n\n",
                f"![{collection}](./assets/preview/{collection}.webp)\n\n",
            ]
        )
