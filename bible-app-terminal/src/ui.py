"""
ui.py
-----------------------------------------------
Contains the command help and user interface display functions.
Helps guide users through available commands.
"""

def show_help():
    """
    Prints a list of available commands and their descriptions.
    """

    print("""
Available Commands:
  search <keyword>       - Search for a verse containing the keyword
  bookmark <Book> <Ref>  - Bookmark a specific verse (e.g., bookmark John 3:16)
  bookmarks              - View all bookmarked verses
  verse_of_the_day       - Display a random verse
  history                - Show recent searches
  help                   - Show this help menu
  exit                   - Exit the application
    """)

def navigation():
    """
    Shows the available command once user seach a verse.
    """

    print("""
Available Commands for  navigation :
  next       - go to next verse
  preview    - go to prevoius verse
  
    """)