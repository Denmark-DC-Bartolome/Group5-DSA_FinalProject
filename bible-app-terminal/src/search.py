"""
src/search.py  —  compact, readable search module

Public API:
  - search_verse(bible_tree, query)
  - navigation(cmd)         # "next" | "prev"
  - clear_results()
  - _find_book_matches(bible_tree, prefix)
  - _choose_book_interactive(matches)

Behavior:
  - Supports reference (Book Chapter:Verse), chapter, book, and keyword searches.
  - Uses an inverted index (if present) for fast keyword & phrase searches.
  - Falls back to Horspool (Boyer–Moore variant) substring search if index missing.
  - Interactive disambiguation when input could be a book name or a keyword.
  - Pagination: PAGE_SIZE results per page, with next/prev navigation.
"""

from __future__ import annotations
import re
from typing import List, Tuple, Optional, Dict
from history import add_history
from ui import clear_screen, show_commands

# try to use the index-based search helper (optional)
try:
    from search_index import load_index, query_index
    _INDEX = load_index()
except Exception:
    _INDEX = {}  # safe fallback

# ------------------------------------------------------------------
# Config + state
# ------------------------------------------------------------------
PAGE_SIZE = 20
last_results: List[Tuple[str, str]] = []    # list of (ref, text)
_current_page_start = 0

# Regex patterns for detecting reference/chapter/book
_REF_RE = re.compile(r"^([1-3]?\s?[A-Za-z]+)\s+(\d+):([\d,\-\s]+)$", re.I)
_CH_RE = re.compile(r"^([1-3]?\s?[A-Za-z]+)\s+(\d+)$", re.I)
_BOOK_RE = re.compile(r"^([1-3]?\s?[A-Za-z]+)$", re.I)

# ------------------------------------------------------------------
# Small, safe Horspool implementation (fast and compact)
# ------------------------------------------------------------------
def _horspool_shift(p: str) -> Dict[str, int]:
    m = len(p)
    shift = {chr(i): m for i in range(256)}
    for i in range(m - 1):
        shift[p[i]] = m - i - 1
    return shift

def horspool_search(text: str, pattern: str) -> int:
    """Case-insensitive Horspool; returns first index or -1."""
    if not pattern:
        return 0
    if not text:
        return -1
    t = text.lower(); p = pattern.lower()
    m, n = len(p), len(t)
    if m > n:
        return -1
    shift = _horspool_shift(p)
    i = m - 1
    while i < n:
        k = 0
        while k < m and p[m - 1 - k] == t[i - k]:
            k += 1
        if k == m:
            return i - m + 1
        i += shift.get(t[i], m)
    return -1

# ------------------------------------------------------------------
# Book name normalization & matching helpers (handles "1 Corinthians")
# ------------------------------------------------------------------
def _norm_book(s: str) -> str:
    return "".join(s.split()).lower() if s else ""

def _find_book_matches(bible_tree: dict, short_name: str) -> List[str]:
    t = _norm_book(short_name)
    return [bk for bk in bible_tree.keys() if _norm_book(bk).startswith(t)]

def _choose_book_interactive(matches: List[str]) -> Optional[str]:
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]
    print("\n Your input matches multiple books:")
    for i, b in enumerate(matches, 1):
        print(f"  {i}. {b}")
    while True:
        c = input(f"Enter 1–{len(matches)} (or Enter to cancel): ").strip()
        if c == "":
            print("Cancelled.")
            return None
        if c.isdigit():
            idx = int(c)
            if 1 <= idx <= len(matches):
                sel = matches[idx - 1]
                print(f"Selected: {sel}")
                return sel
        print("Invalid choice — try again.")

# ------------------------------------------------------------------
# Quick check: does token appear anywhere? (uses index if available)
# ------------------------------------------------------------------
def _quick_keyword_check(bible_tree: dict, token: str, limit: int = 1) -> bool:
    if not token:
        return False
    q = token.lower()
    if _INDEX:
        # query_index supports multiple tokens & phrases; we only need existence
        res = query_index(q, _INDEX, bible_tree)
        return len(res) >= 1
    # fallback scan (stop early)
    seen = 0
    for bk, chapters in bible_tree.items():
        for ch, verses in chapters.items():
            for vnum, txt in verses.items():
                if txt and q in txt.lower():
                    seen += 1
                    if seen >= limit:
                        return True
    return False

# ------------------------------------------------------------------
# Core: search_verse (short & structured)
# ------------------------------------------------------------------
def search_verse(bible_tree: dict, query: str):
    """Detect type and dispatch to reference/chapter/book/text handlers."""
    global last_results, _current_page_start
    last_results = []; _current_page_start = 0
    if not query or not query.strip():
        print(" Empty search. Use: search love | search Col 3:4 | search Col 1")
        return
    q = query.strip()

    # Reference e.g. "Col 3:4" or "1Cor 13:4-7"
    m = _REF_RE.match(q)
    if m:
        book_raw, chap, verse_part = m.groups()
        matches = _find_book_matches(bible_tree, book_raw)
        if not matches:
            print(f" Book '{book_raw}' not found.")
            return
        bk = _choose_book_interactive(matches)
        if not bk:
            return
        add_history(q)
        _handle_reference_search(bible_tree, bk, chap, verse_part)
        _show_current_page(); return

    # Book + chapter e.g. "Col 1"
    m = _CH_RE.match(q)
    if m:
        book_raw, chap = m.groups()
        matches = _find_book_matches(bible_tree, book_raw)
        if matches:
            bk = _choose_book_interactive(matches)
            if not bk:
                return
            add_history(q)
            _handle_chapter_search(bible_tree, bk, chap)
            _show_current_page(); return
        # else fallthrough to text search

    # Book-only vs text ambiguity e.g. "r"
    m = _BOOK_RE.match(q)
    if m:
        book_raw = m.group(1)
        matches = _find_book_matches(bible_tree, book_raw)
        keyword_possible = _quick_keyword_check(bible_tree, q, limit=1)
        if matches and keyword_possible:
            clear_screen()
            print(f"\n '{q}' matches both book names and text.")
            choice = input("Type 1 for Book, 2 for Text (Enter to cancel): ").strip()
            if choice == "1":
                bk = _choose_book_interactive(matches)
                if not bk: return
                add_history(q); _handle_book_search(bible_tree, bk); _show_current_page(); return
            if choice == "2":
                add_history(q); _handle_text_search(bible_tree, q); _show_current_page(); return
            clear_screen(); print("Cancelled."); show_commands(); return
        if matches and not keyword_possible:
            bk = _choose_book_interactive(matches)
            if not bk: return
            add_history(q); _handle_book_search(bible_tree, bk); _show_current_page(); return
        if not matches:
            add_history(q); _handle_text_search(bible_tree, q); _show_current_page(); return

    # Fallback: treat as keyword/text search
    add_history(q)
    _handle_text_search(bible_tree, q)
    _show_current_page()

# ------------------------------------------------------------------
# Result collectors: populate last_results
# ------------------------------------------------------------------
def _handle_text_search(bible_tree: dict, query: str):
    """Use inverted index when available, otherwise fall back to Horspool scanning."""
    global last_results, _current_page_start
    last_results = []; _current_page_start = 0
    q = (query or "").strip()
    if not q:
        return
    # If index available -> use it (fast, supports phrases)
    if _INDEX:
        hits = query_index(q, _INDEX, bible_tree)
        for h in hits:
            last_results.append((h["ref"], h["text"]))
        return
    # Fallback substring scan using Horspool for faster per-verse check
    ql = q.lower()
    for bk, chapters in bible_tree.items():
        for ch, verses in chapters.items():
            for vnum, txt in verses.items():
                if txt and horspool_search(txt, ql) != -1:
                    last_results.append((f"{bk} {ch}:{vnum}", txt))

def _handle_reference_search(bible_tree: dict, book_key: str, chapter: str, verse_part: str):
    global last_results, _current_page_start
    last_results = []; _current_page_start = 0
    chap = bible_tree.get(book_key, {}).get(chapter)
    if not chap:
        print(f" Chapter {chapter} not found in {book_key}."); return
    found = False
    for token in verse_part.split(","):
        part = token.strip()
        if "-" in part:
            try:
                s, e = map(int, part.split("-", 1))
            except ValueError:
                continue
            for v in range(s, e + 1):
                t = chap.get(str(v))
                if t:
                    last_results.append((f"{book_key} {chapter}:{v}", t)); found = True
        else:
            t = chap.get(part)
            if t:
                last_results.append((f"{book_key} {chapter}:{part}", t)); found = True
    if not found:
        print(f" No matching verse(s) in {book_key} {chapter} for '{verse_part}'.")

def _handle_chapter_search(bible_tree: dict, book_key: str, chapter: str):
    global last_results, _current_page_start
    last_results = []; _current_page_start = 0
    chap = bible_tree.get(book_key, {}).get(chapter)
    if not chap:
        print(f" Chapter {chapter} not found in {book_key}."); return
    for vnum, txt in chap.items():
        last_results.append((f"{book_key} {chapter}:{vnum}", txt))

def _handle_book_search(bible_tree: dict, book_key: str):
    global last_results, _current_page_start
    last_results = []; _current_page_start = 0
    book_data = bible_tree.get(book_key, {})
    if not book_data:
        print(f" Book '{book_key}' not found or empty."); return
    for ch, verses in book_data.items():
        for vnum, txt in verses.items():
            last_results.append((f"{book_key} {ch}:{vnum}", txt))

# ------------------------------------------------------------------
# Pagination & navigation
# ------------------------------------------------------------------
def _show_current_page():
    global last_results, _current_page_start
    if not last_results:
        print("ℹ No results to display."); return
    total = len(last_results)
    start = _current_page_start
    end = min(start + PAGE_SIZE, total)
    page = start // PAGE_SIZE + 1
    pages = (total - 1) // PAGE_SIZE + 1
    clear_screen()
    print(f"\n Showing verses {start+1}–{end} of {total} (Page {page}/{pages})\n")
    print("-" * 80)
    for i in range(start, end):
        ref, txt = last_results[i]
        print(f"{ref} — {txt}\n")
    print("-" * 80)
    show_commands()
    if pages > 1:
        print("\nUse 'next' or 'prev' to navigate.")

def navigation(command: str):
    global _current_page_start, last_results
    if not last_results:
        clear_screen(); print("ℹ No active search results. Use 'search <query>'."); show_commands(); return
    total = len(last_results)
    cmd = command.lower()
    if cmd == "next":
        if _current_page_start + PAGE_SIZE < total:
            _current_page_start += PAGE_SIZE; _show_current_page()
        else:
            print(" End of results.")
    elif cmd == "prev":
        if _current_page_start >= PAGE_SIZE:
            _current_page_start -= PAGE_SIZE; _show_current_page()
        else:
            clear_screen(); print(" Already at first page."); show_commands()
    else:
        print(" Use 'next' or 'prev'.")

def clear_results():
    global last_results, _current_page_start
    last_results = []; _current_page_start = 0
