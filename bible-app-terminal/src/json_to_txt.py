"""
JSON to TXT Bible Converter
Converts en_kjv.json (downloaded from thiagobodruk/bible)
into bible.txt for the Terminal-Based Bible App.
"""

import json
import os

def convert_json_to_txt():
    # Define file paths
    input_path = os.path.join(os.path.dirname(__file__), "../data/en_kjv.json")
    output_path = os.path.join(os.path.dirname(__file__), "../data/bible.txt")

    # Load JSON data
    with open(input_path, "r", encoding="utf-8") as f:
        bible_data = json.load(f)

    # Write to bible.txt in the correct format
    with open(output_path, "w", encoding="utf-8") as out:
        for book in bible_data["books"]:
            book_name = book["name"]
            for chapter_idx, chapter in enumerate(book["chapters"], start=1):
                for verse_idx, verse_text in enumerate(chapter, start=1):
                    line = f"{book_name} {chapter_idx}:{verse_idx} {verse_text}\n"
                    out.write(line)

    # print("Conversion complete! 'bible.txt' created in /data folder.")

if __name__ == "__main__":
    convert_json_to_txt()
