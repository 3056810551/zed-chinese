"""
Zed Localization Patcher
Applies translations from zh-CN.json directly to Zed Rust source files.
Provides safe, lossless, and easily reversible string replacement.
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
LOCALES_DIR = Path(__file__).resolve().parent / "locales"
EXTRACTED_FILE = LOCALES_DIR / "extracted_strings.json"
ZH_CN_FILE = LOCALES_DIR / "zh-CN.json"

# Exact wrapper patterns for safe in-place replacement
REPLACE_TEMPLATES = [
    ('MenuItem::action("{en}"', 'MenuItem::action("{zh}"'),
    ('MenuItem::os_action("{en}"', 'MenuItem::os_action("{zh}"'),
    ('Menu::new("{en}")', 'Menu::new("{zh}")'),
    ('name: "{en}".into()', 'name: "{zh}".into()'),
    ('.action("{en}"', '.action("{zh}"'),
    ('.action_disabled_when({extra}, "{en}"', '.action_disabled_when({extra}, "{zh}"'),
    ('ContextMenuEntry::action("{en}"', 'ContextMenuEntry::action("{zh}"'),
    ('Tooltip::text("{en}")', 'Tooltip::text("{zh}")'),
    ('Tooltip::simple("{en}"', 'Tooltip::simple("{zh}"'),
    ('Tooltip::for_action_title("{en}"', 'Tooltip::for_action_title("{zh}"'),
    ('Tooltip::with_meta("{en}"', 'Tooltip::with_meta("{zh}"'),
    ('Label::new("{en}")', 'Label::new("{zh}")'),
    ('HighlightedLabel::new("{en}"', 'HighlightedLabel::new("{zh}"'),
    ('.label("{en}")', '.label("{zh}")'),
    ('Headline::new("{en}")', 'Headline::new("{zh}")'),
    ('Subheadline::new("{en}")', 'Subheadline::new("{zh}")'),
    ('Section::new("{en}")', 'Section::new("{zh}")'),
    ('.placeholder("{en}")', '.placeholder("{zh}")'),
]

def load_translations() -> Dict[str, str]:
    if not ZH_CN_FILE.exists():
        print(f"Error: {ZH_CN_FILE} does not exist. Run generate_dict.py first.")
        sys.exit(1)

    with open(ZH_CN_FILE, "r", encoding="utf-8") as fp:
        raw_dict = json.load(fp)

    # Filter out empty or identical translations
    active = {k: v for k, v in raw_dict.items() if v and v != k}
    return active

def apply_patch():
    translations = load_translations()
    print(f"Loaded {len(translations)} active Chinese translations from zh-CN.json.")

    if not EXTRACTED_FILE.exists():
        print(f"Error: {EXTRACTED_FILE} does not exist. Run extract.py first.")
        sys.exit(1)

    with open(EXTRACTED_FILE, "r", encoding="utf-8") as fp:
        extracted = json.load(fp)

    # Map each target file to its relevant translations
    files_to_patch = {}
    for en_text, zh_text in translations.items():
        if en_text in extracted:
            for rel_file in extracted[en_text]["files"]:
                files_to_patch.setdefault(rel_file, []).append((en_text, zh_text))

    total_files_modified = 0
    total_replacements = 0

    for rel_path, items in files_to_patch.items():
        full_path = ROOT_DIR / rel_path
        if not full_path.exists():
            continue

        try:
            with open(full_path, "r", encoding="utf-8") as fp:
                original_content = fp.read()
        except Exception as e:
            print(f"Skipping {rel_path}: {e}")
            continue

        content = original_content
        file_replacements = 0

        for en, zh in items:
            # Escape quotes for Rust string literals
            en_esc = en.replace('"', r'\"')
            zh_esc = zh.replace('"', r'\"')

            for t_src, t_dst in REPLACE_TEMPLATES:
                src_str = t_src.format(en=en_esc, extra="")
                dst_str = t_dst.format(zh=zh_esc, extra="")

                if src_str in content:
                    count = content.count(src_str)
                    content = content.replace(src_str, dst_str)
                    file_replacements += count

        if content != original_content:
            with open(full_path, "w", encoding="utf-8") as fp:
                fp.write(content)
            total_files_modified += 1
            total_replacements += file_replacements

    print(f"\n[OK] Patch Applied Successfully!")
    print(f"  - Files modified: {total_files_modified}")
    print(f"  - Strings replaced: {total_replacements}")

def restore_code():
    print("Restoring crates/ to original state...")
    try:
        subprocess.run(["git", "checkout", "--", "crates/"], cwd=ROOT_DIR, check=True)
        print("[OK] Successfully restored crates/ to original state.")
    except Exception as e:
        print(f"Error restoring via git: {e}")

def show_status():
    translations = load_translations()
    print(f"Localization Status:")
    print(f"  - Active zh-CN translations: {len(translations)}")
    try:
        res = subprocess.run(["git", "status", "--porcelain", "crates/"], cwd=ROOT_DIR, capture_output=True, text=True)
        modified = [line for line in res.stdout.splitlines() if line.startswith(" M")]
        print(f"  - Modified crate files: {len(modified)}")
        if modified:
            print("  - Samples:")
            for m in modified[:10]:
                print(f"    {m.strip()}")
    except Exception as e:
        print(f"Git check error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--restore":
        restore_code()
    elif len(sys.argv) > 1 and sys.argv[1] == "--status":
        show_status()
    else:
        apply_patch()
