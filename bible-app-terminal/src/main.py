"""
Terminal-Based Bible App
Data Strasdas and adsjdsdjaas Project
Group 5

-----------------------------------------------
This is the main entry point of the application.
It handles the command-line interface and connects
all program modules (search, bookmark, verse of the day, etc.).
"""


from search import boyer_moore_search, search_verse
import os


# -----------------------------------------------
# Load Bible data (Tree Structure)
# -----------------------------------------------
# Adjust the path if necessary based on setup
DATA_PATH = os.path.join(os.pathdirname(__file__), "../data/bible.txt")
# print(" Loading from:", os.path.abspath(DATA_PATH))

def main():
    print("Welcome")
    print("Type help to see commandf")
    
    """
    Main application loop.
    Continuously accepts user input and executes commands.
    """
    # while loop
    while True:
        command = input("> ").strip().lower()

        # -----------------------------
        # SEARCH COMMAND
        # BOOKMARK COMMAND
        # OTHER COMMANDS  (UI)
        # -----------------------------






