"""
bookmark.py
-----------------------------------------------
Handles the bookmark feature using a hash table (Python dictionary).
Allows users to store and retrieve bookmarked verses quickly.
"""

# Global hash table to store bookmarked verses
bookmarks = {}


def add_bookmark(ref, verse_text):
    """
    Adds a verse to the user's bookmarks.
    Key: verse reference (e.g., 'John 3:16')
    Value: verse text
    """
    bookmarks[ref] = verse_text
    print(f" Added bookmark: {ref}")


def show_bookmarks():
    """
    Displays all bookmarked verses in the console.
    """
    if not bookmarks:
        print("No bookmarks yet.")
    else:
        print("\n Bookmarked Verses:")
        for ref, text in bookmarks.items():
            print(f"{ref} — {text}")
