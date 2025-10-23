"""
history.py
-----------------------------------------------
Handles the search history using a Queue (deque),
each record now includes a timestamp.
"""

from collections import deque
from datetime import datetime

# Each item will be a tuple: (timestamp, query)
history = deque(maxlen=50)  # Increased capacity


# Now, each search query gets saved like: ("2025-10-22 21:45:30", "love")


def add_history(query):
    """
    Adds a search query to history with current timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append((timestamp, query))


def show_history(limit=None):
    """
    Displays recent search history.
    If 'limit' is specified, only shows that number of recent searches.
    """
    if not history:
        print("No recent searches.")
        return

    print("\n Search History:")
    if limit is None or limit > len(history):
        limit = len(history)

    # Show newest last, oldest first
    for timestamp, query in list(history)[-limit:]:
        print(f"[{timestamp}] {query}")
