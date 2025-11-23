"""
history.py
-----------------------------------------------
Timestamped search history persisted in ../outputs/history.txt (JSON).
Each record is a tuple/list: [ timestamp_str, query_str ].
"""

import json
import os
from collections import deque
from datetime import datetime
from ui import *

# file paths
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../outputs")
HISTORY_FILE = os.path.join(OUTPUT_DIR, "history.txt")

# in-memory deque
MAX_HISTORY = 200
history = deque(maxlen=MAX_HISTORY)  # store tuples (timestamp, query)

# -------------------------
# Helpers: load/save
# -------------------------
def _ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

def _load_history():
    global history
    _ensure_output_dir()
    if not os.path.exists(HISTORY_FILE):
        history = deque(maxlen=MAX_HISTORY)
        return
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Expect a list of [timestamp, query]
            if isinstance(data, list):
                history = deque(data[-MAX_HISTORY:], maxlen=MAX_HISTORY)
            else:
                history = deque(maxlen=MAX_HISTORY)
    except Exception:
        history = deque(maxlen=MAX_HISTORY)

def _save_history():
    _ensure_output_dir()
    try:
        # convert deque -> list for JSON
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(list(history), f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(RED + f"Could not save history: {e}" + RESET)

# Load on import
_load_history()

# -------------------------
# Public API
# -------------------------
def add_history(query):
    """
    Add a timestamped query to history and persist immediately.
    Skips navigation commands 'next' and 'prev'.
    """
    if not query:
        return
    q_norm = str(query).strip()
    if q_norm.lower() in ("next", "prev"):
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append((timestamp, q_norm))
    _save_history()

def show_history(limit=None):
    """
    Print recent search history. If limit provided, show up to limit items.
    Most recent items shown last (chronological).
    """
    if not history:
        print(" No recent searches.")
        return

    items = list(history)
    if limit is None or limit > len(items):
        limit = len(items)

    # Show newest last (older first)
    for timestamp, query in items[-limit:]:
        print(f"{BLUE}[{timestamp}]{RESET} {query}")

def clear_history():
    """
    Clear history both in-memory and on-disk.
    """
    global history
    history = deque(maxlen=MAX_HISTORY)
    _save_history()
    print("  History cleared.")
