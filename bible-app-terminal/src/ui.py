import os
"""
ui.py
-----------------------------------------------
Contains the command help and user interface display functions.
Helps guide users through available commands.
"""
# -------------------------------------------------
#  ANSI COLOR CODES
# -------------------------------------------------
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
# -------------------------------------------------
#  COMMAND-LINE HELP MENU
# -------------------------------------------------
def show_commands():
    """Displays all available user commands with color coding."""
    print(f"""{Colors.BOLD}{Colors.CYAN}
================================== COMMANDS MENU ====================================
{Colors.END}{Colors.GREEN}  search <keyword/book/ref>       {Colors.END}→ Search for verses or references
{Colors.GREEN}  next / prev                     {Colors.END}→ Navigate search results
{Colors.GREEN}  bookmark <Book> <Chapter:Verse> {Colors.END}→ Save a verse to your bookmarks
{Colors.GREEN}  bookmarks                       {Colors.END}→ View saved bookmarks
{Colors.GREEN}  history [n]                     {Colors.END}→ View search history (optionally limit results)
{Colors.GREEN}  verseofday                      {Colors.END}→ Display a random verse
{Colors.GREEN}  home                            {Colors.END}→ Return to home menu
{Colors.GREEN}  exit                            {Colors.END}→ Quit the program
{Colors.CYAN}====================================================================================={Colors.END}
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

