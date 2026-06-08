# CorpID Mobile Pages — Memory

## Project Context

This project reproduces a Hong Kong government CorpID digital identity portal as static HTML mock-up pages sized for iPhone 16 Pro (393×852 CSS pixels). Source mock-up images are in `mock-images/`. All output pages live in `Mobile/`.

> **v2 update:** After the first pass, the pages were refined against the actual mock images for higher fidelity — emoji icons replaced with inline SVG, corrected bottom-nav labels, iOS-style status bar, blue `iD` logo, masonry card grid, and bordered login cards.

### Pages Built

| File | Screen |
|---|---|
| `Mobile/home.html` | Home/landing — sky-gradient hero with CSS skyline + blue `iD` logo, "註冊 CORPiD" promo banner, announcement carousel (3 slides, auto-advances every 3.5s, animated pill dots), guide tabs (新手攻略 / 中小企指南 + 更多 link), masonry service card grid, bottom nav (首頁 active) |
| `Mobile/services.html` | Services directory — 3-tab list (主題 / 政府及有關機構 / 商業及其他機構), 12 items each, bottom nav (服務 active = filled blue grid) |
| `Mobile/apply-corpid.html` | T&C scroll page — 7 sections of Chinese terms, checkbox button enables the 繼續 button via JS |
| `Mobile/login.html` | Auth method selection — bordered white cards on gray page; iAM Smart green pill button (phone-check icon) + 2 boxed-↗ links; iD-One blue pill button + 1 link; no bottom nav |

---

## Design System

**Viewport:** `<meta name="viewport" content="width=393, initial-scale=1">`
**Frame:** `.phone-frame` — `width: 393px; height: 852px; overflow: hidden; border-radius: 48px`, background `#eef1f4`

### Color Tokens

| Token | Value | Usage |
|---|---|---|
| Header blue | `#155CB0` | Status bar, headers, search area, active tab/nav, login section headings |
| Accent blue | `#1155BB` | Primary buttons, AI 助手 pill, `iD` logo, home active dot |
| Light-tile blue | `#4DA6E0` | One tile of the active 服務 grid nav icon |
| Green | `#3d7d68` | iAM Smart button |
| Disabled | `#A8C8E8` | Disabled 繼續 button |
| Link teal | `#157a8c` | External links + boxed ↗ icon stroke |
| Nav inactive | `#5b6168` | Inactive bottom-nav icons/labels |
| Page bg | `#eef1f4` | Phone frame + scroll backgrounds |
| Text dark | `#1a1a1a` | Body/heading text |
| Text muted | `#7c8590` / `#9aa0a6` | Secondary text, card subtitles, placeholders |

### Card Palette (pastel masonry backgrounds, home.html)
`#dde9f6` blue · `#d9efe6` green · `#f5e7d6` beige · `#e6e1f2` purple · `#f7e1e8` pink · `#f7f0d8` yellow · `#d8eef0` teal
Cards have a faint diagonal hatch overlay (`repeating-linear-gradient`) and an emoji glyph anchored bottom-right; the first card uses `.tall` (`grid-row: span 2`).

### Font Stack
`-apple-system, 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif`

### Layout Pattern
```
.phone-frame → flex column
  status-bar  (flex-shrink: 0, 50px, #155CB0)   — on home it overlaps the hero (negative margin)
  header      (flex-shrink: 0, 50px, #155CB0)    — optional (services/apply/login)
  body-scroll (flex: 1, overflow-y: auto)
  bottom-nav  (flex-shrink: 0, 78px, white, border-top)  — home/services only
```

### Status Bar Template (inline SVG, not emoji)
50px tall, `#155CB0` (or transparent over the home hero), bottom-aligned content.
- **Time** left: 15px white 600 weight
- **Signal**: 4 ascending `<rect>` bars
- **WiFi**: two arcs + dot built from `<path>`/`<circle>`
- **Battery**: pill showing `79` — white text knocked out via `-webkit-text-fill-color`, 79% fill via `linear-gradient(... 79%, transparent 79%)`, plus a small tip nub

### Header Template (inline SVG icons)
Back chevron (`<path>`), three-dot menu (`3× <circle>`), a 1px white divider, and an X close (two crossed `<path>` strokes). Title absolutely centered.

### Bottom Nav Template — 5 tabs, inline SVG icons
Correct labels (left → right): **首頁 · 服務 · 掃描 · 待辦 · 本企**
(Earlier draft wrongly used 主頁/企業 and emoji — fixed.)

| Tab | Icon (inline SVG) | Active treatment |
|---|---|---|
| 首頁 | house outline | filled solid `currentColor` |
| 服務 | 2×2 rounded-square grid | filled; one tile uses light-blue `#4DA6E0` |
| 掃描 | QR code (corner squares + dots) | n/a in mocks |
| 待辦 | clipboard with lines | n/a |
| 本企 | building/factory with columns | n/a |

Icons use `stroke="currentColor"` / `fill="currentColor"`; the `.nav-item` sets color — `#5b6168` inactive, `#155CB0` active. Active item swaps to the filled icon variant.

---

## Implementation Notes

- All CSS and JS are **inline** — no external files or CDNs
- Pages work by opening the `.html` file directly in a browser
- JS is minimal: tab switching, carousel rotation, checkbox toggle only
- **No raster images embedded** — all icons/logos are hand-authored inline SVG; the hero "photo" is a CSS sky gradient plus a `<svg>` skyline silhouette; card art is emoji + CSS hatch overlays
- When adding a page, copy the status-bar / header / bottom-nav SVG blocks from `home.html` or `services.html` as the canonical templates

## Verification Status
- Code-reviewed for consistency across all four files
- **Not yet browser-screenshot verified** — the Bash safety classifier was unavailable during the v2 pass, so a headless-browser render could not be captured. Recommend opening each file in DevTools device mode (393×852) to confirm spacing/colors.
