from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Sequence, Tuple


def normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def clamp_text(s: str, max_len: int) -> str:
    s = normalize_space(s)
    if len(s) <= max_len:
        return s
    cut = s[: max_len - 1].rstrip()
    return cut


def word_count_from_html(html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = re.sub(r"\{\{\s*link:[^}]+\}\}", " ", text)
    text = normalize_space(text)
    if not text:
        return 0
    return len([w for w in text.split(" ") if w])


def p(text: str) -> str:
    return f"<p>{text}</p>"


def h2(text: str) -> str:
    return f"<h2>{text}</h2>"


def h3(text: str) -> str:
    return f"<h3>{text}</h3>"


def ul(items: Sequence[str]) -> str:
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f"<ul>{lis}</ul>"


def cta_box(title: str, body: str, link_placeholder: str, cta_text: str, strong: bool = False) -> str:
    cls = "seo-cta seo-cta--strong" if strong else "seo-cta seo-cta--soft"
    return (
        f'<div class="{cls}">'
        f"<h3>{title}</h3>"
        f"<p>{body}</p>"
        f"<div class=\"seo-cta__action\">{{{{ link:{link_placeholder} }}}}</div>"
        f"<p class=\"seo-cta__hint\">{cta_text}</p>"
        f"</div>"
    )


@dataclass(frozen=True)
class MetaPack:
    title: str
    meta_title: str
    meta_description: str


def make_meta(title: str, meta_title: str, meta_description: str, meta_title_max: int = 60, meta_desc_min: int = 150, meta_desc_max: int = 160) -> MetaPack:
    mt = clamp_text(meta_title, meta_title_max)
    md = normalize_space(meta_description)
    if len(md) < meta_desc_min:
        # pad lightly without stuffing
        md = (md + " " + "Detaylar için sayfayı inceleyin.").strip()
    md = clamp_text(md, meta_desc_max)
    return MetaPack(title=normalize_space(title), meta_title=mt, meta_description=md)


def faq(question_answer_pairs: Iterable[Tuple[str, str]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for q, a in question_answer_pairs:
        qn = normalize_space(q)
        an = normalize_space(a)
        if not qn or not an:
            continue
        rows.append({"question": qn, "answer": an})
    return rows

