"""
data_structure.py
-----------------------------------------------
Responsible for loading and structuring the Bible text data.
Uses a hierarchical tree-like dictionary format:
Book → Chapter → Verse → Text
"""

def load_bible(file_path):
    """
    Loads the Bible from a text file into a nested dictionary structure.
    Expected line format: Book Chapter:Verse Text
    Example: Genesis 1:1 In the beginning God created the heaven and the earth.
    """
    bible_tree = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                # Split line into book, reference, and text
                book, ref, verse_text = line.strip().split(" ", 2)
                chapter, verse = ref.split(":")
            except ValueError:
                continue  # Skip malformed lines

            # Build nested structure dynamically
            if book not in bible_tree:
                bible_tree[book] = {}
            if chapter not in bible_tree[book]:
                bible_tree[book][chapter] = {}

            bible_tree[book][chapter][verse] = verse_text

    return bible_tree
