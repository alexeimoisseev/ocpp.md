#!/usr/bin/env python3
"""
Site generator for ocpp.md

Converts OCPP-related markdown files to HTML pages matching the hand-crafted
index.html style. Outputs to public/ directory.

Usage:
    python scripts/generate_site.py

Dependencies:
    pip install markdown
"""

import html
import os
import re
import shutil
from pathlib import Path

import markdown

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "public"

# Markdown files to convert: (source_path, clean_url_path)
# Each page outputs to public/<url_path>/index.html
INDEX_SOURCE = "docs/index.md"

CONTENT_FILES = [
    ("docs/OCPP-2.0.1.md", "ocpp-2.0.1"),
    ("docs/OCPP-2.0.1-DataTypes.md", "ocpp-2.0.1/data-types"),
    ("docs/METHODOLOGY.md", "methodology"),
    ("docs/AI-AGENT-SETUP.md", "ai-agent-setup"),
    ("docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Authorization.md", "ocpp-2.0.1/schemas/authorization"),
    ("docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Availability.md", "ocpp-2.0.1/schemas/availability"),
    ("docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Diagnostics.md", "ocpp-2.0.1/schemas/diagnostics"),
    ("docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Display.md", "ocpp-2.0.1/schemas/display"),
    ("docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Firmware.md", "ocpp-2.0.1/schemas/firmware"),
    ("docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md", "ocpp-2.0.1/schemas/provisioning"),
    ("docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Reservation.md", "ocpp-2.0.1/schemas/reservation"),
    ("docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Security.md", "ocpp-2.0.1/schemas/security"),
    ("docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md", "ocpp-2.0.1/schemas/smart-charging"),
    ("docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Transactions.md", "ocpp-2.0.1/schemas/transactions"),
    ("docs/OCPP-2.0.1-Sequences/OCPP-2.0.1-Sequences.md", "ocpp-2.0.1/sequences"),
    ("docs/OCPP-2.0.1-Sequences/OCPP-2.0.1-Sequences-Operational.md", "ocpp-2.0.1/sequences/operational"),
    ("docs/OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md", "ocpp-2.0.1/smart-charging"),
    ("docs/OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging-Examples.md", "ocpp-2.0.1/smart-charging/examples"),
    ("docs/OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging-ISO15118.md", "ocpp-2.0.1/smart-charging/iso15118"),
    # OCPP 1.6J
    ("docs/OCPP-1.6J.md", "ocpp-1.6j"),
    ("docs/OCPP-1.6J-Schemas/OCPP-1.6J-Schemas-Core.md", "ocpp-1.6j/schemas/core"),
    ("docs/OCPP-1.6J-Schemas/OCPP-1.6J-Schemas-SmartCharging.md", "ocpp-1.6j/schemas/smart-charging"),
    ("docs/OCPP-1.6J-Schemas/OCPP-1.6J-Schemas-Firmware.md", "ocpp-1.6j/schemas/firmware"),
    ("docs/OCPP-1.6J-Schemas/OCPP-1.6J-Schemas-LocalAuthList.md", "ocpp-1.6j/schemas/local-auth-list"),
    ("docs/OCPP-1.6J-Schemas/OCPP-1.6J-Schemas-Reservation.md", "ocpp-1.6j/schemas/reservation"),
    ("docs/OCPP-1.6J-Schemas/OCPP-1.6J-Schemas-RemoteTrigger.md", "ocpp-1.6j/schemas/remote-trigger"),
    ("docs/OCPP-1.6J-Sequences/OCPP-1.6J-Sequences.md", "ocpp-1.6j/sequences"),
    ("docs/OCPP-1.6J-SmartCharging/OCPP-1.6J-SmartCharging.md", "ocpp-1.6j/smart-charging"),
]

# Mapping: normalized .md source path -> clean URL path (for link rewriting)
MD_TO_URL = {os.path.normpath(src): url for src, url in CONTENT_FILES}

STATIC_FILES = [
    "favicon.ico",
    "favicon.svg",
    "favicon-180.png",
    "_headers",
]

# Index page TOC — short labels for the landing page sticky nav
INDEX_TOC = [
    ("why-this-exists", "Why"),
    ("using-with-ai-agents", "Setup"),
    ("ocpp-201", "2.0.1"),
    ("ocpp-16j", "1.6J"),
    ("the-escalation-model", "Escalation"),
    ("about-this-project", "About"),
]

# Section ID overrides for the index page (markdown h2 text -> desired id)
INDEX_HEADING_IDS = {
    "Why This Exists": "why-this-exists",
    "OCPP 2.0.1": "ocpp-201",
    "OCPP 1.6J": "ocpp-16j",
    "The Escalation Model": "the-escalation-model",
    "Using with AI Agents": "using-with-ai-agents",
    "About This Project": "about-this-project",
}

# Subsection ID overrides for the index page
INDEX_SUBHEADING_IDS = {
    "Claude Code": "claude-code",
    "Other Agents (Cursor, Windsurf, Copilot, etc.)": "other-agents",
}


# ---------------------------------------------------------------------------
# CSS — extracted from the hand-crafted index.html
# ---------------------------------------------------------------------------

SITE_CSS = """\
  :root {
    --bg: #faf9f7;
    --bg-code: #f0efeb;
    --bg-table-head: #e8e6e1;
    --bg-table-stripe: #f5f4f1;
    --text: #1a1a18;
    --text-muted: #6b6962;
    --text-light: #8a857c;
    --accent: #2d6a4f;
    --accent-light: #d8f3dc;
    --border: #d4d1c9;
    --border-light: #e8e6e1;
    --link: #2d6a4f;
    --link-hover: #1b4332;
    --serif: 'Source Serif 4', Georgia, 'Times New Roman', serif;
    --mono: 'IBM Plex Mono', 'Menlo', 'Consolas', monospace;
    --max-width: 800px;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  html { scroll-behavior: smooth; }

  body {
    font-family: var(--serif);
    font-size: 17px;
    line-height: 1.72;
    color: var(--text);
    background: var(--bg);
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }

  /* --- Header / Hero --- */
  .site-header {
    border-bottom: 1px solid var(--border);
    padding: 3rem 2rem 2.5rem;
    background: linear-gradient(180deg, #f5f4f0 0%, var(--bg) 100%);
  }

  .site-header .inner {
    max-width: var(--max-width);
    margin: 0 auto;
  }

  .site-header .domain {
    font-family: var(--mono);
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--accent);
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
  }

  .site-header .domain a {
    color: var(--accent);
    text-decoration: none;
  }

  .site-header .domain a:hover {
    text-decoration: underline;
  }

  .site-header h1 {
    font-family: var(--serif);
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1.2;
    color: var(--text);
    margin-bottom: 0.6rem;
    letter-spacing: -0.01em;
  }

  .site-header .subtitle {
    font-size: 1.05rem;
    color: var(--text-muted);
    line-height: 1.6;
    max-width: 600px;
    font-weight: 300;
  }

  .site-header .meta {
    margin-top: 1.5rem;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--text-light);
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem 1.5rem;
  }

  .site-header .meta span::before {
    content: '';
    display: inline-block;
    width: 6px;
    height: 6px;
    background: var(--accent);
    border-radius: 50%;
    margin-right: 0.5rem;
    vertical-align: middle;
    position: relative;
    top: -1px;
  }

  /* --- Navigation / TOC Bar --- */
  .toc-bar {
    border-bottom: 1px solid var(--border-light);
    padding: 1rem 2rem;
    position: sticky;
    top: 0;
    background: rgba(250, 249, 247, 0.92);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    z-index: 100;
  }

  .toc-bar .inner {
    max-width: var(--max-width);
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    overflow-x: auto;
    scrollbar-width: none;
  }

  .toc-bar .inner::-webkit-scrollbar { display: none; }

  .toc-bar a {
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--text-muted);
    text-decoration: none;
    white-space: nowrap;
    padding: 0.3rem 0.55rem;
    border-radius: 4px;
    transition: all 0.15s;
    letter-spacing: 0.01em;
  }

  .toc-bar a:hover {
    color: var(--accent);
    background: var(--accent-light);
  }

  .toc-bar a.active {
    color: var(--accent);
    background: var(--accent-light);
  }

  .toc-sep {
    color: var(--border);
    font-size: 0.7rem;
    user-select: none;
  }

  /* --- Main Content --- */
  main {
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 2.5rem 2rem 6rem;
  }

  /* --- Headings --- */
  h2, h3, h4 {
    position: relative;
  }

  h2 {
    font-family: var(--serif);
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 1rem;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid var(--accent);
    letter-spacing: -0.01em;
    line-height: 1.3;
  }

  h3 {
    font-family: var(--serif);
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--text);
    margin-top: 2rem;
    margin-bottom: 0.6rem;
    line-height: 1.35;
  }

  h4 {
    font-family: var(--mono);
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--accent);
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    letter-spacing: 0.02em;
  }

  /* --- Heading anchor links --- */
  .heading-anchor {
    position: absolute;
    left: -1.4em;
    top: 0;
    font-family: var(--mono);
    font-weight: 400;
    color: var(--border);
    text-decoration: none;
    opacity: 0;
    transition: opacity 0.15s, color 0.15s;
    font-size: 0.85em;
    line-height: inherit;
    padding-right: 0.3em;
  }

  h3 .heading-anchor { font-size: 0.8em; }
  h4 .heading-anchor { font-size: 0.9em; left: -1.5em; }

  h2:hover .heading-anchor,
  h3:hover .heading-anchor,
  h4:hover .heading-anchor,
  .heading-anchor:focus {
    opacity: 1;
  }

  .heading-anchor:hover {
    color: var(--accent);
    opacity: 1;
  }

  /* Flash highlight when navigating to an anchor */
  :target {
    scroll-margin-top: 80px;
  }

  h2:target, h3:target, h4:target {
    animation: anchor-flash 1.5s ease;
  }

  @keyframes anchor-flash {
    0% { background: var(--accent-light); }
    100% { background: transparent; }
  }

  /* --- Paragraphs --- */
  p {
    margin-bottom: 1rem;
  }

  strong {
    font-weight: 600;
  }

  /* --- Links --- */
  a {
    color: var(--link);
    text-decoration-color: rgba(45, 106, 79, 0.3);
    text-underline-offset: 2px;
    transition: color 0.15s, text-decoration-color 0.15s;
  }

  a:hover {
    color: var(--link-hover);
    text-decoration-color: var(--link-hover);
  }

  /* --- Blockquote --- */
  blockquote {
    border-left: 3px solid var(--accent);
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
    background: var(--accent-light);
    border-radius: 0 6px 6px 0;
    font-size: 0.95rem;
    color: var(--text-muted);
  }

  blockquote p { margin-bottom: 0.4rem; }
  blockquote p:last-child { margin-bottom: 0; }

  /* --- Code --- */
  code {
    font-family: var(--mono);
    font-size: 0.85em;
    background: var(--bg-code);
    padding: 0.15em 0.4em;
    border-radius: 3px;
    color: var(--text);
  }

  pre {
    background: #1e1e1c;
    color: #e0ddd5;
    padding: 1.25rem 1.5rem;
    border-radius: 8px;
    overflow-x: auto;
    margin-bottom: 1.25rem;
    line-height: 1.55;
    font-size: 0.82rem;
    border: 1px solid rgba(0,0,0,0.06);
  }

  pre code {
    background: none;
    padding: 0;
    border-radius: 0;
    color: inherit;
    font-size: inherit;
  }

  /* Syntax highlighting — minimal */
  .tok-str { color: #a9dc76; }
  .tok-num { color: #fc9867; }
  .tok-key { color: #78dce8; }
  .tok-comment { color: #727067; font-style: italic; }
  .tok-bracket { color: #939089; }

  /* --- Tables --- */
  .table-wrap {
    overflow-x: auto;
    margin-bottom: 1.25rem;
    border-radius: 6px;
    border: 1px solid var(--border-light);
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
    line-height: 1.5;
  }

  thead {
    background: var(--bg-table-head);
  }

  th {
    font-family: var(--mono);
    font-size: 0.76rem;
    font-weight: 600;
    text-align: left;
    padding: 0.65rem 1rem;
    color: var(--text-muted);
    letter-spacing: 0.03em;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
  }

  td {
    padding: 0.55rem 1rem;
    border-bottom: 1px solid var(--border-light);
    vertical-align: top;
  }

  tbody tr:nth-child(even) {
    background: var(--bg-table-stripe);
  }

  tbody tr:last-child td {
    border-bottom: none;
  }

  td code {
    font-size: 0.82em;
    white-space: nowrap;
  }

  /* --- Lists --- */
  ul, ol {
    padding-left: 1.5rem;
    margin-bottom: 1rem;
  }

  li {
    margin-bottom: 0.3rem;
  }

  li > ul, li > ol {
    margin-top: 0.3rem;
    margin-bottom: 0.3rem;
  }

  /* --- Horizontal Rule --- */
  hr {
    border: none;
    height: 1px;
    background: var(--border);
    margin: 3rem 0;
  }

  /* --- ASCII diagram --- */
  .diagram {
    background: var(--bg-code);
    border: 1px solid var(--border-light);
    padding: 1.25rem 1.5rem;
    border-radius: 8px;
    overflow-x: auto;
    margin-bottom: 1.25rem;
    font-family: var(--mono);
    font-size: 0.82rem;
    line-height: 1.55;
    color: var(--text);
  }

  /* --- Copied tooltip --- */
  .copied-toast {
    position: fixed;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%) translateY(20px);
    font-family: var(--mono);
    font-size: 0.75rem;
    background: var(--text);
    color: var(--bg);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s, transform 0.2s;
    z-index: 1000;
  }

  .copied-toast.visible {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }

  /* --- Responsive --- */
  @media (max-width: 640px) {
    body { font-size: 16px; }
    .site-header { padding: 2rem 1.25rem 1.75rem; }
    .site-header h1 { font-size: 1.7rem; }
    .toc-bar { padding: 0.75rem 1.25rem; }
    main { padding: 2rem 1.25rem 4rem; }
    pre { padding: 1rem; font-size: 0.78rem; }
    th, td { padding: 0.5rem 0.7rem; }
    h2 { font-size: 1.35rem; }
    .heading-anchor { display: none; }
  }

  /* --- Print --- */
  @media print {
    .toc-bar { display: none; }
    .heading-anchor { display: none; }
    body { font-size: 11pt; }
    pre { white-space: pre-wrap; }
  }"""

# ---------------------------------------------------------------------------
# JavaScript — extracted from the hand-crafted index.html
# ---------------------------------------------------------------------------

SITE_JS = """\
(function() {
  // --- Scroll spy for top nav ---
  var topNavLinks = document.querySelectorAll('.toc-bar a[data-section]');
  var headings = [];

  document.querySelectorAll('h2[id], h3[id], h4[id]').forEach(function(h) {
    headings.push(h);
  });

  var topSectionIds = [];
  topNavLinks.forEach(function(a) {
    topSectionIds.push(a.getAttribute('data-section'));
  });

  function updateScrollSpy() {
    var scrollY = window.scrollY + 100;
    var active = null;
    for (var i = 0; i < headings.length; i++) {
      if (headings[i].offsetTop <= scrollY) {
        active = headings[i];
      }
    }
    if (!active) return;

    // Find the nearest h2 section for the top nav
    var activeSection = null;
    if (active.tagName === 'H2' && topSectionIds.indexOf(active.id) !== -1) {
      activeSection = active.id;
    } else {
      for (var i = headings.indexOf(active); i >= 0; i--) {
        if (headings[i].tagName === 'H2' && topSectionIds.indexOf(headings[i].id) !== -1) {
          activeSection = headings[i].id;
          break;
        }
      }
    }

    topNavLinks.forEach(function(a) {
      if (a.getAttribute('data-section') === activeSection) {
        a.classList.add('active');
      } else {
        a.classList.remove('active');
      }
    });
  }

  var scrollTimeout;
  window.addEventListener('scroll', function() {
    if (scrollTimeout) cancelAnimationFrame(scrollTimeout);
    scrollTimeout = requestAnimationFrame(updateScrollSpy);
  }, { passive: true });

  updateScrollSpy();

  // --- Copy anchor link on click ---
  var toast = document.getElementById('copied-toast');
  var toastTimer;

  document.querySelectorAll('.heading-anchor').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      var id = this.getAttribute('href');
      var url = window.location.origin + window.location.pathname + id;

      history.replaceState(null, '', id);

      if (navigator.clipboard) {
        navigator.clipboard.writeText(url);
      }

      toast.classList.add('visible');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(function() {
        toast.classList.remove('visible');
      }, 1800);
    });
  });
})();"""


# ---------------------------------------------------------------------------
# Output path helpers
# ---------------------------------------------------------------------------

def url_to_output_path(url_path: str) -> str:
    """Convert a clean URL path to its output file path."""
    return os.path.join(url_path, "index.html")


# ---------------------------------------------------------------------------
# JSON syntax highlighter (matches hand-crafted .tok-* classes)
# ---------------------------------------------------------------------------

def highlight_json(code_text: str) -> str:
    """Apply .tok-* span highlighting to JSON code."""
    result = []
    i = 0
    text = code_text
    length = len(text)

    while i < length:
        ch = text[i]

        # String literal
        if ch == '"' or ch == '&' and text[i:i+6] == '&quot;':
            # Find the actual quote character
            if ch == '&':
                quote_str = '&quot;'
                quote_len = 6
            else:
                quote_str = '"'
                quote_len = 1

            # Scan ahead to find the closing quote
            j = i + quote_len
            while j < length:
                if text[j] == '\\':
                    j += 2  # skip escaped char
                    continue
                if text[j:j+quote_len] == quote_str:
                    j += quote_len
                    break
                if text[j] == '&':
                    # HTML entity — check for &quot;
                    if text[j:j+6] == '&quot;':
                        j += 6
                        break
                j += 1
            else:
                j = length

            token = text[i:j]

            # Check if this is a key (followed by optional whitespace then colon)
            rest = text[j:j+10].lstrip()
            if rest.startswith(':'):
                result.append(f'<span class="tok-key">{token}</span>')
            else:
                result.append(f'<span class="tok-str">{token}</span>')
            i = j
            continue

        # Number (after colon/comma/bracket or at start)
        if ch in '0123456789' or (ch == '-' and i + 1 < length and text[i+1] in '0123456789'):
            j = i + 1
            while j < length and text[j] in '0123456789.eE+-':
                j += 1
            result.append(f'<span class="tok-num">{text[i:j]}</span>')
            i = j
            continue

        # Booleans and null
        for keyword in ['true', 'false', 'null']:
            if text[i:i+len(keyword)] == keyword:
                result.append(f'<span class="tok-num">{keyword}</span>')
                i += len(keyword)
                break
        else:
            # Brackets and braces
            if ch in '{}[]':
                result.append(f'<span class="tok-bracket">{ch}</span>')
                i += 1
            else:
                result.append(ch)
                i += 1

    return ''.join(result)


# ---------------------------------------------------------------------------
# Markdown conversion
# ---------------------------------------------------------------------------

def preprocess_markdown(text: str) -> str:
    """Fix markdown quirks before conversion.

    1. Python-Markdown requires a blank line before a list that follows a
       paragraph. GFM does not. Insert blank lines where needed.
    2. Consecutive blockquote lines (> line1 / > line2) render as a single
       paragraph. Append <br> so each line renders separately.
    """
    LIST_START = re.compile(r'^(?:[-*+]|\d+\.) ')
    LIST_ITEM = re.compile(r'^(?:[-*+]|\d+\.) |^\s+(?:[-*+]|\d+\.) ')
    BQ_LINE = re.compile(r'^> .+')

    lines = text.split('\n')
    result = []
    for i, line in enumerate(lines):
        # Insert blank line before list items that follow a non-list paragraph
        if i > 0 and LIST_START.match(line):
            prev = lines[i - 1]
            if prev.strip() and not LIST_ITEM.match(prev):
                result.append('')
        # Append <br> to blockquote lines followed by another blockquote line
        if BQ_LINE.match(line) and i + 1 < len(lines) and BQ_LINE.match(lines[i + 1]):
            result.append(line + '  ')
        else:
            result.append(line)
    return '\n'.join(result)


def convert_markdown(text: str) -> str:
    """Convert markdown text to HTML body using Python-Markdown."""
    text = preprocess_markdown(text)
    md = markdown.Markdown(
        extensions=[
            'tables',
            'fenced_code',
            'toc',
            'md_in_html',
        ],
        extension_configs={
            'toc': {
                'permalink': False,
                'slugify': _slugify,
            },
        },
    )
    return md.convert(text)


def _slugify(value, separator):
    """Generate URL-friendly slug from heading text."""
    # Remove HTML tags
    value = re.sub(r'<[^>]+>', '', value)
    # Decode HTML entities
    value = html.unescape(value)
    # Convert to lowercase
    value = value.lower()
    # Replace special chars with separator
    value = re.sub(r'[^\w\s-]', '', value)
    value = re.sub(r'[\s]+', separator, value.strip())
    value = re.sub(r'[-]+', separator, value)
    return value


# ---------------------------------------------------------------------------
# Post-processing
# ---------------------------------------------------------------------------

def wrap_tables(body: str) -> str:
    """Wrap <table> elements in <div class="table-wrap">."""
    return re.sub(
        r'(<table.*?</table>)',
        r'<div class="table-wrap">\1</div>',
        body,
        flags=re.DOTALL,
    )


def add_heading_anchors(body: str) -> str:
    """Add .heading-anchor links inside h2/h3/h4 tags that have ids."""
    def _add_anchor(m):
        tag = m.group(1)   # h2, h3, h4
        attrs = m.group(2)  # everything between <hN and >
        content = m.group(3)
        # Extract id
        id_match = re.search(r'id="([^"]+)"', attrs)
        if not id_match:
            return m.group(0)
        heading_id = id_match.group(1)
        anchor = f'<a class="heading-anchor" href="#{heading_id}" aria-label="Link to this section">#</a>'
        return f'<{tag}{attrs}>{anchor}{content}</{tag}>'

    return re.sub(
        r'<(h[234])([^>]*)>(.*?)</\1>',
        _add_anchor,
        body,
    )


def rewrite_md_links(body: str, source_rel: str, source_url: str) -> str:
    """Rewrite .md links to clean URL paths using MD_TO_URL mapping."""
    source_dir = str(Path(source_rel).parent)

    def _rewrite(m):
        prefix = m.group(1)  # href=" or src="
        url = m.group(2)
        suffix = m.group(3)  # closing quote

        # Only rewrite relative .md links
        if '://' in url or url.startswith('#') or url.startswith('mailto:'):
            return m.group(0)

        # Split fragment
        if '#' in url:
            path_part, fragment = url.split('#', 1)
            fragment = '#' + fragment
        else:
            path_part = url
            fragment = ''

        if not path_part.endswith('.md'):
            return m.group(0)

        # Resolve the target .md path relative to source file's directory
        if source_dir and source_dir != '.':
            resolved = os.path.normpath(os.path.join(source_dir, path_part))
        else:
            resolved = os.path.normpath(path_part)

        # Look up target's clean URL path
        if resolved not in MD_TO_URL:
            return m.group(0)  # unknown .md file, leave as-is

        target_url = MD_TO_URL[resolved]

        # Compute relative path from source page to target page
        rel = os.path.relpath(target_url, source_url).replace('\\', '/')

        # Build directory-style URL with trailing slash
        if rel == '.':
            new_url = './' + fragment
        else:
            new_url = rel + '/' + fragment

        return f'{prefix}{new_url}{suffix}'

    return re.sub(
        r'(href="|src=")(.*?)(")',
        _rewrite,
        body,
    )


def highlight_json_blocks(body: str) -> str:
    """Find <code class="language-json"> blocks and apply JSON syntax highlighting."""
    def _highlight(m):
        code_content = m.group(1)
        highlighted = highlight_json(code_content)
        return f'<code class="language-json">{highlighted}</code>'

    return re.sub(
        r'<code class="language-json">(.*?)</code>',
        _highlight,
        body,
        flags=re.DOTALL,
    )


def extract_title(body: str) -> tuple:
    """Extract and remove the first <h1> from the body. Returns (title, body_without_h1)."""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', body)
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1))  # strip inner tags
        title = html.unescape(title)  # decode &amp; etc. to avoid double-encoding later
        body = body[:m.start()] + body[m.end():]
        # Also remove any <hr> immediately after the h1 (common in markdown)
        body = re.sub(r'^\s*<hr\s*/?>', '', body, count=1)
        return title, body
    return "OCPP.md", body


def extract_h2_toc(body: str) -> list:
    """Extract (id, text) pairs from h2 headings for TOC bar generation."""
    toc = []
    for m in re.finditer(r'<h2[^>]*id="([^"]+)"[^>]*>(?:<a[^>]*>.*?</a>)?(.*?)</h2>', body):
        heading_id = m.group(1)
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        text = html.unescape(text)  # decode &amp; etc. to avoid double-encoding in TOC
        # Strip leading number prefix like "1. " for cleaner TOC
        short = re.sub(r'^\d+\.\s*', '', text)
        toc.append((heading_id, short))
    return toc


def override_heading_ids(body: str, is_index: bool) -> str:
    """For the index page, override auto-generated heading IDs to match the hand-crafted ones."""
    if not is_index:
        return body

    def _override_h2(m):
        full_tag = m.group(0)
        tag = m.group(1)
        attrs = m.group(2)
        content = m.group(3)
        # Get text content for lookup
        text = re.sub(r'<[^>]+>', '', content).strip()
        lookup = INDEX_HEADING_IDS if tag == 'h2' else INDEX_SUBHEADING_IDS
        if text in lookup:
            new_id = lookup[text]
            attrs = re.sub(r'id="[^"]*"', f'id="{new_id}"', attrs)
            return f'<{tag}{attrs}>{content}</{tag}>'
        return full_tag

    body = re.sub(r'<(h2)([^>]*)>(.*?)</\1>', _override_h2, body)
    body = re.sub(r'<(h3)([^>]*)>(.*?)</\1>', _override_h2, body)
    body = re.sub(r'<(h4)([^>]*)>(.*?)</\1>', _override_h2, body)
    return body


# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------

HEAD_COMMON = """\
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&display=swap" rel="stylesheet">"""


def build_toc_bar_html(toc_items: list) -> str:
    """Generate the sticky TOC bar HTML from (id, label) pairs."""
    parts = []
    for i, (heading_id, label) in enumerate(toc_items):
        if i > 0:
            parts.append(' <span class="toc-sep">&middot;</span>\n')
        parts.append(
            f'    <a href="#{heading_id}" data-section="{heading_id}">{html.escape(label)}</a>'
        )
    inner = '\n'.join(parts)
    return f'<nav class="toc-bar">\n  <div class="inner">\n{inner}\n  </div>\n</nav>'


def build_page(
    title: str,
    body: str,
    toc_items: list,
    source_rel: str,
    url_path: str,
    is_index: bool = False,
    description: str = "",
) -> str:
    """Assemble a complete HTML page."""

    # Raw markdown link: relative path from HTML page's directory to .md file
    raw_md_href = os.path.relpath(source_rel, url_path).replace('\\', '/')

    # Back link to index page
    if is_index:
        path_to_index = ""
    else:
        index_url = MD_TO_URL.get(os.path.normpath(INDEX_SOURCE))
        if index_url:
            rel = os.path.relpath(index_url, url_path).replace('\\', '/')
            path_to_index = rel + '/'
        else:
            # INDEX_SOURCE not in CONTENT_FILES — it's rendered at site root
            depth = url_path.count('/')
            path_to_index = '../' * (depth + 1) if depth >= 0 else '/'

    # Page title for <title> tag
    if is_index:
        page_title = "OCPP.md \u2014 Open Charge Point Protocol Reference"
    else:
        page_title = f"{title} \u2014 OCPP.md"

    if not description:
        if is_index:
            description = "A structured OCPP protocol reference for AI agents and developers working on EV charging infrastructure. Covers OCPP 2.0.1 and 1.6J specifications."
        else:
            description = f"{title} \u2014 OCPP protocol reference for AI agents."

    # Header
    if is_index:
        header_html = f"""\
<header class="site-header">
  <div class="inner">
    <div class="domain">ocpp.md</div>
    <h1>Open Charge Point Protocol Reference</h1>
    <p class="subtitle">Schemas, sequences, smart charging, and escalation markers for AI agents and developers.</p>
    <div class="meta">
      <span><a href="./ocpp-2.0.1/" style="color: var(--text-light); text-decoration: underline; text-decoration-color: rgba(138,133,124,0.4);">OCPP 2.0.1</a></span>
      <span><a href="./ocpp-1.6j/" style="color: var(--text-light); text-decoration: underline; text-decoration-color: rgba(138,133,124,0.4);">OCPP 1.6J</a></span>
    </div>
  </div>
</header>"""
    else:
        header_html = f"""\
<header class="site-header">
  <div class="inner">
    <div class="domain"><a href="{path_to_index}">\u2190 ocpp.md</a></div>
    <h1>{html.escape(title)}</h1>
    <div class="meta">
      <span><a href="{raw_md_href}" style="color: var(--text-light); text-decoration: underline; text-decoration-color: rgba(138,133,124,0.4);">Raw Markdown \u2197</a></span>
    </div>
  </div>
</header>"""

    toc_bar_html = build_toc_bar_html(toc_items)

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
{HEAD_COMMON}
<title>{html.escape(page_title)}</title>
<meta name="description" content="{html.escape(description)}">
<style>
{SITE_CSS}
</style>
</head>
<body>

{header_html}

{toc_bar_html}

<!-- Copied toast -->
<div class="copied-toast" id="copied-toast">Link copied</div>

<main>
{body}
</main>

<script>
{SITE_JS}
</script>

</body>
</html>
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_file(source_rel: str, url_path: str):
    """Process a single markdown file and write the HTML output."""
    source_path = ROOT / source_rel
    is_index = (source_rel == INDEX_SOURCE)
    out_rel = url_to_output_path(url_path)

    print(f"  {source_rel} -> {out_rel}")

    # Read markdown
    md_text = source_path.read_text(encoding='utf-8')

    # Convert to HTML
    body = convert_markdown(md_text)

    # Override heading IDs for index page
    body = override_heading_ids(body, is_index)

    # Post-process
    body = wrap_tables(body)
    body = highlight_json_blocks(body)
    body = rewrite_md_links(body, source_rel, url_path)

    # Extract title (first h1)
    title, body = extract_title(body)

    # Add heading anchors (after title extraction)
    body = add_heading_anchors(body)

    # Generate TOC
    if is_index:
        toc_items = INDEX_TOC
    else:
        toc_items = extract_h2_toc(body)

    # Assemble page
    page_html = build_page(
        title=title,
        body=body,
        toc_items=toc_items,
        source_rel=source_rel,
        url_path=url_path,
        is_index=is_index,
    )

    # Write output
    out_path = OUTPUT_DIR / out_rel
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page_html, encoding='utf-8')


def copy_static_files():
    """Copy static files and raw .md sources to public/."""
    # Static files (favicons, _headers)
    for f in STATIC_FILES:
        src = ROOT / f
        if src.exists():
            dst = OUTPUT_DIR / f
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  [static] {f}")

    # Raw .md copies (keep original names and directory structure)
    for source_rel, _url_path in CONTENT_FILES:
        src = ROOT / source_rel
        dst = OUTPUT_DIR / source_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  [md] {source_rel}")


def generate_root_index():
    """Generate a root index.html with links resolved relative to site root."""
    process_file(INDEX_SOURCE, ".")


def main():
    print(f"Generating site into {OUTPUT_DIR}/\n")

    # Clean output directory
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    # Process markdown files
    print("Converting markdown to HTML:")
    for source_rel, url_path in CONTENT_FILES:
        process_file(source_rel, url_path)

    # Copy index to site root
    print("\nRoot index:")
    generate_root_index()

    # Copy static files
    print("\nCopying static files:")
    copy_static_files()

    total = len(CONTENT_FILES)
    print(f"\nDone! {total} pages generated in {OUTPUT_DIR}/")


if __name__ == '__main__':
    main()
