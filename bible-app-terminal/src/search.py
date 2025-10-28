"""
search.py
-----------------------------------------------
Handles Bible text searching using the Boyer–Moore algorithm.
Implements efficient substring search within verse text.
"""

from history import history



# # Global variable to store last search results
# last_results = []
# current_index = 0



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


    # last_results.clear()
    # current_index = 0



    for book, chapters in bible_tree.items():
        for chapter, verses in chapters.items():
            for verse_num, text in verses.items():
                # Search for the pattern using Boyer–Moore
                if boyer_moore_search(text.lower(), query.lower()) != -1:
                    print(f"{book} {chapter}:{verse_num} — {text}")
                    found = True
                    history.append(query)

    if not found:
        print("No matching verses found.")