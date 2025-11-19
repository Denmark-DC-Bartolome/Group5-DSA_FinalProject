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
    _ensure_output_dir()
    try:
        with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
            json.dump(bookmarks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(RED + f" Could not save bookmarks: {e}" + RESET)
# Load bookmarks on module import
_load_bookmarks()


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
    Remove a bookmark if it exists.
    """
    if ref in bookmarks:
        del bookmarks[ref]
        _save_bookmarks()
        print(f"  Removed bookmark: {ref}")
    else:
        print(RED + "  Bookmark not found." + RESET)


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
