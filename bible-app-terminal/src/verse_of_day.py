"""
verse_of_day.py
-----------------------------------------------
Displays a random 'Verse of the Day' using a list and Python's random module.
"""

import random


def verse_of_the_day(bible_tree):
    """
    Selects and displays a random verse from the loaded Bible data.
    """
    all_verses = []

    # Flatten the Bible tree into a list of full verse strings
    for book, chapters in bible_tree.items():
        for chapter, verses in chapters.items():
            for verse_num, text in verses.items():
                all_verses.append(f"{book} {chapter}:{verse_num} {text}")

    # Choose one verse randomly
    verse = random.choice(all_verses)
    print("\n Verse of the Day:")
    print(verse)
