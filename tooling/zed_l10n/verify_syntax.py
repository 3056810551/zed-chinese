import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
LOCALES_DIR = Path(__file__).resolve().parent / "locales"
EXTRACTED_FILE = LOCALES_DIR / "extracted_strings.json"

with open(EXTRACTED_FILE, "r", encoding="utf-8") as fp:
    extracted = json.load(fp)

all_files = set()
for item in extracted.values():
    for f in item["files"]:
        if f.endswith(".rs"):
            all_files.add(f)

print(f"Checking {len(all_files)} target Rust files...")
errors = []

for f in sorted(all_files):
    full_path = ROOT / f
    if not full_path.exists():
        continue
    with open(full_path, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
        for i, line in enumerate(lines):
            code_part = line.split("//")[0]
            code_part = code_part.replace('\\"', '')
            # Multi-line strings can have odd quotes, but check single line anomalies
            if code_part.count('"') % 2 != 0 and 'r#"' not in code_part and '"#' not in code_part:
                errors.append((f, i + 1, line.strip()))

print(f"Checked. Anomalies: {len(errors)}")
for f, line_no, content in errors[:30]:
    print(f"  {f}:{line_no}: {content}")

