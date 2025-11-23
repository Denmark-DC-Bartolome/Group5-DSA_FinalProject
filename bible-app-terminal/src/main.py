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

import re   
import os
from data_structure import load_bible
from search import search_verse, navigation, _find_book_matches, _choose_book_interactive, clear_results

from bookmark import add_bookmark, show_bookmarks, bookmarks, remove_bookmark, remove_bookmarks_bulk, clear_all_bookmarks
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



# ensure outputs folder exists early (helps when running from IDE)
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "../outputs")
if not os.path.exists(OUTPUTS_DIR):
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

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
        print(line)
    print(CYAN+ BOLD + "\t\t      Welcome to the Bible Search and Study App!" + RESET)
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
            print(RED +"Enter a valid command." + RESET)
            continue

        
        # -----------------------------
        # EXIT PROGRAM
        # -----------------------------
        if command.lower() == "exit":
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
                print(CYAN + line)
            print(CYAN+ BOLD +" \t\t     Exiting Bible Search App. Have a blessed day!" + RESET)
            break

        # -----------------------------
        # SEARCH HANDLER
        # -----------------------------
        elif command.lower().startswith("search"):
            parts = command.split(" ", 1)
            clear_results()
            # If user typed only "search"
            if len(parts) == 1 or not parts[1].strip():
                print(YELLOW + "💡 Usage: search <keyword>" + RESET)
                continue

            query = parts[1].strip()
            search_verse(bible_tree, query)



        # -----------------------------
        # MENU (help) - avoid stopping program
        # -----------------------------
        elif command.lower() == "home":
            clear_results()
            clear_screen()
            welcome()
            continue




        

        # -----------------------------
        # NAVIGATION HANDLER
        # -----------------------------
        elif command.lower() == "next":
            navigation("next")

        elif command.lower() == "prev":
            navigation("prev")


        # -----------------------------
        # BOOKMARKS DISPLAY HANDLER
        # -----------------------------
        elif command.lower() == "bookmarks":
            clear_screen()
            clear_results()
            show_bookmarks()
            show_commands()
            continue




        # -----------------------------
        # SEARCH HISTORY HANDLER
        # -----------------------------
        elif command.lower().startswith("history"):
            parts = command.split(" ", 1)
            clear_results()
            if len(parts) > 1 and parts[1].isdigit():
                limit = int(parts[1])
                show_commands()               
                show_history(limit)
            else:
                clear_screen()
                show_history()
                show_commands()


        # Make sure at top of main.py you import these:
        # from bookmark import add_bookmark, show_bookmarks, bookmarks, remove_bookmark, remove_bookmarks_bulk, clear_all_bookmarks

        # -----------------------------
        # BOOKMARK REMOVE / CLEAR HANDLER (robust parsing)
        # -----------------------------
        elif command.lower().startswith("bookmark remove") or command.lower().startswith("bookmark del"):
            # Accept syntax:
            #   bookmark remove <Book Name> <chapter:verse[ -end] [, chapter:verse ...]>
            # Examples:
            #   bookmark remove John 1:1-3
            #   bookmark remove John 1:1,1:3,1:5
            #   bookmark remove "2 Peter" 1:1-2
            m = re.match(r"^bookmark\s+(?:remove|del)\s+(.+?)\s+(.+)$", command, flags=re.IGNORECASE)
            if not m:
                clear_screen()
                show_commands()
                print(" Usage: bookmark remove <Book Name> <chapter:verse>  (e.g., bookmark remove John 1:1-3 or bookmark remove John 1:1,1:3)")
                continue

            user_book = m.group(1).strip()
            chap_verse_input = m.group(2).strip()

            # Resolve candidate books (keeps behavior consistent with add_bookmark)
            matches = _find_book_matches(bible_tree, user_book)
            if not matches:
                clear_screen()
                show_commands()
                print(f" No book found matching '{user_book}'.")
                continue

            book_key = _choose_book_interactive(matches)
            if not book_key:
                # user cancelled selection
                clear_screen()
                show_commands()
                continue

            # Robust parser: find all occurrences of "chapter:verse" or "chapter:verse-range"
            # Example matches it will find: "1:1", "1:1-3", "2:4-6"
            refs_to_remove = []
            # pattern: chapter:verse or chapter:verse-range
            for match in re.finditer(r"(\d+)\s*:\s*(\d+(?:\s*-\s*\d+)?)", chap_verse_input):
                chapter_part = match.group(1)
                verse_part = match.group(2).replace(" ", "")  # remove spaces like "1 - 3" -> "1-3"

                if "-" in verse_part:
                    s_str, e_str = verse_part.split("-", 1)
                    try:
                        s = int(s_str); e = int(e_str)
                    except ValueError:
                        continue
                    # expand range
                    for v in range(s, e + 1):
                        refs_to_remove.append(f"{book_key} {chapter_part}:{v}")
                else:
                    # single verse
                    refs_to_remove.append(f"{book_key} {chapter_part}:{verse_part}")

            # If user typed only verse numbers without chapter (like "1-3" or "1,3"),
            # try to extract a leading chapter from the input (e.g., "1:1-3,4,5" -> already handled).
            # But if no chapter:verse tokens found, attempt a fallback:
            if not refs_to_remove:
                # Try pattern: single chapter provided once, followed by verse numbers "chapter: verses-maybe"
                # Example: "1:1-3,5" would have matched earlier. If user typed "1 1-3" (unlikely), we try:
                simple = re.match(r"^(\d+)\s+(.+)$", chap_verse_input)
                if simple:
                    chapter_part = simple.group(1)
                    rest = simple.group(2)
                    # split by comma and handle ranges
                    for token in re.split(r"\s*,\s*", rest):
                        token = token.strip()
                        if "-" in token:
                            try:
                                s, e = map(int, token.split("-", 1))
                                for v in range(s, e + 1):
                                    refs_to_remove.append(f"{book_key} {chapter_part}:{v}")
                            except ValueError:
                                continue
                        elif token.isdigit():
                            refs_to_remove.append(f"{book_key} {chapter_part}:{token}")

            if not refs_to_remove:
                clear_screen()
                show_commands()
                print("❗ Could not parse chapter:verse input. Use forms like '1:1-3' or '1:1,1:3'.")
                continue

            # Remove duplicates and keep stable order
            refs_to_remove = list(dict.fromkeys(refs_to_remove))

            # Call bulk removal function from bookmark module
            removed, not_found = remove_bookmarks_bulk(refs_to_remove)
            # removed is count, not_found list printed by remove_bookmarks_bulk already
            continue

        elif command.lower().strip() in ("bookmarks clear", "bookmark clear"):
            clear_screen()
            show_commands()
            confirm = input("Are you sure you want to CLEAR ALL bookmarks? Type 'yes' to confirm: ").strip().lower()
            if confirm == "yes":
                clear_all_bookmarks()
            else:
                print("Cancelled.")
            continue











        # -----------------------------
        # BOOKMARKS HANDLER (robust, supports ranges/lists)
        # -----------------------------
        elif command.lower().startswith("bookmark"):
            # Regex captures: bookmark <book name> <chapter>:<verses>
            # verses can be e.g. "1", "1-3", "1,3-5,8", spaces allowed
            m = re.match(r"^bookmark\s+(.+?)\s+(\d+)\s*:\s*([\d,\-\s]+)\s*$", command, flags=re.IGNORECASE)
            if not m:
                clear_screen()
                show_commands()
                print(YELLOW + "💡 Usage: bookmark <Book Name> <Chapter:Verse(s)>  (e.g., bookmark 2 Peter 1:1 or bookmark John 1:1-3,5)" + RESET)
                continue

            user_book = m.group(1).strip()   # e.g. "2 Peter" or "John"
            chapter = m.group(2).strip()     # e.g. "1"
            verse_part = m.group(3).strip()  # e.g. "1-3,5"

            # Normalize whitespace inside verse_part and split by comma
            tokens = [t.strip() for t in verse_part.split(",") if t.strip()]
            if not tokens:
                clear_screen()
                show_commands()
                print(RED + "❗ Invalid chapter:verse format. Use e.g., 3:16" +RESET)
                continue

            # Find matching book(s)
            matches = _find_book_matches(bible_tree, user_book)
            if not matches:
                clear_screen()
                show_commands()
                print(RED + f"❌ No book found matching '{user_book}'. Try '2 Peter' or '2Pet' etc." + RESET)
                continue

            book_key = _choose_book_interactive(matches)
            if not book_key:
                # user cancelled selection
                clear_screen()
                show_commands()
                continue

            # Expand tokens into a list of verse numbers (strings)
            verses_to_bookmark = []
            for token in tokens:
                if "-" in token:
                    # range
                    try:
                        s_str, e_str = [x.strip() for x in token.split("-", 1)]
                        s_i = int(s_str); e_i = int(e_str)
                    except ValueError:
                        print(f"  Skipping invalid range '{token}'.")
                        continue
                    if s_i > e_i:
                        print(f"  Skipping invalid range '{token}' (start > end).")
                        continue
                    for v in range(s_i, e_i + 1):
                        verses_to_bookmark.append(str(v))
                else:
                    # single verse
                    try:
                        v_i = int(token)
                        verses_to_bookmark.append(str(v_i))
                    except ValueError:
                        print(f"  Skipping invalid verse '{token}'.")
                        continue

            if not verses_to_bookmark:
                clear_screen()
                show_commands()
                print( RED+ " No valid verses parsed from your input." +RESET)
                continue

            # Fetch verses from bible_tree and add bookmarks
            added = []
            missing = []
            for vnum in verses_to_bookmark:
                verse_text = bible_tree.get(book_key, {}).get(chapter, {}).get(vnum)
                if verse_text:
                    ref = f"{book_key} {chapter}:{vnum}"
                    add_bookmark(ref, verse_text)
                    added.append(ref)
                else:
                    missing.append(f"{book_key} {chapter}:{vnum}")

            # Feedback to user
            clear_screen()
            if added:
                print(" Added bookmarks:")
                for r in added:
                    print("  -", r)
            if missing:
                print(RED + "\n The following verses were not found (not bookmarked):" + RESET)
                for r in missing:
                    print("  -", r)
            show_commands()
            continue










        # -----------------------------
        # VERSE OF THE DAY
        # -----------------------------
        elif command.lower() == "verseofday":
            clear_results()
            clear_screen()
            show_commands()
            verse_of_the_day(bible_tree)
            

        # -----------------------------
        # UNKNOWN COMMAND HANDLER
        # -----------------------------
        else:
            print(RED + " Unknown command. The available options are displayed above." + RESET)


# -------------------------------------------------
#  PROGRAM ENTRY POINT
# -------------------------------------------------
if __name__ == "__main__":
    try:
        welcome()
        main()
    except KeyboardInterrupt:
        print("\n Program terminated. Have a blessed day!")
