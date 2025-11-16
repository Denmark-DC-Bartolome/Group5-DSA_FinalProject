"""
verse_of_day.py
-----------------------------------------------
Displays a random 'Verse of the Day' using a list and Python's random module.
The verse stays the same for 24 hours (Philippine time).
"""

import random
import os
from datetime import datetime, timedelta, timezone

# Philippine Time (UTC+8)
PHT = timezone(timedelta(hours=8))


def verse_of_the_day(bible_tree):
    """
    Selects and displays a random verse from the loaded Bible data.
    Caches the verse for 24 hours so it doesn’t change until the next day.
    """
    cache_file = os.path.join(os.path.dirname(__file__), "../data/verse_cache.txt")

    # Current date (Philippine Time)
    today = datetime.now(PHT).strftime("%Y-%m-%d")

    #  Step 1: Check if verse_cache.txt exists
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            cached_date = f.readline().strip()
            cached_verse = f.readline().strip()

        #  If it’s still the same day → show cached verse
        if cached_date == today and cached_verse:
            print("\n Verse of the Day :")
            print(cached_verse)
            print(f"\n Last updated: {cached_date} (PHT)")
            return

    #  Step 2: Generate a new random verse
    all_verses = []
    for book, chapters in bible_tree.items():
        for chapter, verses in chapters.items():
            for verse_num, text in verses.items():
                all_verses.append(f"{book} {chapter}:{verse_num} {text}")

    verse = random.choice(all_verses)

    #  Step 3: Save today’s verse to verse_cache.txt
    with open(cache_file, "w", encoding="utf-8") as f:
        f.write(today + "\n")
        f.write(verse)

    print("\n Verse of the Day (newly selected):")
    print(verse)
    print(f"\n Last updated: {today} (PHT)")
