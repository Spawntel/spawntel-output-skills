#!/usr/bin/env python3
"""Build a Spawntel document: embed Inter, check for dashes, print to PDF, render a contact sheet.

Usage: python3 build.py <input.html> <output.pdf> [--sheet sheet.png] [--open]
"""
import argparse
import base64
import glob
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "assets", "Inter.woff2")
BANNED = {"—": "em dash", "–": "en dash"}


def find_browser():
    shells = sorted(glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell")))
    if shells:
        return shells[-1], False
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "brave-browser", "brave"):
        path = shutil.which(name)
        if path:
            return path, True
    sys.exit("No headless browser found. Install Playwright's chromium (npx playwright install chromium-headless-shell) or Chromium.")


def check_dashes(html):
    problems = []
    for n, line in enumerate(html.splitlines(), 1):
        for ch, label in BANNED.items():
            if ch in line:
                problems.append(f"  line {n}: {label}: {line.strip()[:90]}")
    if problems:
        sys.exit("Found dashes. Replace them with a period, comma, colon or 'to':\n" + "\n".join(problems))


def embed_font(html):
    if "/*FONT*/" not in html:
        print("note: no /*FONT*/ placeholder, Inter not embedded")
        return html
    data = base64.b64encode(open(FONT, "rb").read()).decode()
    face = ('@font-face{font-family:"Inter";src:url(data:font/woff2;base64,' + data +
            ') format("woff2");font-weight:100 900;font-display:swap}')
    return html.replace("/*FONT*/", face, 1)


def print_pdf(html_path, pdf_path):
    browser, needs_headless_flag = find_browser()
    cmd = [browser, "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}"]
    if needs_headless_flag:
        cmd.insert(1, "--headless=new")
    cmd.append("file://" + os.path.abspath(html_path))
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180, check=False)
    if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) == 0:
        sys.exit("PDF was not created. Run the browser command by hand to see the error:\n  " + " ".join(cmd))


def report_pages(pdf_path, sheet_path):
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            print("note: pymupdf not installed, skipping page check and contact sheet (pip install pymupdf pillow)")
            return
    doc = pymupdf.open(pdf_path)
    print(f"pages: {len(doc)}")
    for i, page in enumerate(doc, 1):
        text = page.get_text().strip()
        first = text.splitlines()[0][:60] if text else "(empty)"
        flag = "  <- nearly empty, check for an orphan" if len(text) < 200 else ""
        print(f"  {i:>2}: {first}{flag}")
    if not sheet_path:
        return
    try:
        from PIL import Image
    except ImportError:
        print("note: pillow not installed, skipping contact sheet")
        return
    with tempfile.TemporaryDirectory() as tmp:
        images = []
        for i, page in enumerate(doc):
            p = os.path.join(tmp, f"{i:03d}.png")
            page.get_pixmap(dpi=45).save(p)
            images.append(Image.open(p).convert("RGB"))
        w, h = images[0].size
        cols = min(5, len(images))
        rows = (len(images) + cols - 1) // cols
        gap = 8
        sheet = Image.new("RGB", (cols * w + (cols + 1) * gap, rows * h + (rows + 1) * gap), (120, 120, 120))
        for k, im in enumerate(images):
            sheet.paste(im, (gap + (k % cols) * (w + gap), gap + (k // cols) * (h + gap)))
        sheet.save(sheet_path)
    print(f"contact sheet: {sheet_path}  (look at it before calling the document done)")


def open_file(path):
    opener = "open" if sys.platform == "darwin" else ("start" if os.name == "nt" else "xdg-open")
    subprocess.Popen([opener, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=(os.name == "nt"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("pdf")
    ap.add_argument("--sheet")
    ap.add_argument("--open", action="store_true")
    a = ap.parse_args()

    html = open(a.html, encoding="utf-8").read()
    check_dashes(html)
    built = embed_font(html)
    out_dir = os.path.dirname(os.path.abspath(a.pdf))
    os.makedirs(out_dir, exist_ok=True)
    src_dir = os.path.dirname(os.path.abspath(a.html))  # keep relative image paths working
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=src_dir, delete=False, encoding="utf-8") as f:
        f.write(built)
        tmp_html = f.name
    try:
        print_pdf(tmp_html, a.pdf)
    finally:
        os.remove(tmp_html)
    print(f"pdf: {a.pdf}")
    report_pages(a.pdf, a.sheet)
    if a.open:
        open_file(a.pdf)


if __name__ == "__main__":
    main()
