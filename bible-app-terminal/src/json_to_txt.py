import json
import os

def convert_json_to_txt():
    """Converts the Bible JSON (en_kjv.json) into bible.txt for the main app."""
    input_path = os.path.join(os.path.dirname(__file__), "../data/en_kjv.json")
    output_path = os.path.join(os.path.dirname(__file__), "../data/bible.txt")

    # Make sure the file exists
    if not os.path.exists(input_path):
        print(" JSON file not found! Make sure en_kjv.json is in the /data folder.")
        return

    # Handle UTF-8 BOM automatically
    with open(input_path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    #  Handle both formats (with or without "books" key)
    if isinstance(data, dict) and "books" in data:
        books = data["books"]
    elif isinstance(data, list):
        books = data
    else:
        print(" Unsupported JSON format. Check your en_kjv.json structure.")
        return

    # Write the converted file
    total_verses = 0
    with open(output_path, "w", encoding="utf-8") as out:
        for book in books:
            name = book["name"]
            for c_idx, chapter in enumerate(book["chapters"], start=1):
                for v_idx, verse in enumerate(chapter, start=1):
                    out.write(f"{name} {c_idx}:{v_idx} {verse.strip()}\n")
                    total_verses += 1

    print(f" Conversion complete! Created {total_verses:,} verses at {output_path}")

if __name__ == "__main__":
    convert_json_to_txt()
