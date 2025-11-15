"""
search.py
-----------------------------------------------
Handles Bible text searching using the Boyer–Moore algorithm.
Implements efficient substring search within verse text.
"""
import re
from history import add_history
from ui import clear_screen, show_commands



# # Global variable to store last search results
last_results = []
current_index = 0



def boyer_moore_search(text, pattern):
    """
    Boyer–Moore Algorithm for string search.
    Efficiently finds the index of the first occurrence of 'pattern' in 'text'.
    Returns -1 if the pattern is not found.
    """
    m = len(pattern)
    n = len(text)

    if m == 0:
        return 0

    # Preprocessing: build the bad character skip table
    skip = {pattern[i]: m - i - 1 for i in range(m - 1)}
    i = m - 1  # current index in text

    while i < n:
        k = 0
        # Compare backwards from the end of the pattern
        while k < m and pattern[m - 1 - k].lower() == text[i - k].lower():
            k += 1
        # If full pattern matched
        if k == m:
            return i - m + 1
        # Otherwise, skip ahead based on mismatch
        i += skip.get(text[i], m)

    return -1


def search_verse(bible_tree, query, history):
    """
    Searches for all verses containing the given query.
    Prints matches and stores the query in the history queue.
    """
    print(f"\n Searching for: {query}")
    found = False


    last_results.clear()
    current_index = 0



    for book, chapters in bible_tree.items():
        for chapter, verses in chapters.items():
            for verse_num, text in verses.items():
                # Search for the pattern using Boyer–Moore
                if boyer_moore_search(text.lower(), query.lower()) != -1:
                    verse_ref = f"{book} {chapter}:{verse_num}"
                    last_results.append((verse_ref, text))
                    found = True
    if found:
        add_history(query)
        clear_screen()
        print(f"  Found {len(last_results)} result(s). Type 'next' or 'prev' to navigate.")
        show_current_verse()
        show_commands()
    else:
        clear_screen()
        print("No matching verses found.")
        show_commands()

def show_current_verse():
    """Displays the currently selected verse."""
    global current_index
    if not last_results:
        clear_screen()
        print("No active search results. Use 'search <keyword>' first.")
        show_commands()
        return

    verse_ref, text = last_results[current_index]
    print(f"\n {verse_ref} — {text}")
    print(f"({current_index + 1} of {len(last_results)})")


def navigation(command):
    """
    Moves to the next or previous verse in the current search results.
    Command: 'next' or 'prev'
    """
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


# from history import add_history

# """
# search.py
# -----------------------------------------------
# Handles Bible text searching using the Boyer–Moore algorithm.
# Implements efficient substring search within verse text.
# """

# from history import add_history



# # # Global variable to store last search results
# # last_results = []
# # current_index = 0



# def boyer_moore_search(text, pattern):
#     """
#     Boyer–Moore Algorithm for string search.
#     Efficiently finds the index of the first occurrence of 'pattern' in 'text'.
#     Returns -1 if the pattern is not found.
#     """
#     m = len(pattern)
#     n = len(text)

#     if m == 0:
#         return 0

#     # Preprocessing: build the bad character skip table
#     skip = {pattern[i]: m - i - 1 for i in range(m - 1)}
#     i = m - 1  # current index in text

#     while i < n:
#         k = 0
#         # Compare backwards from the end of the pattern
#         while k < m and pattern[m - 1 - k].lower() == text[i - k].lower():
#             k += 1
#         # If full pattern matched
#         if k == m:
#             return i - m + 1
#         # Otherwise, skip ahead based on mismatch
#         i += skip.get(text[i], m)

#     return -1


# def search_verse(bible_tree, query, history):
#     """
#     Searches for all verses containing the given query.
#     Prints matches and stores the query in the history queue.
#     """
#     print(f"\n Searching for: {query}")
#     found = False


#     # last_results.clear()
#     # current_index = 0



#     for book, chapters in bible_tree.items():
#         for chapter, verses in chapters.items():
#             for verse_num, text in verses.items():
#                 # Search for the pattern using Boyer–Moore
#                 if boyer_moore_search(text.lower(), query.lower()) != -1:
#                     verse_ref = f"{book} {chapter}:{verse_num}"
#                     last_results.append((verse_ref, text))
#                     found = True
#     if found:
#         add_history(query)
#         print(f"  Found {len(last_results)} result(s). Type 'next' or 'prev' to navigate.")
#         show_current_verse()
#     else:
#         print("No matching verses found.")

# def show_current_verse():
#     """Displays the currently selected verse."""
#     global current_index
#     if not last_results:
#         print("No active search results. Use 'search <keyword>' first.")
#         return

#     verse_ref, text = last_results[current_index]
#     print(f"\n {verse_ref} — {text}")
#     print(f"({current_index + 1} of {len(last_results)})")


# def navigation(command):
#     """
#     Moves to the next or previous verse in the current search results.
#     Command: 'next' or 'prev'
#     """
#     global current_index
#     if not last_results:
#         print("No active search results. Use 'search' first.")
#         return

#     if command == "next":
#         if current_index < len(last_results) - 1:
#             current_index += 1
#         else:
#             print(" End of results reached.")
#     elif command == "prev":
#         if current_index > 0:
#             current_index -= 1
#         else:
#             print(" You're at the first verse.")
#     else:
#         print("Invalid navigation command. Use 'next' or 'prev'.")

#     show_current_verse()


# from history import add_history

# """
# search.py
# -----------------------------------------------
# Handles Bible text searching using the Boyer–Moore algorithm.
# Implements efficient substring search within verse text.
# """

# from history import add_history

# # Global variable to store last search results
# last_results = []
# current_index = 0


# def boyer_moore_search(text, pattern):
#     """
#     Boyer–Moore Algorithm for string search.
#     Efficiently finds the index of the first occurrence of 'pattern' in 'text'.
#     Returns -1 if the pattern is not found.
#     """
#     m = len(pattern)
#     n = len(text)

#     if m == 0:
#         return 0

#     # Preprocessing: build the bad character skip table
#     skip = {pattern[i]: m - i - 1 for i in range(m - 1)}
#     i = m - 1  # current index in text

#     while i < n:
#         k = 0
#         # Compare backwards from the end of the pattern
#         while k < m and pattern[m - 1 - k].lower() == text[i - k].lower():
#             k += 1
#         # If full pattern matched
#         if k == m:
#             return i - m + 1
#         # Otherwise, skip ahead based on mismatch
#         i += skip.get(text[i], m)

#     return -1


# def search_verse(bible_tree, query, history):
#     """
#     Searches for all verses containing the given query.
#     Prints matches and stores the query in the history queue.
#     """
#     print(f"\n Searching for: {query}")
#     found = False

#     last_results.clear()
#     current_index = 0


#      for book, chapters in bible_tree.items():
#         for chapter, verses in chapters.items():
#             for verse_num, text in verses.items():
#                 # Search for the pattern using Boyer–Moore
#                 if boyer_moore_search(text.lower(), query.lower()) != -1:
#                     verse_ref = f"{book} {chapter}:{verse_num}"
#                     last_results.append((verse_ref, text))
#                     found = True
#     if found:
#         add_history(query)
#         print(f"  Found {len(last_results)} result(s). Type 'next' or 'prev' to navigate.")
#         show_current_page()
#     else:
#         print("No matching verses found.")


# # -------------------------------------------------
# #  PAGINATED NAVIGATION (20 verses per page)
# # -------------------------------------------------
# PAGE_SIZE = 20  # Number of verses to display at once


# def show_current_page():
#     """Displays up to PAGE_SIZE verses starting from the current index."""
#     global current_index
#     if not last_results:
#         print(" No active search results. Use 'search' first.")
#         return

#     start = current_index
#     end = min(start + PAGE_SIZE, len(last_results))

#     print(f"\n Showing verses {start + 1}–{end} of {len(last_results)}:\n")
#     print("=" * 70)

#     for i in range(start, end):
#         verse_ref, text = last_results[i]
#         print(f"{verse_ref} — {text}")

#     print("=" * 70)
#     print(f"📘 Page {start // PAGE_SIZE + 1} of {(len(last_results) - 1) // PAGE_SIZE + 1}")
#     print("Use 'next' or 'prev' to navigate.\n")


# def navigation(command):
#     """Handles navigation commands ('next' / 'prev') for paginated results."""
#     global current_index
#     if not last_results:
#         print(" No active search results. Use 'search' first.")
#         return

#     if command == "next":
#         if current_index + PAGE_SIZE < len(last_results):
#             current_index += PAGE_SIZE
#             show_current_page()
#         else:
#             print(" You’ve reached the end of the results.")
#     elif command == "prev":
#         if current_index - PAGE_SIZE >= 0:
#             current_index -= PAGE_SIZE
#             show_current_page()
#         else:
#             print(" You’re already at the first page.")
#     else:
#         print(" Invalid navigation command. Use 'next' or 'prev'.")