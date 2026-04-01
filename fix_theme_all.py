#!/usr/bin/env python3
"""
Fix dark/light theme across all HTML pages.
Replaces hardcoded Tailwind color classes with CSS-variable-based utility classes.
"""

import re
import os

BASE = r"d:\Craft Cider & Meadery Company"

FILES = [
    "about.html",
    "contact.html",
    "gallery.html",
    "booking.html",
    "services.html",
    "servicedetails.html",
    "login.html",
    "signup.html",
    "userdash.html",
    "dashboard.html",
    "index.html",
    "home2.html",
]

# CSS-class replacements: (old_class, new_class)
# We do exact word-boundary replacements (space-separated class tokens)
REPLACEMENTS = [
    # Section backgrounds
    ("bg-white",        "bg-background"),
    ("bg-[#FFFFFF]",    "bg-background"),

    # Light gray tint bg  
    ("bg-[#F1F5F2]",    "bg-hover"),
    ("bg-[#F9FAF9]",    "bg-hover"),
    ("bg-[#F9FAF8]",    "bg-hover"),

    # Text colors
    ("text-gray-600",   "text-secondary-text"),
    ("text-gray-500",   "text-secondary-text"),
    ("text-gray-400",   "text-secondary-text"),
    ("text-[#1F3D2B]",  "text-accent"),
    ("text-[#2D5A3F]",  "text-accent"),

    # Border colors
    ("border-gray-200", "border-border"),
    ("border-gray-100", "border-border"),

    # Input/form backgrounds in light context  
    ("bg-[#F9FAF9] rounded-2xl border border-transparent hover:border-[#E6B325]/30 hover:bg-white",
     "bg-hover rounded-2xl border border-transparent hover:border-accent-light/30 hover:bg-background"),
]

# Also add dark-mode-aware CSS block additions to each file's <style>
EXTRA_CSS = """
        /* Dark mode overrides for hardcoded content sections */
        html[data-theme='dark'] .section-bg-white {
            background-color: var(--color-background) !important;
        }
        html[data-theme='dark'] section,
        html[data-theme='dark'] .card-bg {
            color: var(--color-primary-text);
        }
        /* Form inputs in dark mode */
        html[data-theme='dark'] input,
        html[data-theme='dark'] select,
        html[data-theme='dark'] textarea {
            background-color: var(--color-hover);
            color: var(--color-primary-text);
            border-color: var(--color-border);
        }
        html[data-theme='dark'] input::placeholder,
        html[data-theme='dark'] textarea::placeholder {
            color: var(--color-secondary-text);
        }
        /* Cards / white background blocks */
        html[data-theme='dark'] .bg-white {
            background-color: var(--color-background) !important;
        }
        html[data-theme='dark'] .bg-\\[\\#F1F5F2\\],
        html[data-theme='dark'] .bg-\\[\\#F9FAF9\\],
        html[data-theme='dark'] .bg-\\[\\#F9FAF8\\] {
            background-color: var(--color-hover) !important;
        }
        html[data-theme='dark'] .text-gray-600,
        html[data-theme='dark'] .text-gray-500,
        html[data-theme='dark'] .text-gray-400 {
            color: var(--color-secondary-text) !important;
        }
        html[data-theme='dark'] .text-\\[\\#1F3D2B\\],
        html[data-theme='dark'] .text-\\[\\#2D5A3F\\] {
            color: var(--color-primary-text) !important;
        }
        html[data-theme='dark'] .border-gray-100,
        html[data-theme='dark'] .border-gray-200 {
            border-color: var(--color-border) !important;
        }
        html[data-theme='dark'] .bg-\\[\\#F9FAF9\\] .bg-white,
        html[data-theme='dark'] details.bg-white,
        html[data-theme='dark'] .rounded-2xl.bg-white,
        html[data-theme='dark'] .rounded-xl.bg-white,
        html[data-theme='dark'] .rounded-3xl.bg-white {
            background-color: var(--color-hover) !important;
        }
        /* FAQ/accordion dark mode */
        html[data-theme='dark'] details {
            background-color: var(--color-hover) !important;
            border-color: var(--color-border) !important;
        }
        html[data-theme='dark'] details summary {
            color: var(--color-primary-text) !important;
        }
        /* Form containers */
        html[data-theme='dark'] form input,
        html[data-theme='dark'] form select,
        html[data-theme='dark'] form textarea {
            background-color: var(--color-hover) !important;
            color: var(--color-primary-text) !important;
            border-color: var(--color-border) !important;
        }
        /* Contact info cards */
        html[data-theme='dark'] .group.p-8 {
            background-color: var(--color-hover) !important;
        }
        /* Package cards */
        html[data-theme='dark'] .border.border-gray-100 {
            background-color: var(--color-hover) !important;
            border-color: var(--color-border) !important;
        }
        /* Filter buttons */
        html[data-theme='dark'] button.text-gray-400 {
            color: var(--color-secondary-text) !important;
        }
        html[data-theme='dark'] .py-12.bg-white {
            background-color: var(--color-background) !important;
        }
        html[data-theme='dark'] .py-20.bg-white,
        html[data-theme='dark'] .py-24.bg-white {
            background-color: var(--color-background) !important;
        }
"""

MARKER = "/* DARK MODE EXTRA - AUTO GENERATED */"

def inject_css(content, extra_css):
    """Inject extra CSS before closing </style> in the <head>."""
    if MARKER in content:
        # Already injected, skip
        return content
    # Find the closing </style> in head
    insert_before = "    </style>"
    idx = content.find(insert_before)
    if idx == -1:
        return content
    marked = f"\n        {MARKER}{extra_css}\n"
    return content[:idx] + marked + content[idx:]


def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Inject extra dark mode CSS
    content = inject_css(content, EXTRA_CSS)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [FIXED] {os.path.basename(filepath)}")
    else:
        print(f"  [SKIP]  {os.path.basename(filepath)} (already up to date)")


if __name__ == "__main__":
    print(f"Processing {len(FILES)} files in: {BASE}\n")
    for fname in FILES:
        fpath = os.path.join(BASE, fname)
        if os.path.exists(fpath):
            fix_file(fpath)
        else:
            print(f"  [MISS]  {fname} not found")
    print("\nDone.")
