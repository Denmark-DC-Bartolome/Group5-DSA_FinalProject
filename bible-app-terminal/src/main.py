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
from search import search_verse, navigation, _find_book_matches, _choose_book_interactive, clear_results
from bookmark import add_bookmark, show_bookmarks, bookmarks
from verse_of_day import verse_of_the_day
from history import history, show_history
from datetime import datetime
from ui import *


# FOR FUTURE FEATURES (Bible Translation)
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
# cache_file = os.path.join(os.path.dirname(__file__), "../data/verse_cache.txt")


# Load Bible data into a hierarchical structure (Book → Chapter → Verse)
bible_tree = load_bible(DATA_PATH)





#Welcome message (landing screen)
def welcome():
    clear_screen()
    book = [
    "\t\t           __...--~~~~~-._   _.-~~~~~--...__",
    "\t\t         //               `V'               \\\\ ",
    "\t\t        //                 |                 \\\\ ",
    "\t\t       //__...--~~~~~~-._  |  _.-~~~~~~--...__\\\\ ",
    "\t\t      //__.....----~~~~._\\ | /_.~~~~----.....__\\\\",
    "\t\t     ====================\\\\|//====================",
    "\t\t                          `---`"
    ]

    for line in book:
        print(BLUE + line)
    print("\t\t      Welcome to the Bible Search and Study App!"  + RESET)
    show_commands()

# -------------------------------------------------
#  MAIN PROGRAM LOOP
# -------------------------------------------------
def main():
    """Main command loop for user interaction."""
    while True:
        command = input("\n> ").strip()

        # -----------------------------
        # BLANK INPUT HANDLER
        # -----------------------------
        if command == "":
            print("Enter a valid command.")
            continue

        # -----------------------------
        # HOME FUNCTION
        # -----------------------------
        if command.lower() == "home":
            clear_results()
            return welcome()
        
        # -----------------------------
        # EXIT PROGRAM
        # -----------------------------
        if command.lower() == "exit":
            print(" Exiting Bible Search App. Have a blessed day!")
            clear_screen()
            break

        # -----------------------------
        # SEARCH HANDLER
        # -----------------------------
        elif command.lower().startswith("search"):
            parts = command.split(" ", 1)

            # If user typed only "search"
            if len(parts) == 1 or not parts[1].strip():
                print("💡 Usage: search <keyword>")
                continue

            query = parts[1].strip()
            search_verse(bible_tree, query)



        

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

        # -------------OLD BOOKMARK-------


        # elif command.lower()== "bookmark":
        #     parts = command.split(" ", 2)
        #     if len(parts) < 3:
        #         show_commands()
        #         print("💡 Usage: bookmark <Book> <Chapter:Verse>")
        #     else:
        #         book, chap_verse = parts[1], parts[2]
        #         ref = f"{book} {chap_verse}"
        #         try:
        #             chapter, verse = chap_verse.split(":")
        #             verse_text = bible_tree[book][chapter][verse]
        #             add_bookmark(ref, verse_text)
        #         except KeyError:
        #             show_commands()
        #             print(" Invalid verse reference. Please check your input.")

        # elif command.lower() == "bookmarks":
        #     clear_screen()
        #     show_bookmarks()
        #     show_commands()



 
#  ------------------TESTING---------------------------------



        elif command.lower().split()[0] == "bookmark":
            parts = command.split(" ", 2)

            if len(parts) < 3:
                print("💡Usage: bookmark <Book> <Chapter:Verse>")
                continue

            user_book = parts[1].strip()
            chap_verse = parts[2].strip()

            # Parse chapter:verse
            try:
                chapter, verse = chap_verse.split(":")
            except ValueError:
                clear_screen()
                print(" Invalid format. Use: chapter:verse (e.g., 3:16)")
                show_commands()
                continue

            # Match book using search.py logic
            matches = _find_book_matches(bible_tree, user_book)

            if not matches:
                clear_screen()
                print(f" No book found matching '{user_book}'.")
                show_commands()
                continue

            # Let user choose if multiple
            book_key = _choose_book_interactive(matches)
            if not book_key:
                continue

            # Fetch verse safely
            try:
                verse_text = bible_tree[book_key][chapter][verse]
            except KeyError:
                clear_screen()
                print(" Chapter or verse not found.")
                show_commands()
                continue

            ref = f"{book_key} {chapter}:{verse}"
            add_bookmark(ref, verse_text)

        # -----------------------------
        # BOOKMARKS DISPLAY HANDLER
        # -----------------------------
        elif command.lower() == "bookmarks":
            clear_screen()
            show_commands()
            show_bookmarks()


        # -----------------------------
        # SEARCH HISTORY HANDLER
        # -----------------------------
        elif command.lower().startswith("history"):
            parts = command.split(" ", 1)
            if len(parts) > 1 and parts[1].isdigit():
                limit = int(parts[1])
                show_commands()               
                show_history(limit)
            else:
                clear_screen()
                show_history()
                show_commands()

    # Shell
    #   history 5 (shows only 5 searchess)


        # -----------------------------
        # VERSE OF THE DAY
        # -----------------------------
        elif command.lower() == "verseofday":
            clear_screen()
            show_commands()
            verse_of_the_day(bible_tree)
            

        # -----------------------------
        # UNKNOWN COMMAND HANDLER
        # -----------------------------
        else:
            print(" Unknown command. The available options are displayed above.")


# -------------------------------------------------
#  PROGRAM ENTRY POINT
# -------------------------------------------------
if __name__ == "__main__":
    try:
        welcome()
        main()
    except KeyboardInterrupt:
        print("\n Program terminated. Have a blessed day!")
