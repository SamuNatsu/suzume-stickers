import json
import os
import re


total = 0
manifest = {}


# Scan subdirs
for subdir in os.listdir("stickers"):
    subdir_path = os.path.join("stickers", subdir)
    names = []

    # Collect names
    for file in os.listdir(subdir_path):
        name = file.rsplit(".", 1)[0]
        names.append(name)
        total += 1

    # Skip empty subdir
    if len(names) == 0:
        continue

    # Add record
    manifest[subdir] = sorted(names)


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
