"""
search_index.py (lightweight, compatible with your indexer)

Expects outputs/index.json with shape:
  { "inverted_index": { "word": ["Book 1:1", ...], ... } }

Provides:
 - load_index()
 - query_index(query_str, index, bible_tree) -> list of {ref, book, chapter, verse, text}
 - paginate_results(results, page, page_size)
"""

import os
import json
import re
from typing import Dict, List, Tuple

INDEX_FILE = os.path.join(os.path.dirname(__file__), "../outputs/index.json")
_TOKEN_RE = re.compile(r"\w+", flags=re.UNICODE)


def load_index() -> Dict[str, List[str]]:
    """Load the persisted index (simple term->list-of-refs)."""
    if not os.path.exists(INDEX_FILE):
        return {}
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            payload = json.load(f)
            # accept either direct dict or {"inverted_index": {...}}
            if isinstance(payload, dict) and "inverted_index" in payload:
                return payload["inverted_index"]
            # if payload itself is the dict
            return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def _split_ref(ref: str) -> Tuple[str, str, str]:
    """Split 'Book Chapter:Verse' -> (book, chapter, verse)."""
    # assume last token contains chapter:verse
    parts = ref.rsplit(" ", 1)
    if len(parts) != 2:
        return ref, "0", "0"
    book = parts[0]
    chap_verse = parts[1]
    if ":" in chap_verse:
        ch, v = chap_verse.split(":", 1)
    else:
        ch, v = chap_verse, "0"
    return book, ch, v


def _normalize_term(t: str) -> str:
    return t.lower()


def _intersect_lists(lists: List[List[str]]) -> List[str]:
    """Intersect multiple sorted/unsorted lists of refs (simple set intersection)."""
    if not lists:
        return []
    sets = [set(lst) for lst in lists if lst]
    if not sets:
        return []
    common = set.intersection(*sets)
    return list(common)


def _is_phrase_in_text(phrase: str, text: str) -> bool:
    if not phrase or not text:
        return False
    return phrase.lower() in text.lower()


def _tokenize_query(query: str) -> Tuple[List[str], List[str]]:
    """Extract quoted phrases and plain terms."""
    if not query:
        return [], []
    phrases = re.findall(r'"([^"]+)"', query)
    stripped = re.sub(r'"[^"]+"', " ", query)
    terms = [t.lower() for t in _TOKEN_RE.findall(stripped)]
    return phrases, terms


def query_index(query_str: str, index: Dict[str, List[str]], bible_tree: dict) -> List[dict]:
    """
    Query the simple index.
    - terms are ANDed
    - phrases (quoted) are verified by checking verse text
    """
    if not query_str or not query_str.strip():
        return []
    phrases, terms = _tokenize_query(query_str)

    # collect posting lists for terms
    term_lists = []
    for t in terms:
        term_lists.append(index.get(t, []))

    # intersect term posting lists
    if term_lists:
        candidate_refs = _intersect_lists(term_lists)
    else:
        # if no plain terms, start from union of phrase matches later
        candidate_refs = None

    # if phrases exist, filter candidates by phrase presence in the verse text
    if phrases:
        # for each phrase, gather refs that contain the phrase by scanning bible_tree
        phrase_ref_sets = []
        for ph in phrases:
            ph_matches = []
            # scan only candidate_refs if available, otherwise scan all verses
            if candidate_refs is not None:
                refs_to_check = candidate_refs
            else:
                # collect all refs from index (fast to iterate keys)
                # but we need verse text; instead scan bible_tree once (safe)
                refs_to_check = None

            if refs_to_check is not None:
                # check those refs
                for ref in refs_to_check:
                    book, ch, v = _split_ref(ref)
                    text = bible_tree.get(book, {}).get(ch, {}).get(v, "")
                    if _is_phrase_in_text(ph, text):
                        ph_matches.append(ref)
            else:
                # full scan: for small phrase queries only done once
                for book, chapters in bible_tree.items():
                    for ch, verses in chapters.items():
                        for v, txt in verses.items():
                            ref = f"{book} {ch}:{v}"
                            if _is_phrase_in_text(ph, txt):
                                ph_matches.append(ref)
            phrase_ref_sets.append(set(ph_matches))
        # combine phrase sets (AND semantics across phrases)
        if phrase_ref_sets:
            phrase_common = set.intersection(*phrase_ref_sets)
        else:
            phrase_common = set()
        # combine with candidate_refs
        if candidate_refs is not None:
            candidate_refs = list(set(candidate_refs) & phrase_common)
        else:
            candidate_refs = list(phrase_common)

    # if still None (no terms and no phrases) -> empty
    if candidate_refs is None:
        return []

    # Build results with verse text
    results = []
    for ref in candidate_refs:
        book, ch, v = _split_ref(ref)
        text = bible_tree.get(book, {}).get(ch, {}).get(v, "")
        results.append({"ref": ref, "book": book, "chapter": ch, "verse": v, "text": text})

    # sort results for stable presentation
    results.sort(key=lambda r: (r["book"], int(r["chapter"]) if r["chapter"].isdigit() else 0, int(r["verse"]) if r["verse"].isdigit() else 0))
    return results


def paginate_results(results: List[dict], page: int = 1, page_size: int = 20) -> Tuple[List[dict], int]:
    if not results:
        return [], 0
    total = len(results)
    total_pages = (total - 1) // page_size + 1
    page = max(1, min(page, total_pages))
    start = (page - 1) * page_size
    end = min(start + page_size, total)
    return results[start:end], total_pages
