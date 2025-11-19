"""
indexer.py
Builds a search index (inverted index) from bible.txt.
Creates `data/index.json` used by search.py for ultra-fast searches.
"""

import os
import json
from collections import defaultdict
from data_structure import load_bible   # reuse your existing loader

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/bible.txt")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "../data/index.json")

def build_index(bible_tree):
    inverted = defaultdict(list)

    for book, chapters in bible_tree.items():
        for chapter, verses in chapters.items():
            for verse_num, text in verses.items():
                ref = f"{book} {chapter}:{verse_num}"
                words = text.lower().split()

                for w in words:
                    w = ''.join(c for c in w if c.isalnum())  # clean punctuation
                    if w:
                        inverted[w].append(ref)

    return inverted

def main():
    print("Loading Bible...")
    bible_tree = load_bible(DATA_PATH)

    print("Building index (this may take a few seconds)...")
    index = build_index(bible_tree)

    print("Saving index...")
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump({"inverted_index": index}, f, ensure_ascii=False, indent=2)

    print("Index built successfully!")

if __name__ == "__main__":
    main()
