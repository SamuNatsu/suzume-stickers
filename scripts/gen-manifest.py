import os
import re
import json

root_dir = "stickers"
manifest = {}
count = 0

if os.path.exists(root_dir):
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)

        if os.path.isdir(item_path):
            webp_files = []
            for filename in sorted(os.listdir(item_path)):
                if filename.endswith(".webp"):
                    clean_name = filename.rsplit(".", 1)[0]
                    webp_files.append(clean_name)
                    count += 1

            if webp_files:
                manifest[item] = webp_files

with open("manifest.json", "w") as f:
    json.dump(manifest, f, separators=(",", ":"))

with open("README.md") as f:
    rdme = f.read()

with open("README.md", "w") as f:
    pat = re.compile(r'<span id="count">(.*)?</span>')
    rdme = re.sub(pat, f'<span id="count">{count}</span>', rdme)
    f.write(rdme)
