"""
bookmark.py
-----------------------------------------------
Persistent bookmarks using a JSON file at ../outputs/bookmarks.txt
Keeps an in-memory dict `bookmarks` for fast access and writes to disk
whenever a change is made.
"""

import json
import os
from ui import *
import re

# On-disk path (relative to this file's directory)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../outputs")
BOOKMARKS_FILE = os.path.join(OUTPUT_DIR, "bookmarks.txt")

# In-memory bookmark store: { "John 3:16": "For God so loved..." }
bookmarks = {}

# -------------------------
# Helpers: load/save
# -------------------------
def _ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

def _load_bookmarks():
    global bookmarks
    _ensure_output_dir()
    if not os.path.exists(BOOKMARKS_FILE):
        bookmarks = {}
        return
    try:
        with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
            bookmarks = json.load(f)
            if not isinstance(bookmarks, dict):
                bookmarks = {}
    except Exception:
        # If file is corrupted or unreadable, reset to empty and overwrite on next save
        bookmarks = {}

def _save_bookmarks():
    """Persist the in-memory bookmarks dict to disk (JSON)."""
    _ensure_output_dir()
    try:
        with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
            json.dump(bookmarks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(RED + f" Could not save bookmarks: {e}" + RESET)
# Load bookmarks on module import
_load_bookmarks()



# -------------------------
# Parsing helpers (if needed)
# -------------------------
# NOTE: The program's main flow already canonicalizes book names; these functions
# help when user supplies a list/range of refs (if you later need to parse them inside this file).
_REF_SPLIT_RE = re.compile(r"^(.+?)\s+(\d+:\d+(?:[-, \d]*)?)\s*$")

def _normalize_ref_string(ref: str) -> str:
    """
    Normalize a single canonical ref string (no structural changes) — e.g. trim.
    Used when removing exact keys from bookmarks dict.
    """
    return ref.strip()

















# -------------------------
# Public API
# -------------------------
def add_bookmark(ref, verse_text):
    """
    Adds or updates a bookmark, saves to disk immediately.
    ref: canonical string like 'John 3:16'
    verse_text: the verse content
    """
    bookmarks[ref] = verse_text
    _save_bookmarks()
    print(f"  Added bookmark: {ref}")


def remove_bookmark(ref):
    """
    Remove a bookmark by exact reference string.
    Accepts a single canonical ref (e.g. "John 3:16").
    Returns True if removed, False if not found.
    """
    key = _normalize_ref_string(ref)
    if key in bookmarks:
        del bookmarks[key]
        _save_bookmarks()
        print(GREEN + f"  Removed bookmark: {key}" + RESET)
        return True
    else:
        print( RED + f" Bookmark not found: {key}" + RESET)
        return False


def remove_bookmarks_bulk(refs):
    """
    Remove multiple bookmarks given a list of canonical reference strings.
    Returns a tuple (removed_count, not_found_list).
    """
    removed = 0
    not_found = []
    for r in refs:
        key = _normalize_ref_string(r)
        if key in bookmarks:
            del bookmarks[key]
            removed += 1
        else:
            not_found.append(key)
    # Save once after bulk removal
    _save_bookmarks()
    if removed:
        print(f"  Removed {removed} bookmark(s).")
    if not_found:
        print("  These bookmarks were not found and so were not removed:")
        for k in not_found:
            print(f"   - {k}")
    return (removed, not_found)

def clear_all_bookmarks():
    """
    Remove all bookmarks (in-memory and on-disk).
    Use caution: this is destructive and permanent.
    """
    global bookmarks
    bookmarks = {}
    _save_bookmarks()
    print("  All bookmarks cleared.")









def show_bookmarks():
    """
    Displays all bookmarked verses.
    """
    if not bookmarks:
        print(" No bookmarks yet.")
        return

    print("\n Bookmarked Verses:")
    for ref, text in bookmarks.items():
        print(f"{BLUE}{ref}{RESET} — {text}\n")




def export_bookmarks_txt(path):
    """
    Optional: export bookmarks to a plain text file at 'path'.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            for ref, text in bookmarks.items():
                f.write(f"{ref} — {text}\n")
        print(f"  Exported bookmarks to {path}")
    except Exception as e:
        print(f"  Failed to export bookmarks: {e}")
