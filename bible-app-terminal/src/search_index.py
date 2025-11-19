"""
search_index.py
---------------
Query helper for inverted index created by indexer.py.

Provides:
 - load_index() -> index dict
 - query_index(query_str, index, bible_tree) -> list of result dicts with verse text
 - paginate_results(results, page, page_size)

Query features:
 - phrase queries using double quotes:  search "love of God"
 - multi-term default -> AND (all terms must be present)
 - tokens normalized via indexer.tokenize (consistency)
"""

from __future__ import annotations
import os
import json
import re
from typing import Dict, List, Tuple
from indexer import tokenize, OUTPUT_DIR

INDEX_FILE = os.path.join(os.path.dirname(__file__), "../outputs/index.json")
_TOKEN_RE = re.compile(r"\w+", flags=re.UNICODE)


def load_index() -> Dict[str, List[dict]]:
    """Load the persisted index; return {} if missing/corrupt."""
    if not os.path.exists(INDEX_FILE):
        return {}
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _posting_key(p: dict) -> str:
    return f"{p['book']}|{p['chapter']}|{p['verse']}"


def _merge_postings_list(postings: List[dict]) -> Dict[str, dict]:
    """Convert postings list -> dict keyed by posting key for O(1) lookup."""
    out = {}
    for p in postings:
        out[_posting_key(p)] = p
    return out


def _intersect_terms(index: Dict[str, List[dict]], terms: List[str]) -> List[dict]:
    """Return postings (list) that contain ALL terms (AND semantics)."""
    if not terms:
        return []
    # Sort by posting list length (smallest first) to minimize work
    term_lists = [(t, index.get(t, [])) for t in terms]
    term_lists.sort(key=lambda x: len(x[1]) if x[1] else 0)
    if not term_lists or not term_lists[0][1]:
        return []
    base = _merge_postings_list(term_lists[0][1])
    for t, plist in term_lists[1:]:
        if not plist:
            return []
        cur = _merge_postings_list(plist)
        keys = set(base.keys()) & set(cur.keys())
        base = {k: base[k] for k in keys}
    return list(base.values())


def _phrase_search(index: Dict[str, List[dict]], phrase: str) -> List[dict]:
    """
    Phrase search using positional lists:
    - tokenize phrase
    - get postings for each token
    - find verses common to all tokens and confirm positional adjacency
    """
    toks = tokenize(phrase)
    if not toks:
        return []
    term_maps = {t: _merge_postings_list(index.get(t, [])) for t in toks}
    # compute intersection of keys
    keys = None
    for m in term_maps.values():
        ks = set(m.keys())
        if keys is None:
            keys = ks
        else:
            keys &= ks
    if not keys:
        return []
    results = []
    for k in keys:
        pos_lists = [term_maps[t][k]["positions"] for t in toks]
        pos_sets = [set(pl) for pl in pos_lists]
        found = False
        for p in pos_lists[0]:
            ok = True
            for i in range(1, len(pos_lists)):
                if (p + i) not in pos_sets[i]:
                    ok = False
                    break
            if ok:
                found = True
                break
        if found:
            results.append(term_maps[toks[0]][k])
    return results


def _tokenize_query(query: str) -> Tuple[List[str], List[str]]:
    """Extract quoted phrases and plain terms."""
    if not query:
        return [], []
    phrases = re.findall(r'"([^"]+)"', query)
    stripped = re.sub(r'"[^"]+"', " ", query)
    terms = [t.lower() for t in _TOKEN_RE.findall(stripped)]
    return phrases, terms


def query_index(query_str: str, index: Dict[str, List[dict]], bible_tree: dict) -> List[dict]:
    """
    Run query against index. Returns list of results as dicts with keys:
      {ref, book, chapter, verse, text}
    """
    if not query_str or not query_str.strip():
        return []

    query_str = query_str.strip()
    phrases, terms = _tokenize_query(query_str)

    # phrase results: require all phrases (AND)
    phrase_keys = None
    for ph in phrases:
        ph_matches = _phrase_search(index, ph)
        keys = set(_posting_key(m) for m in ph_matches)
        phrase_keys = keys if phrase_keys is None else (phrase_keys & keys)

    # term results (AND across terms)
    term_keys = None
    if terms:
        term_postings = _intersect_terms(index, [t.lower() for t in terms])
        term_keys = set(_posting_key(p) for p in term_postings)

    # combine filters
    if phrase_keys is not None and term_keys is not None:
        final_keys = phrase_keys & term_keys
    elif phrase_keys is not None:
        final_keys = phrase_keys
    elif term_keys is not None:
        final_keys = term_keys
    else:
        return []

    results = []
    for key in final_keys:
        book, chapter, verse = key.split("|")
        text = bible_tree.get(book, {}).get(chapter, {}).get(verse, "")
        results.append({
            "ref": f"{book} {chapter}:{verse}",
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "text": text
        })

    # Simple stable ordering: by book, chapter, verse
    results.sort(key=lambda r: (r["book"], int(r["chapter"]), int(r["verse"])))
    return results


def paginate_results(results: List[dict], page: int = 1, page_size: int = 20) -> Tuple[List[dict], int]:
    """Return (page_results, total_pages). page is 1-based."""
    if not results:
        return [], 0
    total = len(results)
    total_pages = (total - 1) // page_size + 1
    page = max(1, min(page, total_pages))
    start = (page - 1) * page_size
    end = min(start + page_size, total)
    return results[start:end], total_pages
