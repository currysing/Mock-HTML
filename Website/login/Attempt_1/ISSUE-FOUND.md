# HTML Display Issues — Root Cause Analysis

## Problem Summary
All HTML files render poorly when opened directly in a browser because they are saved snapshots of a **Vue.js / Vite Single Page Application (SPA)**. The JavaScript fails to execute when loaded via the `file://` protocol.

---

## Root Cause: `type="module"` + `crossorigin` CORS Blocking

Every HTML file contains:

```html
<script type="module" crossorigin="" src="assets/index-....js"></script>
```

Browsers (Chrome, Edge, Firefox) block ES module scripts loaded from `file://` origins due to CORS policy. Error in console:

> Access to script at 'file:///...' from origin 'null' has been blocked by CORS policy.

**Consequence:** The Vue application never initializes, so dynamic components, styling logic, dropdowns, carousels, and interactive elements remain broken or unstyled.

---

## Secondary Issues Found

### 1. Missing JavaScript Chunks
The main JS bundles reference ~30+ lazy-loaded chunk files that **do not exist** in `assets/`:
- `assets/Register-Bs-LHtU_.js`
- `assets/PageContainer.vue_vue_type_script_setup_true_lang-....js`
- ...and many others.

Even with CORS resolved, navigation and dynamic features will fail due to missing chunks.

### 2. Mismatched Build Versions
- `index.html` uses: `index-CoIE853Z.js` + `index-Cfx39piE.css`
- All other 20 pages use: `index-CvaI-sSB.js` + `index-uitrUlFZ.css`

This suggests pages were saved from different builds or at different times.

### 3. Missing Image Assets
Per `missing-assets-report.txt`:
- `assets/service_item1-Gb0TXat9.png` through `service_item6`
- `favicon.ico`

### 4. External Links Still Point to Live Site
Navigation links reference `https://uat-webportal.corpid-np.gov.hk/...` instead of local `.html` files.

---

## Recommended Fix

**Do not open files via double-click.** Serve them over HTTP instead.

From the `login/` directory, run one of:

```bash
# Node.js
npx serve .

# Python
python -m http.server 8000

# Then visit http://localhost:8000
```

Or use **VS Code Live Server** extension.

---

## Suggested Follow-up Actions

| Priority | Task |
|----------|------|
| High | Consolidate all HTML files to use the **same** JS/CSS bundle version |
| High | Identify and restore missing lazy-loaded JS chunks, or rebuild from source |
| Medium | Replace external absolute URLs with relative `.html` links |
| Low | Add missing image assets (`service_item*.png`, `favicon.ico`) |
