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
    """Displays all available user commands with color coding."""
    print(f"""{BOLD}{CYAN}
================================== COMMANDS MENU ====================================
{RESET}{GREEN}  search <keyword/book/ref>       {RESET}→ Search for verses or references
{GREEN}  next / prev                     {RESET}→ Navigate search results
{GREEN}  bookmark <Book> <Chapter:Verse> {RESET}→ Save a verse to your bookmarks
{GREEN}  bookmarks                       {RESET}→ View saved bookmarks
{GREEN}  history [n]                     {RESET}→ View search history (optionally limit results)
{GREEN}  verseofday                      {RESET}→ Display a random verse
{GREEN}  home                            {RESET}→ Return to home menu
{GREEN}  exit                            {RESET}→ Quit the program
{CYAN}====================================================================================={RESET}
""")

# -------------------------------------------------
#  CLS FUNCTION FOR TERMINAL
# -------------------------------------------------    
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
# -------------------------------------------------
# COLORS (ANSI Escape Codes)
# -------------------------------------------------   

RESET   = "\033[0m"
BOLD    = "\033[1m"

BLACK   = "\033[30m"
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"

