"""
search.py
-------------------------------------------------
Manages all Bible search functionalities for the DSA Final Project.
"""

import re
from history import add_history

# Stores the most recent search results and current index for navigation
last_results = []
current_index = 0


# -------------------------------------------------
#  BOYER–MOORE SEARCH ALGORITHM
# -------------------------------------------------
def boyer_moore_search(text, pattern):
    """
    Boyer–Moore substring search algorithm.
    Efficiently finds 'pattern' within 'text' using skip heuristics.
    Returns:
        int: Index of the match start, or -1 if not found.
    """
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0

    # Preprocess: create skip table
    skip = {pattern[i]: m - i - 1 for i in range(m - 1)}
    i = m - 1

    # Main search loop
    while i < n:
        k = 0
        while k < m and pattern[m - 1 - k].lower() == text[i - k].lower():
            k += 1
        if k == m:
            return i - m + 1  # Found match
        i += skip.get(text[i], m)
    return -1


# -------------------------------------------------
#  MAIN SEARCH HANDLER
# -------------------------------------------------
def search_verse(bible_tree, query, history):
    """
    Main search entry point.
    Automatically detects the type of search:
      • Keyword: e.g., "search love"
      • Book: e.g., "search Col"
      • Book + Chapter: e.g., "search Col 1"
      • Reference: e.g., "search Col 3:4" or "search Col 2:2,4-6"
    """
    global last_results, current_index
    print(f"\n Searching for: {query}")
    last_results.clear()
    current_index = 0
    query = query.strip()

    # Regex patterns for different query types
    ref_pattern = r"^([1-3]?\s?[A-Za-z]+)\s+(\d+):([\d,\-\s]+)$"  # Book + Chapter:Verses
    chapter_pattern = r"^([1-3]?\s?[A-Za-z]+)\s+(\d+)$"            # Book + Chapter
    book_pattern = r"^([1-3]?\s?[A-Za-z]+)$"                       # Book only

    # 1 Book + Chapter:Verse(s)
    if re.match(ref_pattern, query, re.IGNORECASE):
        book, chapter, verse_part = re.match(ref_pattern, query, re.IGNORECASE).groups()
        book = book.capitalize().replace(" ", "")
        add_history(query)
        handle_reference_search(bible_tree, book, chapter, verse_part)

    # 2 Book + Chapter (e.g., "Col 1")
    elif re.match(chapter_pattern, query, re.IGNORECASE):
        book, chapter = re.match(chapter_pattern, query, re.IGNORECASE).groups()
        book = book.capitalize().replace(" ", "")
        add_history(query)
        handle_chapter_search(bible_tree, book, chapter)

    # 3 Book Only (e.g., "Col")
    elif re.match(book_pattern, query, re.IGNORECASE):
        book = re.match(book_pattern, query, re.IGNORECASE).groups()[0]
        book = book.capitalize().replace(" ", "")
        possible_book = find_book_key(bible_tree, book)

        # Smart check: maybe user means the word "Col", not the book "Colossians"
        if possible_book:
            print(f"\n '{book}' could refer to a Bible book or a search keyword.")
            choice = input(" Type 'b' for Book search or 't' for Text search: ").strip().lower()

            if choice == "b":
                add_history(query)
                handle_book_search(bible_tree, book)
            elif choice == "t":
                handle_text_search(bible_tree, query, history)
            else:
                print(" Invalid choice. Cancelled search.")
        else:
            # No matching book → treat as text search
            handle_text_search(bible_tree, query, history)

    # 4 Fallback: keyword/text search
    else:
        handle_text_search(bible_tree, query, history)


# -------------------------------------------------
#  TEXT SEARCH HANDLER
# -------------------------------------------------
def handle_text_search(bible_tree, query, history):
    """
    Searches the entire Bible for a keyword (case-insensitive).
    Uses Boyer–Moore algorithm for efficiency.
    """
    global last_results
    found = False

    for book, chapters in bible_tree.items():
        for chapter, verses in chapters.items():
            for verse_num, text in verses.items():
                if boyer_moore_search(text.lower(), query.lower()) != -1:
                    verse_ref = f"{book} {chapter}:{verse_num}"
                    last_results.append((verse_ref, text))
                    found = True

    if found:
        add_history(query)
        print(f" Found {len(last_results)} result(s). Type 'next' or 'prev' to navigate.")
        show_current_verse()
    else:
        print(" No matching verses found.")


# -------------------------------------------------
#  REFERENCE SEARCH HANDLER
# -------------------------------------------------
def handle_reference_search(bible_tree, book, chapter, verse_part):
    """
    Handles reference-based searches (e.g., 'Col 3:4' or 'Col 2:2,4-6').
    Supports single verses, comma-separated lists, and ranges.
    """
    global last_results
    last_results.clear()
    found = False

    try:
        book_key = find_book_key(bible_tree, book)
        if not book_key:
            return

        chapter_data = bible_tree[book_key].get(chapter)
        if not chapter_data:
            print(f" Chapter {chapter} not found in {book_key}.")
            return

        # Parse verses like "2,4-6"
        for part in verse_part.split(","):
            part = part.strip()
            if "-" in part:
                start, end = part.split("-")
                for v in range(int(start), int(end) + 1):
                    verse_text = chapter_data.get(str(v))
                    if verse_text:
                        ref = f"{book_key} {chapter}:{v}"
                        last_results.append((ref, verse_text))
                        found = True
            else:
                verse_text = chapter_data.get(part)
                if verse_text:
                    ref = f"{book_key} {chapter}:{part}"
                    last_results.append((ref, verse_text))
                    found = True

        if found:
            print(f" Found {len(last_results)} verse(s). Type 'next' or 'prev' to navigate.")
            show_current_verse()
        else:
            print(f" Verse(s) not found in {book_key} {chapter}.")

    except Exception as e:
        print(f" Error processing reference: {e}")


# -------------------------------------------------
#  CHAPTER & BOOK SEARCH HANDLERS
# -------------------------------------------------
def handle_chapter_search(bible_tree, book, chapter):
    """Displays all verses in a specific chapter (e.g., 'Col 1')."""
    global last_results
    last_results.clear()
    found = False

    book_key = find_book_key(bible_tree, book)
    if not book_key:
        return

    chapter_data = bible_tree[book_key].get(chapter)
    if not chapter_data:
        print(f" Chapter {chapter} not found in {book_key}.")
        return

    for verse_num, verse_text in chapter_data.items():
        ref = f"{book_key} {chapter}:{verse_num}"
        last_results.append((ref, verse_text))
        found = True

    if found:
        print(f" Showing all {len(last_results)} verses from {book_key} {chapter}.")
        show_current_verse()
    else:
        print(f" No verses found in {book_key} {chapter}.")


def handle_book_search(bible_tree, book):
    """Displays all verses in a book (e.g., 'Col')."""
    global last_results
    last_results.clear()
    found = False

    book_key = find_book_key(bible_tree, book)
    if not book_key:
        return

    for chapter, verses in bible_tree[book_key].items():
        for verse_num, verse_text in verses.items():
            ref = f"{book_key} {chapter}:{verse_num}"
            last_results.append((ref, verse_text))
            found = True

    if found:
        print(f" Showing all {len(last_results)} verses from {book_key}.")
        show_current_verse()
    else:
        print(f" No verses found in {book_key}.")


# -------------------------------------------------
#  BOOK NAME RESOLUTION (WITH INTERACTIVE DISAMBIGUATION)
# -------------------------------------------------
def find_book_key(bible_tree, short_name):
    """
    Matches user input to a valid Bible book name.
    - Accepts partial matches (e.g., 'Col' → 'Colossians')
    - If multiple matches exist, prompts user to choose interactively.
    """
    short_name = short_name.lower()
    matches = [book for book in bible_tree.keys() if book.lower().startswith(short_name)]

    if not matches:
        print(f" No book found for '{short_name}'. Try typing more letters.")
        return None

    # Single exact match → return immediately
    if len(matches) == 1:
        return matches[0]

    # Multiple matches → interactive user selection
    print(f"\n Your input '{short_name}' matches multiple books:")
    for idx, match in enumerate(matches, start=1):
        print(f"   {idx}. {match}")

    while True:
        try:
            choice = input(f" Enter 1–{len(matches)} to select the correct book: ").strip()
            if not choice:
                print(" Cancelled. Please type a more specific book name next time.")
                return None
            choice = int(choice)
            if 1 <= choice <= len(matches):
                selected = matches[choice - 1]
                print(f" Selected: {selected}\n")
                return selected
            else:
                print(" Invalid number. Try again.")
        except ValueError:
            print(" Please enter a valid number.")


# -------------------------------------------------
#  NAVIGATION SYSTEM
# -------------------------------------------------
def show_current_verse():
    """Displays the current verse result."""
    global current_index
    if not last_results:
        print("No active search results. Use 'search <keyword>' first.")
        return

    verse_ref, text = last_results[current_index]
    print(f"\n {verse_ref} — {text}")
    print(f"({current_index + 1} of {len(last_results)})")


def navigation(command):
    """Handles navigation commands ('next' / 'prev')."""
    global current_index
    if not last_results:
        print("No active search results. Use 'search' first.")
        return

    if command == "next":
        if current_index < len(last_results) - 1:
            current_index += 1
        else:
            print(" End of results reached.")
    elif command == "prev":
        if current_index > 0:
            current_index -= 1
        else:
            print(" You're at the first verse.")
    else:
        print("Invalid navigation command. Use 'next' or 'prev'.")

    show_current_verse()
