import os
import json

root_dir = "stickers"
manifest = {}

if os.path.exists(root_dir):
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)

        if os.path.isdir(item_path):
            webp_files = []
            for filename in sorted(os.listdir(item_path)):
                if filename.endswith(".webp"):
                    clean_name = filename.rsplit(".", 1)[0]
                    webp_files.append(clean_name)

            if webp_files:
                manifest[item] = webp_files

with open("manifest.json", "w") as f:
    json.dump(manifest, f, separators=(",", ":"))
