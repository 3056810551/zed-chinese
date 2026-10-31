"""
Zed Editor Localization Extraction Tool
Extracts user-facing UI strings from Zed crates into a structured JSON dictionary.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Any

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CRATES_DIR = ROOT_DIR / "crates"
OUTPUT_DIR = Path(__file__).resolve().parent / "locales"

# UI Patterns in Zed Rust source code
PATTERNS = [
    # Menu items in app_menus.rs or menus
    ("menu_action", re.compile(r'\bMenuItem::action\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"')),
    ("menu_os_action", re.compile(r'\bMenuItem::os_action\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"')),
    ("menu_submenu", re.compile(r'\bMenu::new\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"')),
    ("menu_name", re.compile(r'name:\s*"([^"\\]*(?:\\.[^"\\]*)*)"\.into\(\)')),
    ("menu_builder_action", re.compile(r'\.action\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"')),
    ("menu_builder_action_disabled", re.compile(r'\.action_disabled_when\([^,]+,\s*"([^"\\]*(?:\\.[^"\\]*)*)"')),
    ("context_menu_entry", re.compile(r'\bContextMenuEntry::action\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"')),

    # Tooltips
    ("tooltip_text", re.compile(r'\bTooltip::text\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"')),
    ("tooltip_simple", re.compile(r'\bTooltip::simple\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"')),
    ("tooltip_for_action", re.compile(r'\bTooltip::for_action_title\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"')),
    ("tooltip_with_meta", re.compile(r'\bTooltip::with_meta\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"')),

    # UI Labels & Buttons
    ("ui_label", re.compile(r'\bLabel::new\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"\)')),
    ("ui_label_shared", re.compile(r'\bLabel::new\(\s*SharedString::from\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"\s*\)\)')),
    ("highlighted_label", re.compile(r'\bHighlightedLabel::new\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"')),
    ("button_label", re.compile(r'\bButton::new\([^,]+,\s*"([^"\\]*(?:\\.[^"\\]*)*)"\)')),
    ("button_set_label", re.compile(r'\.label\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"\)')),
    ("button_link", re.compile(r'\bButtonLink::new\([^,]+,\s*"([^"\\]*(?:\\.[^"\\]*)*)"\)')),
    
    # Input placeholders, prompts, headers
    ("input_placeholder", re.compile(r'\.placeholder\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"\)')),
    ("headline", re.compile(r'\bHeadline::new\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"\)')),
    ("subheadline", re.compile(r'\bSubheadline::new\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"\)')),
    ("section_title", re.compile(r'\bSection::new\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"\)')),
]

# Patterns or words to filter out (not user-facing UI text, e.g. identifiers, css, technical names)
EXCLUDE_EXACT = {
    "", " ", "\n", "id", "test", "utf-8", "none", "auto", "default", "true", "false",
    "http", "https", "localhost", "127.0.0.1", "0.0.0.0", "zed", "Zed",
}

def should_keep(text: str) -> bool:
    text = text.strip()
    if not text or len(text) < 2:
        return False
    if text in EXCLUDE_EXACT:
        return False
    # Filter out kebab-case / snake_case element ids (e.g. 'activity-indicator-popover')
    if re.match(r'^[a-z0-9]+(-[a-z0-9]+)+$', text):
        return False
    if re.match(r'^[a-z0-9]+(_[a-z0-9]+)+$', text):
        return False
    # Filter out pure code/regex/path/url/hex
    if text.startswith("http://") or text.startswith("https://") or text.startswith("file://"):
        return False
    if text.startswith("/") or text.startswith("\\") or text.startswith("./"):
        return False
    if text.startswith("x-") or text.startswith("application/"):
        return False
    # Must contain at least one ASCII letter
    if not any(c.isalpha() for c in text):
        return False
    return True

def scan_crates():
    results: Dict[str, Dict[str, Any]] = {}
    total_matches = 0

    # Crates to skip (benchmarks, internal system tools, grammar parsers)
    skip_crates = {
        "benchmarks", "editor_benchmarks", "fs_benchmarks", "worktree_benchmarks",
        "grammars", "eval_cli", "eval_utils", "proto", "db"
    }

    for crate_dir in sorted(CRATES_DIR.iterdir()):
        if not crate_dir.is_dir() or crate_dir.name in skip_crates:
            continue

        crate_name = crate_dir.name

        for root, dirs, files in os.walk(crate_dir):
            # Skip test directories to avoid cluttering UI translations
            if "test" in root.lower() and "ui" not in root.lower():
                continue

            for f in files:
                if not f.endswith(".rs"):
                    continue

                filepath = Path(root) / f
                rel_path = filepath.relative_to(ROOT_DIR).as_posix()

                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                except Exception as e:
                    print(f"Error reading {rel_path}: {e}")
                    continue

                for pat_name, pattern in PATTERNS:
                    for m in pattern.finditer(content):
                        text = m.group(1).replace(r'\"', '"')
                        if should_keep(text):
                            total_matches += 1
                            if text not in results:
                                results[text] = {
                                    "occurrences": [],
                                    "categories": set(),
                                }
                            results[text]["occurrences"].append(rel_path)
                            results[text]["categories"].add(pat_name)

    print(f"Scan complete. Found {len(results)} distinct UI strings across {total_matches} occurrences.")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / "extracted_strings.json"

    export_data = {}
    for text, info in sorted(results.items(), key=lambda x: x[0].lower()):
        export_data[text] = {
            "categories": sorted(list(info["categories"])),
            "files": sorted(list(set(info["occurrences"]))),
            "count": len(info["occurrences"]),
        }

    with open(out_file, "w", encoding="utf-8") as fp:
        json.dump(export_data, fp, indent=2, ensure_ascii=False)

    print(f"Saved extracted strings to: {out_file}")
    return export_data

if __name__ == "__main__":
    scan_crates()
