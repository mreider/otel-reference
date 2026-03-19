#!/usr/bin/env python3
"""
Build KDP-ready files from the OpenTelemetry Primer.

Outputs:
  kdp/output/otel-primer.epub          Kindle ebook
  kdp/output/otel-primer-print.pdf     KDP paperback interior (6x9)

Setup:
  brew install pango                   # macOS system dependency for weasyprint
  pip install -r kdp/requirements.txt

Usage:
  python kdp/build.py                  # both formats
  python kdp/build.py --epub-only
  python kdp/build.py --pdf-only

Note: KDP also requires a cover image, uploaded separately.
  Ebook cover: 2560 x 1600 px minimum
  Print cover: use KDP Cover Calculator at kdp.amazon.com
"""

import argparse
import os
import platform
import sys
from collections import OrderedDict
from pathlib import Path

# macOS: ensure Homebrew libraries (pango, gobject) are discoverable
if platform.system() == "Darwin":
    brew_lib = "/opt/homebrew/lib"
    if os.path.isdir(brew_lib):
        os.environ.setdefault("DYLD_LIBRARY_PATH", brew_lib)

ROOT = Path(__file__).resolve().parent.parent
KDP = Path(__file__).resolve().parent
OUTPUT = KDP / "output"

TITLE = "OpenTelemetry Primer"
AUTHOR = "Matthew Reider"
YEAR = 2026
LANGUAGE = "en"
ABOUT_AUTHOR = (
    "Matthew Reider has spent more than twenty years in software, much of it "
    "at the intersection of open source communities and infrastructure. He "
    "found his footing in the Ruby on Rails community at Engine Yard, helped "
    "grow Cloud Foundry into one of the first enterprise platform-as-a-service "
    "projects, and now works at Dynatrace alongside the Kubernetes and "
    "OpenTelemetry communities. He lives in Vienna, Austria with his wife, "
    "kids, cats, and dog."
)
DESCRIPTION = (
    "OpenTelemetry Primer builds understanding one concept at a time "
    "\u2013 each entry introduces a single idea, grounded in what came "
    "before. Written for anyone whose work touches observability, whether "
    "you build the systems, manage the teams, or are evaluating tools.\n\n"
    "Covers:\n"
    "\u2022 Signals \u2013 what metrics, traces, and logs each reveal\n"
    "\u2022 Pipeline \u2013 how telemetry is collected, processed, and routed\n"
    "\u2022 Correlation \u2013 how the three signals connect to reach root cause"
)


def parse_html():
    from bs4 import BeautifulSoup
    html = (ROOT / "index.html").read_text()
    return BeautifulSoup(html, "html.parser")


def get_phases_and_entries(soup):
    """Walk the body and group entries under their phase headings."""
    phases = OrderedDict()
    current_phase = None
    for el in soup.body.children:
        if not hasattr(el, "get"):
            continue
        classes = el.get("class", [])
        if "phase" in classes:
            current_phase = el.get_text(strip=True)
            phases[current_phase] = []
        elif "entry" in classes and current_phase is not None:
            phases[current_phase].append(el)
    return phases


# ---------- EPUB ----------

def build_epub(soup):
    from ebooklib import epub

    book = epub.EpubBook()
    book.set_identifier("otel-primer-v1")
    book.set_title(TITLE)
    book.set_language(LANGUAGE)
    book.add_author(AUTHOR)
    book.add_metadata("DC", "description", DESCRIPTION)

    css = epub.EpubItem(
        uid="style",
        file_name="style/main.css",
        media_type="text/css",
        content=_epub_css().encode("utf-8"),
    )
    book.add_item(css)

    # Cover image (shows in library/thumbnail)
    cover_path = OUTPUT / "cover-ebook.png"
    if cover_path.exists():
        book.set_cover("images/cover.png", cover_path.read_bytes(), create_page=False)

    # Logo image (used on interior title page)
    logo_data = (ROOT / "otel-logo.png").read_bytes()
    logo_item = epub.EpubItem(
        uid="logo",
        file_name="images/otel-logo.png",
        media_type="image/png",
        content=logo_data,
    )
    book.add_item(logo_item)

    # Title page
    title_ch = epub.EpubHtml(title="Title Page", file_name="title.xhtml", lang=LANGUAGE)
    title_ch.content = f"""<div class="title-page">
  <h1>{TITLE}</h1>
  <p class="subtitle">Each concept building on the last</p>
  <img class="title-logo" src="images/otel-logo.png" alt="">
  <p class="author">{AUTHOR}</p>
</div>"""
    title_ch.add_item(css)
    book.add_item(title_ch)

    # Copyright page
    copy_ch = epub.EpubHtml(title="Copyright", file_name="copyright.xhtml", lang=LANGUAGE)
    copy_ch.content = f"""<div class="copyright-page">
  <p>{TITLE}</p>
  <p>&copy; {YEAR} {AUTHOR}. All rights reserved.</p>
  <p style="margin-top:1.5em;">OpenTelemetry is a CNCF incubating project. CNCF and the CNCF logo design are registered trademarks of the Cloud Native Computing Foundation. This book is not affiliated with or sponsored by the Cloud Native Computing Foundation.</p>
</div>"""
    copy_ch.add_item(css)
    book.add_item(copy_ch)

    # One chapter per phase
    phases = get_phases_and_entries(soup)
    chapters = []

    for i, (phase_name, entries) in enumerate(phases.items()):
        ch = epub.EpubHtml(
            title=phase_name,
            file_name=f"ch{i + 1:02d}.xhtml",
            lang=LANGUAGE,
        )
        html = f'<h2 class="phase">{phase_name}</h2>\n'
        for entry in entries:
            html += str(entry) + "\n"
        ch.content = html
        ch.add_item(css)
        book.add_item(ch)
        chapters.append(ch)

    # About the Author (back matter)
    about_ch = epub.EpubHtml(title="About the Author", file_name="about.xhtml", lang=LANGUAGE)
    about_ch.content = f"""<div class="about-page">
  <h2 class="about-heading">About the Author</h2>
  <p>{ABOUT_AUTHOR}</p>
</div>"""
    about_ch.add_item(css)
    book.add_item(about_ch)

    book.toc = chapters + [about_ch]
    book.spine = [title_ch, copy_ch, "nav"] + chapters + [about_ch]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    OUTPUT.mkdir(parents=True, exist_ok=True)
    out = OUTPUT / "otel-primer.epub"
    epub.write_epub(str(out), book)
    print(f"  EPUB  \u2192 {out}")


def _epub_css():
    return """
body {
  font-family: Georgia, 'Times New Roman', serif;
  color: #1a1a1a;
  line-height: 1.5;
  margin: 1em;
}

.title-page {
  text-align: center;
  padding-top: 35%;
}
.title-page h1 {
  font-size: 2em;
  font-weight: normal;
  margin: 0 0 0.3em;
}
.title-page .subtitle {
  font-style: italic;
  color: #666;
  margin: 0 0 1.5em;
}
.title-logo {
  display: block;
  margin: 0 auto 2em;
  width: 50%;
  max-width: 200px;
  height: auto;
}
.title-page .author {
  font-size: 1.1em;
}

.copyright-page {
  padding-top: 50%;
  font-size: 0.85em;
  color: #666;
}
.copyright-page p { margin: 0.3em 0; }

h2.phase {
  font-variant: small-caps;
  letter-spacing: 0.12em;
  font-size: 1.2em;
  color: #555;
  text-align: center;
  margin: 2em 0 1em;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.4em;
}

.entry { margin-bottom: 1.4em; page-break-inside: auto; }
.entry-head { font-weight: bold; font-size: 1.05em; margin-bottom: 0.2em; page-break-after: avoid; }
.entry-num { color: #999; font-weight: normal; font-size: 0.8em; margin-right: 0.3em; }
.entry p { margin: 0.4em 0 0; }

.term { font-weight: bold; }
.it { font-style: italic; }

.ex {
  font-family: monospace;
  font-size: 0.8em;
  line-height: 1.5;
  background: #f5f5f0;
  border-left: 2px solid #ddd;
  padding: 0.6em 0.8em;
  margin: 0.5em 0;
  white-space: pre;
  overflow-x: auto;
}

.defs { margin: 0.8em 0; }
.defs dt { font-weight: bold; margin-top: 0.5em; }
.defs dd { margin: 0.1em 0 0.4em 1.2em; }

.note { font-style: italic; color: #666; font-size: 0.92em; }
.ill, svg { display: block; margin: 1.2em auto; max-width: 100%; height: auto; }

.about-page { padding-top: 15%; }
.about-heading {
  font-variant: small-caps;
  letter-spacing: 0.12em;
  font-size: 1.2em;
  color: #555;
  text-align: center;
  margin: 0 0 1.5em;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.4em;
}
"""


# ---------- PDF ----------

def build_pdf(soup):
    import weasyprint

    # Remove web-only elements
    for el in soup.find_all("nav", class_="toc"):
        el.decompose()
    for el in soup.find_all("svg", class_="squid"):
        el.decompose()
    for el in soup.find_all("div", class_="downloads"):
        el.decompose()
    for el in soup.find_all("img", class_="logo"):
        el.decompose()
    for el in soup.find_all("footer"):
        el.decompose()
    for el in soup.find_all("p", class_="subtitle"):
        el.decompose()
    h1 = soup.find("h1")
    if h1:
        h1.decompose()

    # Build TOC from entry headings
    toc_html = ""
    for entry in soup.find_all("div", class_="entry"):
        head = entry.find("div", class_="entry-head")
        if head:
            toc_html += f'<div class="toc-entry">{head.get_text()}</div>\n'

    # Filter out Comment nodes (the em-dash dividers leak as visible text)
    from bs4 import Comment
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()

    # Strip inline width/height from SVGs so CSS controls sizing,
    # and darken strokes/fills for print legibility
    _print_colors = {
        "#e5e5e5": "#888", "#eee": "#aaa", "#ddd": "#777",
        "#d5d5d5": "#777", "#ccc": "#555", "#bbb": "#444",
        "#aaa": "#333", "#999": "#333",
    }
    for svg in soup.find_all("svg"):
        if svg.get("viewBox"):
            del svg["width"]
            del svg["height"]
        for el in svg.find_all(True):
            for attr in ("stroke", "fill"):
                val = (el.get(attr) or "").lower()
                if val in _print_colors:
                    el[attr] = _print_colors[val]
            # Thicken strokes
            sw = el.get("stroke-width")
            if sw:
                try:
                    el["stroke-width"] = str(float(sw) * 2)
                except ValueError:
                    pass

    body = "".join(str(c) for c in soup.body.children) if soup.body else str(soup)
    print_css = (KDP / "print.css").read_text()

    full_html = f"""<!DOCTYPE html>
<html lang="{LANGUAGE}">
<head>
  <meta charset="UTF-8">
  <style>{print_css}</style>
</head>
<body>
  <div class="title-page"><div class="tp-inner">
    <h1 class="book-title">{TITLE}</h1>
    <p class="book-subtitle">Each concept building on the last</p>
    <img class="title-logo" src="otel-logo.png" alt="">
    <p class="book-author">{AUTHOR}</p>
  </div></div>

  <div class="copyright-page">
    <p>{TITLE}</p>
    <p>&copy; {YEAR} {AUTHOR}. All rights reserved.</p>
    <p class="cp-note">OpenTelemetry is a CNCF incubating project. CNCF and the CNCF logo design are registered trademarks of the Cloud Native Computing Foundation. This book is not affiliated with or sponsored by the Cloud Native Computing Foundation.</p>
  </div>

  <div class="toc-page">
    <div class="toc-heading">Contents</div>
    {toc_html}
  </div>

  {body}

  <div class="about-page">
    <div class="about-heading">About the Author</div>
    <p>{ABOUT_AUTHOR}</p>
  </div>
</body>
</html>"""

    OUTPUT.mkdir(parents=True, exist_ok=True)
    out = OUTPUT / "otel-primer-print.pdf"
    doc = weasyprint.HTML(string=full_html, base_url=str(ROOT))
    doc.write_pdf(str(out))
    print(f"  PDF   \u2192 {out}")


# ---------- Main ----------

def main():
    parser = argparse.ArgumentParser(description="Build KDP-ready files")
    parser.add_argument("--epub-only", action="store_true")
    parser.add_argument("--pdf-only", action="store_true")
    args = parser.parse_args()

    both = not args.epub_only and not args.pdf_only

    print("Building KDP formats...\n")

    if both or args.epub_only:
        build_epub(parse_html())

    if both or args.pdf_only:
        build_pdf(parse_html())

    print("\nDone. Output in kdp/output/")
    print(f"\nReminder: KDP requires a cover image (uploaded separately).")
    print(f"  Ebook: 2560 x 1600 px minimum")
    print(f"  Print: use KDP Cover Calculator at kdp.amazon.com")


if __name__ == "__main__":
    main()
