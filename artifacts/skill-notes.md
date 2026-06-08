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

---

## Skills & Tools Used

| Tool / Skill | Purpose |
|---|---|
| `Agent (Explore)` | v1 — read all 10 mock images and produce a detailed description of each screen |
| `Read` (on JPEGs) | v2 — directly inspect the actual mock images for pixel-level detail (icons, colors, exact labels) |
| `EnterPlanMode` + `ExitPlanMode` | Design and get approval for implementation approach before writing code |
| `Write` / `Edit` | Create and refine the four HTML files and memory/artifact files |
| `Bash` | Create the `Mobile/` and `artifacts/` directories |

### Key Lesson
The Explore agent's text description was good for structure and copy, but **reading the source images directly was necessary for visual fidelity** — icon shapes, the exact nav labels (本企 vs 企業), the blue (not teal) logo, and the iOS status-bar treatment were only correct after direct inspection.

---

## File Map

```
project/
├── mock-images/          ← source JPEG mock-ups (read-only reference)
│   ├── HomePage1-4.jpeg
│   ├── ServiceCat1-3a.jpeg
│   ├── ApplyCorpID1-2.jpeg
│   └── Login1.jpeg
├── Mobile/               ← output HTML pages
│   ├── home.html
│   ├── services.html
│   ├── apply-corpid.html
│   └── login.html
└── artifacts/            ← this folder
    ├── memory.md         ← project context + design system reference
    └── skill-notes.md    ← this file
```

---

## Verification Checklist

1. Open each file in a browser (or DevTools device mode at 393×852)
2. `home.html` — carousel rotates every 3.5s; guide tabs switch card grid; blue `iD` logo + skyline hero render
3. `services.html` — three tabs show different lists; 服務 nav icon is filled blue with one light tile
4. `apply-corpid.html` — clicking the checkbox button enables the 繼續 button
5. `login.html` — two bordered cards; green iAM Smart + blue iD-One pill buttons; boxed-↗ links
6. Bottom-nav labels read 首頁 · 服務 · 掃描 · 待辦 · 本企 with SVG icons (no emoji)
7. Status bar shows SVG signal/wifi + a `79` battery pill
8. All Chinese text displays correctly (Traditional Chinese — Hong Kong)

> **Status:** Code-reviewed for consistency. Not yet browser-screenshot verified — the Bash safety classifier was unavailable during v2, so a headless render could not be captured. Manual browser check recommended.
