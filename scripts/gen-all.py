import json
import math
import os
import re

from PIL import Image, ImageDraw, ImageFont
from natsort import natsorted


THUMB_SIZE = (150, 150)
PADDING = 20
TEXT_HEIGHT = 40
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_SIZE = 12
FONT_INDEX = 6


total = 0
manifest = {}

try:
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE, index=FONT_INDEX)
except IOError:
    print(f"Error loading {FONT_PATH}")
    font = ImageFont.load_default()


# Scan subdirs
for subdir in os.listdir("stickers"):
    subdir_path = os.path.join("stickers", subdir)
    names = []
    images = []

    # Collect names
    for file in os.listdir(subdir_path):
        name = file.rsplit(".", 1)[0]
        names.append(name)
        total += 1

    # Skip empty subdir
    if len(names) == 0:
        continue

    # Read images
    manifest[subdir] = sorted(names)
    for name in manifest[subdir]:
        file_path = os.path.join(subdir_path, f"{name}.webp")
        with Image.open(file_path) as img:
            container = Image.new(
                "RGBA",
                (THUMB_SIZE[0], THUMB_SIZE[1] + TEXT_HEIGHT + 5),
                (255, 255, 255, 0),
            )

            img = img.convert("RGBA")
            img.thumbnail(THUMB_SIZE)

            # Centering image
            x_offset = (THUMB_SIZE[0] - img.width) // 2
            y_offset = (THUMB_SIZE[1] - img.height) // 2
            container.paste(img, (x_offset, y_offset), img)

            images.append((container, name))

    # Compute preview size
    num_images = len(images)
    cols = math.ceil(math.sqrt(num_images))
    rows = math.ceil(num_images / cols)
    cell_width = THUMB_SIZE[0] + PADDING
    cell_height = THUMB_SIZE[1] + TEXT_HEIGHT + PADDING
    final_width = (cols * cell_width) + PADDING
    final_height = (rows * cell_height) + PADDING

    # Create preview image
    preview_img = Image.new("RGB", (final_width, final_height), BG_COLOR)
    draw = ImageDraw.Draw(preview_img)

    # Draw stickers and texts
    for index, (img, name) in enumerate(images):
        col = index % cols
        row = index // cols
        x = PADDING + (col * cell_width)
        y = PADDING + (row * cell_height)

        preview_img.paste(img, (x, y), img)

        text_bbox = draw.textbbox((0, 0), name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x + (THUMB_SIZE[0] - text_width) // 2
        text_y = y + THUMB_SIZE[1] + 5

        draw.text((text_x, text_y), name, fill=TEXT_COLOR, font=font)

    # Save image
    output_path = os.path.join("assets/preview", f"{subdir}.webp")
    preview_img.save(output_path)


# Update manifest
with open("manifest.json", "w") as f:
    json.dump(manifest, f, separators=(",", ":"), sort_keys=True)


# Update readme
with open("README.md", "r") as f:
    old = f.read()
with open("README.md", "w") as f:
    pat = re.compile(r'<span id="count">(.*)?</span>')
    new = re.sub(pat, f'<span id="count">{total}</span>', old)
    f.write(new)


# Update preview
with open("PREVIEW.md", "w") as f:
    f.write("# 表情包预览\n\n")
    for subdir in natsorted(manifest.keys()):
        f.writelines(
            [
                f"## {subdir}\n\n",
                f"共 {len(manifest[subdir])} 枚\n\n",
                f"![{subdir}](./assets/preview/{subdir}.webp)\n\n",
            ]
        )
