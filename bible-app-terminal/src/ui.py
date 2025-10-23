"""
ui.py
-----------------------------------------------
Contains the command help and user interface display functions.
Helps guide users through available commands.
"""

# -------------------------------------------------
#  COMMAND-LINE HELP MENU
# -------------------------------------------------
def show_help():
    """Displays all available user commands."""
    print("""
============================== HELP MENU ==============================
  search <keyword/book/ref>         → Search for verses or references
  next / prev                       → Navigate search results
  bookmark <Book> <Chapter:Verse>   → Save a verse to your bookmarks
  bookmarks                         → View saved bookmarks
  history [n]                       → View search history (optionally limit results)
  verseofday                        → Display a random verse
  help                              → Show this help menu
  exit                              → Quit the program
=======================================================================
""")