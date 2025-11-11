import os
"""
ui.py
-----------------------------------------------
Contains the command help and user interface display functions.
Helps guide users through available commands.
"""

# -------------------------------------------------
#  COMMAND-LINE HELP MENU
# -------------------------------------------------
def show_commands():
    """Displays all available user commands."""
    print("""
================================== COMMANDS MENU ====================================
  search <keyword/book/ref>         → Search for verses or references
  next / prev                       → Navigate search results
  bookmark <Book> <Chapter:Verse>   → Save a verse to your bookmarks
  bookmarks                         → View saved bookmarks
  history [n]                       → View search history (optionally limit results)
  verseofday                        → Display a random verse
  home                              → Return to home menu
  exit                              → Quit the program
=====================================================================================
""")

# -------------------------------------------------
#  CLS FUNCTION FOR TERMINAL
# -------------------------------------------------    
def clear_screen():
    os.system('cls')
