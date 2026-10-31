import re
from pathlib import Path
import json

content = Path("crates/settings_ui/src/page_data.rs").read_text(encoding="utf-8")

# Pages
pages = re.findall(r'SettingsPage\s*\{\s*title:\s*"([^"]+)"', content)

# Section headers
headers = list(set(re.findall(r'SectionHeader\(\s*"([^"]+)"\)', content)))

# Setting item titles and descriptions
titles = list(set(re.findall(r'title:\s*"([^"]+)"', content)))
descs = list(set(re.findall(r'description:\s*"([^"]+)"', content)))

print(f"Pages ({len(pages)}):", pages)
print(f"Headers count: {len(headers)}")
print(f"Titles count: {len(titles)}")
print(f"Descriptions count: {len(descs)}")

out = {
    "pages": sorted(pages),
    "headers": sorted(headers),
    "titles": sorted(titles),
    "descriptions": sorted(descs)
}
Path("tooling/zed_l10n/settings_strings.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved to tooling/zed_l10n/settings_strings.json")
