# CorpID Mobile Pages — Memory

## Project Context

This project reproduces a Hong Kong government CorpID digital identity portal as static HTML mock-up pages sized for iPhone 16 Pro (393×852 CSS pixels). Source mock-up images are in `mock-images/`. All output pages live in `Mobile/`.

> **v2 update:** After the first pass, the pages were refined against the actual mock images for higher fidelity — emoji icons replaced with inline SVG, corrected bottom-nav labels, iOS-style status bar, blue `iD` logo, masonry card grid, and bordered login cards.

> **v3 update (services only):** `Mobile/Services/INDEX.html` (originally `services.html`) was redone against a new set of `mock-images/service_cat_*.PNG`. The 主題 tab became a 3-col icon grid (21 categories); the 政府 / 商業 tabs became logo-list rows. New mock data:
> - **主題 (21, row order):** 農業林業及漁業 · 採礦及採石 · 製造 · 電力及燃氣供應 · 自來水供應/污水/廢棄物/污染防治 · 建造 · 進出口貿易批發及零售業 · 運輸倉庫郵政及速遞 · 住宿及膳食服務 · 資訊及通訊 · 金融及保險 · 地產 · 專業科學及技術 · 行政及支援服務 · 公共行政 · 教育 · 人類保健及社會工作 · 藝術娛樂及康樂 · 其他服務 · 家庭住戶內部工作 · 享有治外法權的組織及團體
> - **政府及有關機構 (16):** 漁農自然護理署 · 稅務局 · 數字政策辦公室 · 海關 · 食物環境衞生署 · 醫務衞生局 · 運輸署 · 入境事務處 · 土木工程拓展署 (CEDD) · 土地註冊處 · 工業貿易署 · 商務及經濟發展局 · 康樂及文化事務署 · 路政署 · 運輸及物流局 · 公務員事務局 — (first 7 added later from individual logo PNGs in `mock-images/`; 數字政策辦公室 + 醫務衞生局 had **no sample**, so are approximated — digital-blue node mark + red HKSAR bauhinia emblem)
> - **商業及其他機構 (6):** 香港數碼港管理 (Cyberport) · 香港科技園 (HKSTP) · 香港生產力促進局 (hkpc) · 香港金融管理局 (HKMA) · 貿易通電子貿易 (Tradelink) · 易簽寶香港 (eSign.AI)
> - Org logos are **simplified inline-SVG approximations** (project's no-raster rule), not pixel-accurate brand artwork. Status bar kept the shared `79` pill (time 12:34) rather than the mock's plain full battery, for cross-page consistency.

> **v4 update (services expansion):**
> - **28 made-up demo companies** added to 商業及其他機構: 8 CJK (stroke 3–10, agriculture/mining/manufacturing/electricity) — 大豐農業 · 天耀礦業 · 永發製造廠 · 光明電力工程 · 良禾農產 · 金石礦業集團 · 南華製鐵 · 海能電力; and 20 English (A–M, water/construction/wholesale/accommodation/transportation/financial) — Aquaclear · Atlantic Builders · Beacon Hospitality · BlueWave Logistics · Crystal Springs · Drake Mercantile · Eastwind Trading · Fairmont Builders · Goldcrest Financial · Greenway Waterworks · Harbour View Resorts · Imperial Wholesale Mart · Jade Garden Inn · Keystone Construction · Kingsbridge Bank · Landmark Express · Liberty Reservoir · Merchant Marine · Metro Plaza Hotels. Each has a colored-circle + 2-letter monogram SVG logo (cyan/orange/green/purple/red/dark-blue per industry).
> - **iOS Contacts-style sorting/indexing** added to both 政府 and 商業 tabs: a generic `buildIndex(panelId, barId, prefix)` sorts `.org-item`s by `classify(name)` → CJK (stroke count via `STROKES` map) first, then ASCII A–Z, then `#` bucket; inserts `.org-group-header` rows (`"N 劃"` / `"A"`); and populates a right-edge `.index-bar` (`#gov-index-bar` / `#biz-index-bar`) of tappable scroll-to-group items. `activateTab()` toggles the matching bar's `.show` class.
> - **Gov items lost their `>` chevron** (all 16 `<span class="org-arrow">` removed) to mirror the biz section's clean look.
> - **10 industry topic pages** created in `Mobile/Services/` — `Farming.html` · `Mining.html` · `Manufacture.html` · `Electric.html` · `Water.html` · `Construction.html` · `ImpExp.html` · `Catering.html` · `Transport.html` · `Finance.html` — all modelled on `InfoComm.html` (status bar / header / pale-blue topic banner / two `.org-list` sections / bottom nav). Each is wired to the matching 主題 tile in `INDEX.html` (the `<div class="topic-cell">` blocks are now `<a>` links). The page banner reuses the same SVG icon as the topic tile.
> - **Dynamic back-navigation via `?from=` URL parameter** — every detail-page link inside a topic page uses `<a href="AFCD.html?from=Farming.html">`. Each detail page (`DPO.html` · `AFCD.html` · `FEH.html` · `Customs.html` · `TD.html` · `IRD.html`) has `id="backLink"` on its back chevron plus a small IIFE that reads `location.search`, validates the value against `/^[A-Za-z0-9_-]+\.html(#[A-Za-z0-9_-]+)?$/`, and rewrites the chevron's `href`. Without the param it falls back to the default `INDEX.html#gov`.

### Pages Built

| File | Screen |
|---|---|
| `Mobile/home.html` | Home/landing — sky-gradient hero with CSS skyline + blue `iD` logo, "註冊 CORPiD" promo banner, announcement carousel (3 slides, auto-advances every 3.5s, animated pill dots), guide tabs (新手攻略 / 中小企指南 + 更多 link), masonry service card grid, bottom nav (首頁 active) |
| `Mobile/Services/INDEX.html` | Services directory (renamed from `services.html`) — 3 tabs (主題 / 政府及有關機構 / 商業及其他機構). **v3** = layout; **v4** = both 政府 & 商業 use the same iOS-Contacts-style sort + right-edge stroke/letter index bar; 政府 items chevron-less to match 商業. 主題 is a **3-col icon grid** of 21 industry categories; each tile is now an `<a>` linking to its topic page (10 wired so far). Tab can be deep-linked via URL hash (`INDEX.html#gov`). |
| `Mobile/Services/<TOPIC>.html` | **Topic pages**, all modelled on `InfoComm.html` (status bar / header → `INDEX.html#topics` / pale-blue topic banner / two `.org-list` sections — 政府 + 商業 / bottom nav). Built: `InfoComm.html` · `Farming.html` · `Mining.html` · `Manufacture.html` · `Electric.html` · `Water.html` · `Construction.html` · `ImpExp.html` · `Catering.html` · `Transport.html` · `Finance.html`. Each gov item inside a topic page links to its detail page with a **`?from=<thisTopic>.html`** query string. |
| `Mobile/Services/<ORG>.html` | **Org detail pages**, all modelled on AFCD.html (same status bar / header / bottom nav; pale-blue org banner = logo + name; link rows = `<a href="#">` placeholders; back chevron = `<a id="backLink" href="INDEX.html#gov">` + IIFE that rewrites `href` from `?from=` param). Built: `AFCD.html` 漁農自然護理署 · `IRD.html` 稅務局 · `DPO.html` 數字政策辦公室 · `Customs.html` 海關 · `FEH.html` 食物環境衞生署 · `HD.html` 醫務衞生局 · `TD.html` 運輸署. The `?from=` handler is wired on all but `HD.html` (not currently linked from any topic). |
| `Mobile/apply-corpid.html` | T&C scroll page — 7 sections of Chinese terms, checkbox button enables the 繼續 button via JS |
| `Mobile/login.html` | Auth method selection — bordered white cards on gray page; iAM Smart green pill button (phone-check icon) + 2 boxed-↗ links; iD-One blue pill button + 1 link; no bottom nav |
| `Mobile/Settings/INDEX.html` | Settings landing — recolored from the iAM Smart green/orange mock to **CorpID blue** (`#155CB0`). Blue profile header (white `iD` mark + 測試員 + eye + logout), pale-blue 具有數碼簽署功能 promo (CorpID wordmark, not 智方便). Two sections: **應用程式設定** (切換至簡易模式 toggle · 顯示 · 通知 · 個人碼 · 儲存空間 · 使用指南 · 需要幫忙 · 關於 CorpID · 服務條款 · 程式版本 4.14.0) and **戶口設定** (戶口資料 · 使用紀錄 · 安全及私隱 · 登出). Standard CorpID bottom nav (本企 marked active — mock's 設定 tab has no CorpID equivalent). Easy-mode toggle is JS-interactive. |
| `Mobile/Settings/<SUB>.html` | **10 settings sub-pages**, each from a `mock-images/Settings/Setting*.jpg` mock, all recolored green→CorpID blue. Shared sub-page chrome = **white** status bar + **white** header (black text/icons, back chevron → `INDEX.html`, centered title, bottom border) — distinct from INDEX's blue profile header. Built: `Display.html` 顯示 (語言 pill · 字體大小 preview + 3-stop slider · 無障礙設計) · `Notification.html` 通知 (允許CorpID取用 / 通知設定, push toggle) · `PersonalCode.html` 個人碼 (掃描有效期 banner + 5–1分鐘 radio list, JS single-select, 5分鐘 default) · `Storage.html` 儲存空間 (single outlined 刪除緩存資料 button on gray bg) · `Guide.html` 使用指南 (主頁/服務/訊息/我的/設定 rows) · `Help.html` 需要幫忙 (**3 JS tabs** 關於CorpID/相關服務/如何使用, FAQ `.q` rows, blue underline on active tab) · `Terms.html` 服務條款 (5 terms rows) · `AccountInfo.html` 戶口資料 (info banner + 身份證資料/電子證書 `.field` k-v blocks, demo data 梁冠誠/LEUNG Koon Sing, masked fields w/ eye icon, 已驗證 email) · `UsageLog.html` 使用紀錄 (過往90日 banner + 8 demo log entries) · `Security.html` 安全及私隱 (安全設定 / 資料私隱 rows). 智方便→CorpID, 智能身份證→商業登記證 text swaps throughout. |

> **Folder note:** the services page + all topic / org detail pages live in `Mobile/Services/`. The services page was renamed `services.html` → **`INDEX.html`** (no `services.html` refs remain). Three navigation flows:
> 1. **INDEX → detail** (direct from 政府 tab): `<a href="AFCD.html">` — detail back chevron falls back to `INDEX.html#gov`.
> 2. **INDEX → topic → detail**: topic tile is `<a href="Farming.html">`; gov item inside the topic is `<a href="AFCD.html?from=Farming.html">`; detail-page IIFE rewrites `#backLink` → `Farming.html`.
> 3. **INDEX → topic → INDEX**: topic back chevron is `<a href="INDEX.html#topics">`.
>
> Pattern for future topic pages: copy `InfoComm.html`, swap banner icon/name + the two `.org-list` payloads, ensure gov-item hrefs carry `?from=<thisFile>.html`, and turn the matching `INDEX.html` topic tile into an `<a>`. Pattern for future detail pages: copy `DPO.html` (it has the cleanest `?from=` handler), swap banner + link rows, keep `id="backLink"` on the chevron + the IIFE intact.

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
