---
name: spawntel-documentation
description: Make a clean, simple, fully sourced PDF document the Spawntel way (study guide, blueprint, explainer, handbook, SOP, report meant to be read and kept). Use whenever Jay or the team asks for a PDF, a guide, documentation, a blueprint, a handbook, "something I can study", or a written explanation of how something works. Covers reader-first structure, plain writing, source discipline, the visual system, the HTML-to-PDF build script and page-by-page QA.
---

# Spawntel Documentation

Origin, 2026-10-31: Jay approved the Philippine business registration study guide with "its so clean no unnecessary stuff. just clear and simple." He asked to keep the method, not to copy that guide's exact design or cover. Every new document gets its own cover and sections; the system below stays.

## The method, in order

1. **Know the reader and the job.** Who reads it, and what must they understand or decide afterwards? If the reader is new to the subject, explain the world first: a map of who does what, then the order things happen in, then the details.
2. **Research before writing whenever facts matter.**
   - Primary sources first: the law itself (lawphil.net for Philippine laws), the agency's own page, official PDFs. Then named firms. Blogs last, and labelled as such.
   - Open every source you cite and note the exact line that supports each fact. Never cite a URL you did not open or see in search results.
   - If a fact can't be confirmed from an official source, don't state it. Put it in the "Ask first" part with who to ask.
   - If a source contradicts something said earlier in the conversation, add a yellow correction box in the document and say it plainly in chat.
3. **Outline in numbered parts.** Each part has a pill (`Part 3`), a heading that states the point in plain words, an optional one-line lead, then bullets, cards, a table or a flowchart.
4. **Write plain.** Short sentences. Answer first. Explain each term the first time it appears. One analogy at the start if the reader is new to the subject. Real examples with real math when a number matters. A paragraph longer than about four lines becomes bullets.
5. **Build from `assets/template.html`.** Copy it next to the output, replace the placeholder content, delete every component the content doesn't need.
6. **Run the build:** `python3 scripts/build.py <doc.html> <doc.pdf> --sheet <sheet.png> --open`
7. **Look at the contact sheet before calling it done.** Fix a heading stranded at the bottom of a page, a flowchart split across pages, a lone line on the last page, anything overflowing. Use the `keep` class on a short part to hold it together. Rebuild and look again.
8. **Deliver.** Save the PDF and its HTML source in the account folder the work belongs to, never only as an artifact. The build opens it for Jay. The chat reply stays short: what it covers, any corrections, the path.

## Structure kit

Use only what the content needs.

- **Cover:** pill, a plain one-line title, one sentence under it, one box stating the promise (for example how sources work). No logo unless asked. Never a Spawntel logo on GVA or personal training work.
- **Bullets with a bold lead-in:** `<b>What you get:</b> ...`
- **Card:** a soft-filled block for grouped content.
- **Key fact box (violet):** the single most important rule in a part. At most one per part.
- **Correction box (yellow):** when the document corrects something said earlier or a common wrong belief.
- **Table:** only for real comparisons (A vs B, fee tiers). Dark header, zebra rows.
- **Flowchart:** connected numbered steps with arrows, for any order or process. Keep a flow on one page.
- **Ask first:** what isn't confirmed, and who to ask.
- **Glossary:** every term a newcomer would have to look up.
- **Sources page:** numbered list, each labelled Law, Official, Tax firm, Guide or Commentary, with the date it was checked. Cite inline with a small violet `[n]` right after the fact.

## Never

- Micro-descriptions: dim sub-lines under labels, eyebrow text, taglines, "in one line" summary cards, dim footers.
- Emojis, decorative icons, visible outlines or borders, a second typeface (monospace included).
- Em dashes or en dashes anywhere. The build fails if it finds one.
- Flowering: metaphors for the reader's situation, "X isn't A, it's B" lines, clever titles.
- Briefing notes, internal reasoning, or how-it-was-made notes inside the document.
- Invented numbers, prices, offers or sources.

## Visual system

- A4, white paper, Inter only (the build embeds `assets/Inter.woff2`, so the PDF looks the same on every machine).
- Sizes: cover title 44pt, part heading 24pt, body 11pt. Hierarchy comes from size and weight, never grey tiers.
- Colours: headings `#121214`, body `#2A2A2E`, soft fills `#F3F2F7` and `#E9E6F3`, violet `#6700FF` used sparingly (pills, citation numbers, arrows, one key box), yellow `#FFF4D6` only for corrections.
- Generous white space. Each major part starts on a new page when it would otherwise start near the bottom.

## Build script

`scripts/build.py <input.html> <output.pdf> [--sheet sheet.png] [--open]`

- The input HTML holds `/*FONT*/` inside its `<style>`; the script swaps in the embedded Inter font.
- Fails on any em or en dash and prints the line numbers.
- Prints the page count and flags near-empty pages.
- `--sheet` renders every page into one contact-sheet PNG for the visual check (needs `pymupdf` and `pillow`).
- `--open` opens the PDF in the default viewer.
- Browser: Playwright's `chrome-headless-shell` if present, otherwise Chromium, Google Chrome or Brave.

## Reference

First document built this way: the Philippine business registration study guide (13 pages, 19 sources, laws quoted from lawphil.net), at `SPAWNTEL (MY STARTUP)/Registration/philippine-business-registration-guide.pdf` in Jay's workspace.
