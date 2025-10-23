"""
main.py
-------------------------------------------------
Main entry point for the DSA Final Project:
"Bible Search and Study Application"

Features:
  • Search by keyword, reference, book, or chapter
  • Boyer–Moore text searching for efficiency
  • Interactive navigation ('next' / 'prev')
  • Bookmark system with verse saving
  • Timestamped search history
  • Verse of the Day feature
  • Modular structure for clarity and teamwork
"""

import os
from data_structure import load_bible
from search import search_verse, navigation
from bookmark import add_bookmark, show_bookmarks
from verse_of_day import verse_of_the_day
from history import show_history
from datetime import datetime
from ui import show_help


# FOR FUTURE FEATURES
# # -------------------------------------------------
# #  SELECT BIBLE VERSION
# # -------------------------------------------------
# def choose_bible_version():
#     """Lets the user pick which Bible version to load."""
#     print("\n Choose Bible Version:")
#     print("1. King James Version (KJV - English)")
#     print("2. Ang Dating Biblia 1905 (ADB - Tagalog)")
#     while True:
#         choice = input("Enter 1 or 2: ").strip()
#         if choice == "1":
#             return "../data/bible_kjv.txt", "KJV"
#         elif choice == "2":
#             return "../data/bible_adb.txt", "ADB"
#         else:
#             print(" Invalid input. Please enter 1 or 2.")


# # -------------------------------------------------
# #  LOAD THE CHOSEN VERSION
# # -------------------------------------------------
# def load_bible_version():
#     data_path, version_name = choose_bible_version()
#     abs_path = os.path.join(os.path.dirname(__file__), data_path)
#     print(f"\n Loading {version_name} from: {os.path.abspath(abs_path)}")
#     bible_tree = load_bible(abs_path)
#     print(f" {version_name} loaded successfully!\n")
#     return bible_tree, version_name








# # -------------------------------------------------
# #  MAIN PROGRAM STARTUP
# # -------------------------------------------------
# bible_tree, current_version = load_bible_version()

# print(f" Current Version: {current_version}")
# print("Type 'help' for a list of commands.\n")




# -------------------------------------------------
#  GLOBAL CONFIGURATION
# -------------------------------------------------
# Define path to Bible data file (bible.txt)
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/bible.txt")

# Load Bible data into a hierarchical structure (Book → Chapter → Verse)
bible_tree = load_bible(DATA_PATH)

print(" Welcome to the Bible Search and Study App!")
print("Type 'help' for a list of commands.\n")




# -------------------------------------------------
#  MAIN PROGRAM LOOP
# -------------------------------------------------
def main():
    """Main command loop for user interaction."""
    while True:
        command = input("\n> ").strip()

        # -----------------------------
        # EXIT PROGRAM
        # -----------------------------
        if command.lower() == "exit":
            print(" Exiting Bible Search App. Have a blessed day!")
            break

        # -----------------------------
        # HELP MENU
        # -----------------------------
        elif command.lower() == "help":
            show_help()

        # -----------------------------
        # SEARCH HANDLER
        # -----------------------------
        elif command.lower().startswith("search"):
            # Extract query after the command
            parts = command.split(" ", 1)
            if len(parts) < 2:
                print(" Usage: search <keyword/book/ref>")
            else:
                query = parts[1]
                search_verse(bible_tree, query, show_history)

        # -----------------------------
        # NAVIGATION HANDLER
        # -----------------------------
        elif command.lower() == "next":
            navigation("next")

        elif command.lower() == "prev":
            navigation("prev")

        # -----------------------------
        # BOOKMARKS HANDLER
        # -----------------------------
        elif command.lower().startswith("bookmark"):
            parts = command.split(" ", 2)
            if len(parts) < 3:
                print(" Usage: bookmark <Book> <Chapter:Verse>")
            else:
                book, chap_verse = parts[1], parts[2]
                ref = f"{book} {chap_verse}"
                try:
                    chapter, verse = chap_verse.split(":")
                    verse_text = bible_tree[book][chapter][verse]
                    add_bookmark(ref, verse_text)
                except KeyError:
                    print(" Invalid verse reference. Please check your input.")

        elif command.lower() == "bookmarks":
            show_bookmarks()

        # -----------------------------
        # SEARCH HISTORY HANDLER
        # -----------------------------
        elif command.lower().startswith("history"):
            parts = command.split(" ", 1)
            if len(parts) > 1 and parts[1].isdigit():
                limit = int(parts[1])
                show_history(limit)
            else:
                show_history()

    # Shell
    #   history 5 (shows only 5 searchess)


        # -----------------------------
        # VERSE OF THE DAY
        # -----------------------------
        elif command.lower() == "verseofday":
            verse_of_the_day(bible_tree)

        # -----------------------------
        # UNKNOWN COMMAND HANDLER
        # -----------------------------
        else:
            print(" Unknown command. Type 'help' for available options.")


# -------------------------------------------------
#  PROGRAM ENTRY POINT
# -------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Program terminated. Have a blessed day!")
