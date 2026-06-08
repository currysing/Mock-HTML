# CorpID Mobile Pages — Implementation Plan & Skill Notes

## Task Summary

Convert JPEG mock-up images of a Hong Kong government CorpID digital identity portal into static HTML pages sized for iPhone 16 Pro (393×852 CSS pixels).

---

## Approach Used

### 1. Image Analysis (Explore agent)
All 10 mock images were read and described in detail:
- **10 images** → **4 distinct screens** (some images show the same screen at different scroll/tab states)
- Extracted: layout structure, UI elements, all text content (Traditional Chinese), colors, and inter-image relationships

### 2. Plan
Designed a shared design system (colors, typography, layout pattern) and page-by-page specifications before writing any code.

### 3. Implementation (v1)
Four self-contained HTML files, each with:
- Inline CSS (no external stylesheets)
- Inline JS where needed (tab switching, carousel, checkbox toggle)
- `.phone-frame` wrapper enforcing 393×852 bounds
- Status bar, header, scrollable body, optional bottom nav

### 4. Fidelity Refinement (v2)
The v1 pass relied on the Explore agent's text description and used emoji/Unicode placeholders. For v2 the **actual mock JPEGs were read directly** (Read tool on `HomePage1`, `ServiceCat1a`, `Login1`, `ApplyCorpID2`) to capture details the text summary missed. Changes:
- **Bottom nav** — replaced emoji with hand-authored inline SVG icons (house / 2×2 grid / QR / clipboard / building); corrected labels to **首頁 · 服務 · 掃描 · 待辦 · 本企** (v1 wrongly had 主頁 / 企業); active state renders the filled icon, with the 服務 grid showing one light-blue tile
- **Status bar** — real iOS-style inline-SVG signal bars, wifi arc, and a battery pill reading `79` with a 79% gradient fill (was emoji/text)
- **Headers** — SVG back-chevron, three-dot menu, divider, and X close
- **home.html** — blue `iD` logo (was teal "D"), CSS sky-gradient hero + `<svg>` skyline silhouette, "註冊 CORPiD" promo banner, masonry card grid with a tall card and department subtitles, "更多" right-aligned link
- **login.html** — bordered white cards on gray bg, blue section headings, iAM Smart phone-check button icon, boxed-↗ external link icons

### 5. Services Expansion (v4)
Built out the 主題 tab as a real navigable hub. No new mock images for this round — content was authored from the existing industry list and the user's seed of demo company names. Changes:
- **iOS-Contacts-style index** — refactored `buildBizIndex` (biz-only) into a generic `buildIndex(panelId, barId, prefix)` so 政府 and 商業 share the same sort + right-edge index strip. `classify(name)` returns `{ sort, id, label, text }` keyed on the 1st char: CJK → stroke count (via `STROKES` map, sorted first); ASCII letter → uppercase A–Z (sorted after CJK at `1000+charCode`); else `#`. Group headers are inserted into the list as `.org-group-header`, and the right strip (`.index-bar.show`) renders tappable scroll-to-group items. `activateTab()` toggles which bar shows.
- **`STROKES` map** is the single source of truth; extend it whenever an item's 1st char isn't already listed (gov added: 入 土 工 公 食 商 康 稅 路 運 漁 數 醫). Missing chars fall into `#` and break the visual grouping, so always extend before adding items.
- **10 industry topic pages** (`Farming.html` … `Finance.html`) cloned from `InfoComm.html`, with industry-appropriate gov + biz lists. Topic tiles in `INDEX.html` converted from `<div>` to `<a>`.
- **`?from=` back-link pattern** — gov item inside a topic uses `<a href="AFCD.html?from=Farming.html">`. Detail page back chevron is `<a class="header-back" id="backLink" href="INDEX.html#gov">`, plus an IIFE just before `</body>`:

  ```js
  (function () {
    var m = location.search.match(/[?&]from=([^&]+)/);
    if (!m) return;
    var from = decodeURIComponent(m[1]);
    if (!/^[A-Za-z0-9_-]+\.html(#[A-Za-z0-9_-]+)?$/.test(from)) return;
    var back = document.getElementById('backLink');
    if (back) back.setAttribute('href', from);
  })();
  ```

  The regex whitelist prevents `?from=` from being used as an open-redirect / XSS vector. Without the param the chevron keeps its default `INDEX.html#gov` target.
- **Gov chevron removed** — `<span class="org-arrow">…</span>` deleted from all 16 gov items in `INDEX.html` to mirror the biz section. CSS for `.org-arrow` is still defined and used by topic pages.

---

## Skills & Tools Used

| Tool / Skill | Purpose |
|---|---|
| `Agent (Explore)` | v1 — read all 10 mock images and produce a detailed description of each screen |
| `Read` (on JPEGs) | v2 — directly inspect the actual mock images for pixel-level detail (icons, colors, exact labels) |
| `EnterPlanMode` + `ExitPlanMode` | Design and get approval for implementation approach before writing code |
| `Write` / `Edit` | Create and refine the four HTML files and memory/artifact files |
| `Bash` | Create the `Mobile/` and `artifacts/` directories |

### Key Lessons
- The Explore agent's text description was good for structure and copy, but **reading the source images directly was necessary for visual fidelity** — icon shapes, the exact nav labels (本企 vs 企業), the blue (not teal) logo, and the iOS status-bar treatment were only correct after direct inspection.
- For multi-page expansion (10 topic pages), **batch into rounds** — Round 1: parallel `save-file` of stubs from the canonical template; Round 2: parallel `str-replace` to inject per-page content; Round 3: wire up the entry-point page; Round 4: update shared back-handler logic on detail pages. Each round used parallel tool calls; rounds were sequenced because Round N depended on Round N−1's file existing.
- When extending the navigation graph, **map every entry → back-link pair explicitly** before editing. The `?from=` pattern avoids the dead-end-back-button problem for one-to-many fan-in (e.g. AFCD reachable from both INDEX and Farming) without duplicating detail pages or stuffing `history.back()` (which breaks on direct-URL loads).
- **Refactor before duplicating** — when 政府 needed the same index strip as 商業, generalising `buildBizIndex` → `buildIndex(panelId, barId, prefix)` was cheaper than copy-pasting, and it positions a future 3rd panel for free.

---

## File Map

```
project/
├── mock-images/          ← source mock-ups (read-only reference)
│   ├── HomePage1-4.jpeg
│   ├── service_cat_1a/1b/2/3.PNG   ← v3 services redo
│   ├── ApplyCorpID1-2.jpeg
│   ├── Login1.jpeg
│   └── 漁農自然護理署 / 稅務局 / 海關 / 食物環境衞生署 / 運輸署 .PNG  ← individual gov logos
├── Mobile/               ← output HTML pages
│   ├── home.html
│   ├── apply-corpid.html
│   ├── login.html
│   └── Services/         ← services index + topic + org detail pages
│       ├── INDEX.html              ← services directory (renamed from services.html)
│       ├── AFCD/IRD/DPO/Customs/FEH/HD/TD.html    ← 7 org detail pages
│       └── InfoComm/Farming/Mining/Manufacture/Electric/Water/
│           Construction/ImpExp/Catering/Transport/Finance.html
│                                   ← 11 topic pages (1 original + 10 added in v4)
└── artifacts/            ← this folder
    ├── memory.md         ← project context + design system reference
    └── skill-notes.md    ← this file
```

### Linking conventions (3-tier nav graph)
- Services index file is **`INDEX.html`** (renamed from `services.html`; no `services.html` refs remain anywhere). Default tab on load is 主題; URL hash (`#gov` / `#biz` / `#topics`) deep-links via the load-time IIFE → `activateTab(name)`.
- **INDEX → org detail (direct):** gov row is `<a href="AFCD.html">` reusing `.org-item` (`text-decoration:none; color:inherit;`). Back chevron on detail page falls back to its default `href="INDEX.html#gov"`.
- **INDEX → topic → org detail:** topic tile is `<a href="Farming.html">` in INDEX's 主題 grid; the gov item inside `Farming.html` is `<a href="AFCD.html?from=Farming.html">`; detail-page IIFE rewrites `#backLink` so back goes to `Farming.html`.
- **INDEX → topic (back):** topic-page back chevron is `<a href="INDEX.html#topics">` (no IIFE needed — single entry point).
- **To add a topic page:** copy `InfoComm.html`, swap banner SVG/name + the two `.org-list` payloads, make each gov link carry `?from=<thisFile>.html`, then convert the matching INDEX 主題 tile from `<div class="topic-cell">` to `<a class="topic-cell" href="…">`.
- **To add a detail page:** copy `DPO.html` (cleanest `?from=` handler), swap banner + link rows. Keep `id="backLink"` on the chevron and the IIFE intact. Wire row in `INDEX.html#gov` and (optionally) in any relevant topic page with `?from=<topic>.html`.
- **Extending the index strip:** every new 政府 / 商業 item whose 1st char isn't already in the `STROKES` map at the top of `INDEX.html`'s `<script>` must be added there, otherwise it'll fall into `#`. CJK chars get integer stroke counts; ASCII letters are handled automatically by `classify()`.

---

## Verification Checklist

1. Open each file in a browser (or DevTools device mode at 393×852)
2. `home.html` — carousel rotates every 3.5s; guide tabs switch card grid; blue `iD` logo + skyline hero render
3. `Services/INDEX.html` — three tabs show different lists; 服務 nav icon is filled blue with one light tile; first 7 政府 rows link to org detail pages, whose back arrow returns to `INDEX.html#gov`
4. `apply-corpid.html` — clicking the checkbox button enables the 繼續 button
5. `login.html` — two bordered cards; green iAM Smart + blue iD-One pill buttons; boxed-↗ links
6. Bottom-nav labels read 首頁 · 服務 · 掃描 · 待辦 · 本企 with SVG icons (no emoji)
7. Status bar shows SVG signal/wifi + a `79` battery pill
8. All Chinese text displays correctly (Traditional Chinese — Hong Kong)

> **Status:** Code-reviewed for consistency. Not yet browser-screenshot verified — the Bash safety classifier was unavailable during v2, so a headless render could not be captured. Manual browser check recommended.
