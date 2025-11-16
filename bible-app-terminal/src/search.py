

# """
# src/search.py
# -------------------------------------------------
# Comprehensive search module for the Terminal-Based Bible App.

# Capabilities:
# - Keyword search using Boyer–Moore algorithm
# - Book / Book+Chapter / Book+Chapter:Verse searches (supports ranges & lists)
# - Interactive disambiguation for ambiguous inputs (e.g., "r" or "co")
# - Paginated results (20 verses per page) with `next` / `prev` navigation
# - Timestamped history logging via add_history()
# - All functions are documented and intended for use by main.py
# -------------------------------------------------
# """

# import re
# from history import add_history  # expects history module with add_history(query)
# from typing import List, Tuple

# # Globals for storing current search results and pagination state
# last_results: List[Tuple[str, str]] = []  # list of (ref, text)
# current_page_start: int = 0               # start index (0-based) of current page
# PAGE_SIZE = 20                            # verses per page


# # ---------------------------
# # Boyer–Moore (case-insensitive)
# # ---------------------------
# def boyer_moore_search(text: str, pattern: str) -> int:
#     """
#     Returns index of first occurrence of pattern in text (case-insensitive),
#     or -1 if not found. Uses a simple bad-character heuristic.
#     """
#     text = text or ""
#     pattern = pattern or ""
#     m = len(pattern)
#     n = len(text)
#     if m == 0:
#         return 0
#     # build bad-character table (last occurrence style)
#     skip = {pattern[i].lower(): m - i - 1 for i in range(m - 1)}
#     i = m - 1
#     while i < n:
#         k = 0
#         while k < m and pattern[m - 1 - k].lower() == text[i - k].lower():
#             k += 1
#         if k == m:
#             return i - m + 1
#         i += skip.get(text[i].lower(), m)
#     return -1


# # ---------------------------
# # Book-name helpers
# # ---------------------------
# def find_book_matches(bible_tree: dict, short_name: str) -> List[str]:
#     """
#     Return list of book keys from bible_tree whose names start with short_name (case-insensitive).
#     Example: 'co' -> ['1Corinthians', '2Corinthians', 'Colossians'] (order depends on bible_tree keys)
#     """
#     s = (short_name or "").lower().replace(" ", "")
#     matches = [bk for bk in bible_tree.keys() if bk.lower().replace(" ", "").startswith(s)]
#     return matches


# def choose_book_interactive(matches: List[str]) -> str:
#     """
#     If multiple book matches are found, present them to the user and ask for a numeric choice.
#     Returns the chosen book key, or None if cancelled/invalid.
#     """
#     if not matches:
#         return None
#     if len(matches) == 1:
#         return matches[0]

#     print(f"\n Your input matches multiple books:")
#     for idx, bk in enumerate(matches, start=1):
#         print(f"   {idx}. {bk}")
#     while True:
#         choice = input(f" Enter 1–{len(matches)} to select the correct book (or press Enter to cancel): ").strip()
#         if choice == "":
#             print(" Selection cancelled.")
#             return None
#         try:
#             n = int(choice)
#             if 1 <= n <= len(matches):
#                 selected = matches[n - 1]
#                 print(f" Selected: {selected}\n")
#                 return selected
#             else:
#                 print(" Invalid number. Try again.")
#         except ValueError:
#             print(" Please enter a valid number.")


# # ---------------------------
# # Core search entrypoint
# # ---------------------------
# def search_verse(bible_tree: dict, query: str):
#     """
#     Public entry point for searches.
#     Detects the query type and routes to appropriate handler.

#     Behavior required by spec:
#     - If the query could be both a book and a word (e.g., 'r'), ask the user:
#       "the letter 'r' matches a book and a word, please type 1 if it is book and 2 if it is word"
#     - Supports:
#       - Keyword search: 'search love'
#       - Book only: 'search Col' (asks Book or Text if ambiguous)
#       - Book + Chapter: 'search Col 1'
#       - Reference: 'search Col 3:4'
#       - Range/multiple: 'search Col 2:2,4-6'
#       - Interactive book choice for ambiguous partial names: 'search co 3:4'
#     - After confirming the search type, logs the query with timestamp via add_history(query)
#     - Populates last_results and shows the first page (up to PAGE_SIZE)
#     """
#     global last_results, current_page_start
#     last_results.clear()
#     current_page_start = 0
#     if not query or not query.strip():
#         print(" Empty query. Usage examples:\n  search love\n  search Col 3:4\n  search Col 1")
#         return

#     q = query.strip()

#     # Patterns
#     ref_pattern = r"^([1-3]?\s?[A-Za-z]+)\s+(\d+):([\d,\-\s]+)$"   # book chap:verses
#     chapter_pattern = r"^([1-3]?\s?[A-Za-z]+)\s+(\d+)$"            # book chap
#     book_pattern = r"^([1-3]?\s?[A-Za-z]+)$"                      # book only

#     # If query matches reference like 'Col 3:4' (book chap:verse(s))
#     if re.match(ref_pattern, q, re.IGNORECASE):
#         book_raw, chapter, verse_part = re.match(ref_pattern, q, re.IGNORECASE).groups()
#         book_raw = book_raw.capitalize().replace(" ", "")
#         # resolve book (interactive if multiple)
#         matches = find_book_matches(bible_tree, book_raw)
#         if not matches:
#             print(f" Book '{book_raw}' not found.")
#             return
#         book_key = choose_book_interactive(matches)
#         if not book_key:
#             return
#         # record to history then perform reference search
#         add_history(q)
#         _handle_reference_search(bible_tree, book_key, chapter, verse_part)
#         _show_current_page()
#         return

#     # If query matches 'book chapter' like 'Col 1'
#     if re.match(chapter_pattern, q, re.IGNORECASE):
#         book_raw, chapter = re.match(chapter_pattern, q, re.IGNORECASE).groups()
#         book_raw = book_raw.capitalize().replace(" ", "")
#         matches = find_book_matches(bible_tree, book_raw)
#         if not matches:
#             # Not a book? treat as text search fallback
#             # But first check ambiguous scenario vs word (see below) — we treat as text
#             add_history(q)
#             _handle_text_search(bible_tree, q)
#             _show_current_page()
#             return
#         book_key = choose_book_interactive(matches)
#         if not book_key:
#             return
#         add_history(q)
#         _handle_chapter_search(bible_tree, book_key, chapter)
#         _show_current_page()
#         return

#     # If query matches single book like 'Col'
#     if re.match(book_pattern, q, re.IGNORECASE):
#         book_raw = re.match(book_pattern, q, re.IGNORECASE).groups()[0]
#         book_raw = book_raw.capitalize().replace(" ", "")
#         matches = find_book_matches(bible_tree, book_raw)

#         # Determine if q also yields any immediate keyword hits (we will check quickly but stop early)
#         keyword_possible = _quick_keyword_check(bible_tree, q)

#         # If both a book match and keyword matches exist -> ask user to choose Book vs Text
#         if matches and keyword_possible:
#             print(f"\n The input '{q}' matches a book name and also appears as text in verses.")
#             print(" Type 1 to treat input as a Book search (show book/chapter/verse).")
#             print(" Type 2 to treat input as a Text/Keyword search (find verses containing the word).")
#             choice = input("Enter 1 (Book) or 2 (Text), or press Enter to cancel: ").strip()
#             if choice == "1":
#                 # Book flow
#                 book_key = choose_book_interactive(matches)
#                 if not book_key:
#                     return
#                 add_history(q)
#                 _handle_book_search(bible_tree, book_key)
#                 _show_current_page()
#                 return
#             elif choice == "2":
#                 add_history(q)
#                 _handle_text_search(bible_tree, q)
#                 _show_current_page()
#                 return
#             else:
#                 print(" Cancelled.")
#                 return

#         # If only book matches (no conflicting keyword) -> book search
#         if matches and not keyword_possible:
#             book_key = choose_book_interactive(matches)
#             if not book_key:
#                 return
#             add_history(q)
#             _handle_book_search(bible_tree, book_key)
#             _show_current_page()
#             return

#         # If no book matches -> treat as text search
#         if not matches:
#             add_history(q)
#             _handle_text_search(bible_tree, q)
#             _show_current_page()
#             return

#     # Fallback (default): treat as keyword search
#     add_history(q)
#     _handle_text_search(bible_tree, q)
#     _show_current_page()


# # ---------------------------
# # Helper: quick check whether any verse contains the query (stop early)
# # ---------------------------
# def _quick_keyword_check(bible_tree: dict, query: str, limit: int = 1) -> bool:
#     """
#     Scan bible_tree for the query appearing in any verse. Stop after 'limit' matches are found.
#     Returns True if at least one match found (so keyword search is plausible).
#     This is used to determine ambiguity (book vs word).
#     """
#     q = (query or "").lower()
#     matches_found = 0
#     for book, chapters in bible_tree.items():
#         for chapter, verses in chapters.items():
#             for verse_num, text in verses.items():
#                 if q in (text or "").lower():
#                     matches_found += 1
#                     if matches_found >= limit:
#                         return True
#     return False


# # ---------------------------
# # Handle text/keyword search (fills last_results)
# # ---------------------------
# def _handle_text_search(bible_tree: dict, query: str):
#     """
#     Populate last_results with verses containing the query (case-insensitive).
#     Uses Boyer–Moore for per-verse matching (efficient enough).
#     """
#     global last_results, current_page_start
#     last_results = []
#     current_page_start = 0
#     q = (query or "").lower()
#     for book, chapters in bible_tree.items():
#         for chapter, verses in chapters.items():
#             for verse_num, text in verses.items():
#                 if boyer_moore_search((text or "").lower(), q) != -1:
#                     ref = f"{book} {chapter}:{verse_num}"
#                     last_results.append((ref, text))


# # ---------------------------
# # Handle reference-based search (single, ranges, lists)
# # ---------------------------
# def _handle_reference_search(bible_tree: dict, book_key: str, chapter: str, verse_part: str):
#     """
#     Given book_key (full book name), chapter number and verse_part like '2,4-6',
#     populate last_results with those verses (if found).
#     """
#     global last_results, current_page_start
#     last_results = []
#     current_page_start = 0

#     # Validate chapter exists
#     chapter_data = bible_tree.get(book_key, {}).get(chapter)
#     if not chapter_data:
#         print(f" Chapter {chapter} not found in {book_key}.")
#         return

#     found = False
#     for part in verse_part.split(","):
#         part = part.strip()
#         if "-" in part:
#             try:
#                 start_s, end_s = part.split("-", 1)
#                 start = int(start_s)
#                 end = int(end_s)
#             except ValueError:
#                 continue
#             for v in range(start, end + 1):
#                 verse_text = chapter_data.get(str(v))
#                 if verse_text:
#                     last_results.append((f"{book_key} {chapter}:{v}", verse_text))
#                     found = True
#         else:
#             verse_text = chapter_data.get(part)
#             if verse_text:
#                 last_results.append((f"{book_key} {chapter}:{part}", verse_text))
#                 found = True

#     if not found:
#         print(f" No matching verse(s) found in {book_key} {chapter} for '{verse_part}'.")
#     # else results are ready for pagination


# # ---------------------------
# # Handle chapter-level search (all verses in chapter)
# # ---------------------------
# def _handle_chapter_search(bible_tree: dict, book_key: str, chapter: str):
#     """
#     Populate last_results with every verse in that chapter.
#     """
#     global last_results, current_page_start
#     last_results = []
#     current_page_start = 0
#     chapter_data = bible_tree.get(book_key, {}).get(chapter)
#     if not chapter_data:
#         print(f" Chapter {chapter} not found in {book_key}.")
#         return
#     for verse_num, verse_text in chapter_data.items():
#         last_results.append((f"{book_key} {chapter}:{verse_num}", verse_text))


# # ---------------------------
# # Handle book-level search (all verses in a book)
# # ---------------------------
# def _handle_book_search(bible_tree: dict, book_key: str):
#     """
#     Populate last_results with every verse in the chosen book (all chapters).
#     """
#     global last_results, current_page_start
#     last_results = []
#     current_page_start = 0
#     book_data = bible_tree.get(book_key, {})
#     if not book_data:
#         print(f" Book '{book_key}' not found or empty.")
#         return
#     for chapter, verses in book_data.items():
#         for verse_num, verse_text in verses.items():
#             last_results.append((f"{book_key} {chapter}:{verse_num}", verse_text))


# # ---------------------------
# # Pagination / UI: show current page
# # ---------------------------
# def _show_current_page():
#     """
#     Shows up to PAGE_SIZE verses starting at current_page_start.
#     Also prints "Page X of Y" and navigation hint.
#     """
#     global last_results, current_page_start
#     if not last_results:
#         print("ℹ No results to display.")
#         return

#     total = len(last_results)
#     start = current_page_start
#     end = min(start + PAGE_SIZE, total)
#     page_num = start // PAGE_SIZE + 1
#     total_pages = (total - 1) // PAGE_SIZE + 1

#     print(f"\n Showing verses {start + 1}–{end} of {total} (Page {page_num} of {total_pages})")
#     print("-" * 80)
#     for i in range(start, end):
#         ref, text = last_results[i]
#         print(f"{ref} — {text}")
#     print("-" * 80)
#     print(f" Showing verses {start + 1}–{end} of {total} (Page {page_num} of {total_pages})")
#     if total_pages > 1:
#         print("\n Use 'next' or 'prev' to navigate pages.")


# # ---------------------------
# # Navigation commands: next / prev (page-wise)
# # ---------------------------
# def navigation(command: str):
#     """
#     Move to the next or previous page of results.
#     command: 'next' or 'prev'
#     """
#     global current_page_start, last_results
#     if not last_results:
#         print("ℹ No active search results. Use 'search <query>' to start.")
#         return

#     total = len(last_results)
#     if command.lower() == "next":
#         if current_page_start + PAGE_SIZE < total:
#             current_page_start += PAGE_SIZE
#             _show_current_page()
#         else:
#             print(" You have reached the end of results.")
#     elif command.lower() == "prev":
#         if current_page_start - PAGE_SIZE >= 0:
#             current_page_start -= PAGE_SIZE
#             _show_current_page()
#         else:
#             print(" You are already at the first page.")
#     else:
#         print(" Invalid navigation command. Use 'next' or 'prev'.")


# # ---------------------------
# # For main.py integration: helper to clear results (optional)
# # ---------------------------
# def clear_results():
#     """Clears the current search results and resets pagination."""
#     global last_results, current_page_start
#     last_results = []
#     current_page_start = 0




















"""
src/search.py
---------------------------------------------------------
Comprehensive search module for Terminal-Based Bible App.

Provides:
 - Keyword search (Boyer–Moore, case-insensitive)
 - Reference parsing (book, chapter, verse; ranges & lists)
 - Book-only / chapter-level searches
 - Interactive disambiguation:
     • Book vs Text when input could be both (e.g., 'r')
     • Multiple-book selection when prefix matches many (e.g., 'co')
 - Pagination of results (PAGE_SIZE results per page; next/prev commands)
 - Integration with timestamped history via add_history(query)

Public API:
 - search_verse(bible_tree, query)
 - navigation(command)    # command in {"next","prev"}
 - clear_results()        # optional helper to reset state

Dependencies:
 - history.add_history(query) must be available and should record timestamped history
---------------------------------------------------------
"""

import re
from typing import List, Tuple, Optional
from history import add_history  # your history module should provide add_history(query)

# ---------------------------------------------------------------------
# Globals & configuration
# ---------------------------------------------------------------------
PAGE_SIZE = 20  # number of verses to display per "page"

# last_results: list of tuples (verse_ref, verse_text)
last_results: List[Tuple[str, str]] = []
# start index (0-based) of the current page within last_results
_current_page_start: int = 0


# ---------------------------------------------------------------------
# Utility: Normalization helpers (handles numbered books like "1John")
# ---------------------------------------------------------------------
def _normalize_book_name(name: str) -> str:
    """
    Normalize book names and user input:
      - remove whitespace
      - lower-case
      - keep leading numbers (1,2,3) attached to book name
    Examples:
      "1 Corinthians" -> "1corinthians"
      "  2  Tim  "    -> "2tim"
    """
    if not name:
        return ""
    return "".join(name.split()).lower()


def _find_book_matches(bible_tree: dict, short_name: str) -> List[str]:
    """
    Return list of book keys from bible_tree that start with short_name (normalized).
    Order follows bible_tree.keys() iteration order (usually canonical).
    """
    target = _normalize_book_name(short_name)
    matches = []
    for book_key in bible_tree.keys():
        if _normalize_book_name(book_key).startswith(target):
            matches.append(book_key)
    return matches


def _choose_book_interactive(matches: List[str]) -> Optional[str]:
    """
    If multiple matches found, prompt the user to choose which book they meant.
    Returns selected book key or None (if cancelled).
    """
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]

    print(f"\n Your input matches multiple books:")
    for i, b in enumerate(matches, start=1):
        print(f"   {i}. {b}")

    while True:
        choice = input(f" Enter 1–{len(matches)} to select the correct book (or press Enter to cancel): ").strip()
        if choice == "":
            print(" Selection cancelled.")
            return None
        try:
            idx = int(choice)
            if 1 <= idx <= len(matches):
                selected = matches[idx - 1]
                print(f" Selected: {selected}\n")
                return selected
            else:
                print(" Number out of range. Try again.")
        except ValueError:
            print(" Please enter a valid number.")


# ---------------------------------------------------------------------
# Boyer–Moore (simple bad-character heuristic) - case-insensitive
# ---------------------------------------------------------------------
def boyer_moore_search(text: str, pattern: str) -> int:
    """
    Find first occurrence of pattern in text (case-insensitive).
    Returns index of first match or -1 if not found.
    This implementation uses a simple bad-character skip table.
    """
    if text is None:
        return -1
    if pattern is None:
        return -1
    text_s = text
    pat_s = pattern
    m = len(pat_s)
    n = len(text_s)
    if m == 0:
        return 0
    # build bad-character skip table using lowercase
    skip = {pat_s[i].lower(): m - i - 1 for i in range(m - 1)}
    i = m - 1
    while i < n:
        k = 0
        # compare backwards
        while k < m and pat_s[m - 1 - k].lower() == text_s[i - k].lower():
            k += 1
        if k == m:
            return i - m + 1
        i += skip.get(text_s[i].lower(), m)
    return -1


# ---------------------------------------------------------------------
# Quick keyword check (used to detect ambiguity book vs text)
# ---------------------------------------------------------------------
def _quick_keyword_check(bible_tree: dict, query: str, limit: int = 1) -> bool:
    """
    Quickly scan the Bible for any verse that contains query (case-insensitive).
    Stops early once 'limit' matches are found. Returns True if at least one found.
    Used only to detect ambiguity (book name vs possible text).
    """
    q = (query or "").lower()
    if q == "":
        return False
    found = 0
    for book, chapters in bible_tree.items():
        for chapter, verses in chapters.items():
            for verse_num, text in verses.items():
                if q in (text or "").lower():
                    found += 1
                    if found >= limit:
                        return True
    return False


# ---------------------------------------------------------------------
# Core public function: search_verse
# ---------------------------------------------------------------------
def search_verse(bible_tree: dict, query: str):
    """
    Main entry point to perform a search.

    Behavior:
      - Detects whether query is:
          * reference: e.g., "Col 3:4" or "1Cor 13:4-7"
          * chapter:   e.g., "Col 1"
          * book:      e.g., "Col"  (will disambiguate with text if needed)
          * keyword:   e.g., "love"
      - If the input could be both a book and a word (e.g., "r"), prompts:
          "the letter 'r' matches a book and a word, please type 1 if it is book and 2 if it is word"
      - For ambiguous book-prefixes (e.g., "co"), shows list of matching books for selection.
      - On confirmed search, calls add_history(query) to log timestamped search.
      - Populates results into the global 'last_results' and displays the first page.
    """
    global last_results, _current_page_start
    last_results = []
    _current_page_start = 0

    if not query or not query.strip():
        print(" Empty search. Example usage: search love | search Col 3:4 | search Col 1")
        return

    q = query.strip()

    # patterns
    ref_pattern = r"^([1-3]?\s?[A-Za-z]+)\s+(\d+):([\d,\-\s]+)$"  # Book Chapter:Verses (lists/ranges)
    chapter_pattern = r"^([1-3]?\s?[A-Za-z]+)\s+(\d+)$"           # Book Chapter
    book_pattern = r"^([1-3]?\s?[A-Za-z]+)$"                     # Book only

    # 1) Reference (e.g., "Col 3:4" or "1Cor 13:4-7")
    m = re.match(ref_pattern, q, re.IGNORECASE)
    if m:
        book_raw, chapter, verse_part = m.groups()
        book_raw = book_raw.strip()
        # Find book matches
        matches = _find_book_matches(bible_tree, book_raw)
        if not matches:
            print(f" Book '{book_raw}' not found.")
            return
        # If multiple matches, let user choose interactively
        book_key = _choose_book_interactive(matches)
        if not book_key:
            return
        # Log history and perform reference search
        add_history(q)
        _handle_reference_search(bible_tree, book_key, chapter, verse_part)
        _show_current_page()
        return

    # 2) Book + Chapter (e.g., "Col 1")
    m = re.match(chapter_pattern, q, re.IGNORECASE)
    if m:
        book_raw, chapter = m.groups()
        book_raw = book_raw.strip()
        matches = _find_book_matches(bible_tree, book_raw)
        if matches:
            book_key = _choose_book_interactive(matches)
            if not book_key:
                return
            add_history(q)
            _handle_chapter_search(bible_tree, book_key, chapter)
            _show_current_page()
            return
        else:
            # If no book match, fall back to a text search (but still log)
            add_history(q)
            _handle_text_search(bible_tree, q)
            _show_current_page()
            return

    # 3) Book only (e.g., "Col") - could be book or text (ambiguous)
    m = re.match(book_pattern, q, re.IGNORECASE)
    if m:
        book_raw = m.groups()[0].strip()
        matches = _find_book_matches(bible_tree, book_raw)
        # Check if the same token could be a keyword (exists in verse text)
        keyword_possible = _quick_keyword_check(bible_tree, q, limit=1)

        if matches and keyword_possible:
            # Prompt user: Book or Text?
            print(f"\n The input '{q}' matches a book name and also appears as text in verses.")
            print(" Type 1 to treat input as a Book search (show book/chapter/verse).")
            print(" Type 2 to treat input as a Text/Keyword search (find verses containing the word).")
            choice = input("Enter 1 (Book) or 2 (Text), or press Enter to cancel: ").strip()
            if choice == "1":
                book_key = _choose_book_interactive(matches)
                if not book_key:
                    return
                add_history(q)
                _handle_book_search(bible_tree, book_key)
                _show_current_page()
                return
            elif choice == "2":
                add_history(q)
                _handle_text_search(bible_tree, q)
                _show_current_page()
                return
            else:
                print(" Cancelled.")
                return

        if matches and not keyword_possible:
            # Only book-match -> book search
            book_key = _choose_book_interactive(matches)
            if not book_key:
                return
            add_history(q)
            _handle_book_search(bible_tree, book_key)
            _show_current_page()
            return

        if not matches:
            # No book match -> text search
            add_history(q)
            _handle_text_search(bible_tree, q)
            _show_current_page()
            return

    # 4) Fallback: treat as keyword/text search
    add_history(q)
    _handle_text_search(bible_tree, q)
    _show_current_page()


# ---------------------------------------------------------------------
# Handlers that populate last_results
# ---------------------------------------------------------------------
def _handle_text_search(bible_tree: dict, query: str):
    """
    Populate last_results using keyword search across all verses.
    Uses boyer_moore_search per verse for efficiency (case-insensitive).
    """
    global last_results, _current_page_start
    last_results = []
    _current_page_start = 0
    q = (query or "").lower()
    if q == "":
        return
    for book, chapters in bible_tree.items():
        for chapter, verses in chapters.items():
            for verse_num, text in verses.items():
                if boyer_moore_search((text or "").lower(), q) != -1:
                    last_results.append((f"{book} {chapter}:{verse_num}", text))


def _handle_reference_search(bible_tree: dict, book_key: str, chapter: str, verse_part: str):
    """
    Populate last_results with verses from a specific chapter using verse_part (supports lists and ranges).
    verse_part examples: "4", "2,4-6", "1-3,5"
    """
    global last_results, _current_page_start
    last_results = []
    _current_page_start = 0

    chapter_data = bible_tree.get(book_key, {}).get(chapter)
    if not chapter_data:
        print(f" Chapter {chapter} not found in {book_key}.")
        return

    found_any = False
    for token in verse_part.split(","):
        part = token.strip()
        if "-" in part:
            try:
                s, e = part.split("-", 1)
                s_i = int(s)
                e_i = int(e)
            except ValueError:
                continue
            for v in range(s_i, e_i + 1):
                t = chapter_data.get(str(v))
                if t:
                    last_results.append((f"{book_key} {chapter}:{v}", t))
                    found_any = True
        else:
            t = chapter_data.get(part)
            if t:
                last_results.append((f"{book_key} {chapter}:{part}", t))
                found_any = True

    if not found_any:
        print(f" No matching verse(s) found in {book_key} {chapter} for '{verse_part}'.")


def _handle_chapter_search(bible_tree: dict, book_key: str, chapter: str):
    """
    Populate last_results with all verses in the given chapter.
    """
    global last_results, _current_page_start
    last_results = []
    _current_page_start = 0
    chapter_data = bible_tree.get(book_key, {}).get(chapter)
    if not chapter_data:
        print(f" Chapter {chapter} not found in {book_key}.")
        return
    for verse_num, text in chapter_data.items():
        last_results.append((f"{book_key} {chapter}:{verse_num}", text))


def _handle_book_search(bible_tree: dict, book_key: str):
    """
    Populate last_results with all verses across the given book.
    """
    global last_results, _current_page_start
    last_results = []
    _current_page_start = 0
    book_data = bible_tree.get(book_key, {})
    if not book_data:
        print(f" Book '{book_key}' not found or empty.")
        return
    for chapter, verses in book_data.items():
        for verse_num, text in verses.items():
            last_results.append((f"{book_key} {chapter}:{verse_num}", text))


# ---------------------------------------------------------------------
# Pagination & Navigation
# ---------------------------------------------------------------------
def _show_current_page():
    """
    Display up to PAGE_SIZE verses from last_results starting at _current_page_start.
    Shows page number and total pages.
    """
    global last_results, _current_page_start
    if not last_results:
        print("ℹ No results to display.")
        return

    total = len(last_results)
    start = _current_page_start
    end = min(start + PAGE_SIZE, total)
    page_num = start // PAGE_SIZE + 1
    total_pages = (total - 1) // PAGE_SIZE + 1

    print(f"\n Showing verses {start + 1}–{end} of {total} (Page {page_num} of {total_pages})")
    print("-" * 80)
    for i in range(start, end):
        ref, text = last_results[i]
        print(f"{ref} — {text}")
    print("-" * 80)
    if total_pages > 1:
        print("Use 'next' or 'prev' to navigate pages.")


def navigation(command: str):
    """
    Public navigation function to move pages.
    Accepts 'next' or 'prev'.
    """
    global _current_page_start, last_results
    if not last_results:
        print("ℹ No active search results. Use 'search <query>' to begin.")
        return

    total = len(last_results)
    if command.lower() == "next":
        if _current_page_start + PAGE_SIZE < total:
            _current_page_start += PAGE_SIZE
            _show_current_page()
        else:
            print(" You have reached the end of results.")
    elif command.lower() == "prev":
        if _current_page_start - PAGE_SIZE >= 0:
            _current_page_start -= PAGE_SIZE
            _show_current_page()
        else:
            print(" You are already at the first page.")
    else:
        print(" Invalid navigation command. Use 'next' or 'prev'.")


# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------
def clear_results():
    """Clear current search results and reset pagination state."""
    global last_results, _current_page_start
    last_results = []
    _current_page_start = 0
