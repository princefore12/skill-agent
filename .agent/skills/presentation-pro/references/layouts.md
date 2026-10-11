# Prznt Perfect — Canonical Template Anatomy

Measured geometry of the 15 canonical templates. All values in **px** on the
1920×1080 canvas, origin top-left; convert to pt with **×0.5** (PowerPoint
canvas is 960×540 pt = 13.333×7.5 in). Fill colors refer to tokens in
`design-tokens.json`.

Common: margins 50px; content 1820×980. Footer on 04–15: Caption @(52,1030),
pagination @(~1583 or 1737,1030) right-aligned to content edge.

Items marked **VERIFY** must be pixel-checked against `assets/figma-refs/`.

---

## 01 — Cover (node 583:473)

- Background: vertical linear gradient — top `Graphite #454E63`, bottom
  `Gray-Dark #A8B1C7` (bottom stop ≈41.7%).
- H1 two-tone @(50,50), box 1073×240, rendered at **72px** (template
  override; token is 64). Accent words → `High #00A1FF`, remaining words →
  `Gray-Dark #A8B1C7`. Sample: "Physical AI …".
- Caption @(50,1016). No pagination.

## 02 — Agenda (node 562:185)

- Background: `Graphite #454E63`.
- H2 "Agenda" @(50,68).
- List: a NATIVE PowerPoint table (client decision 2026-07-23 — rows must be
  add/removable): 5 rows × 2 cols @(50,471.5), col1 149px (numbers, origin
  x52), col2 (labels, origin x199), row height 104px. Borders: top of row 1 +
  bottom of every row, 0.5pt `Gray-Dark #A8B1C7` → the 6 measured lines at
  y=471/575/679/783/887/991. Table style = No Style No Grid, all fills off.
  Number and label are both **48px** (the title "Agenda" is 64px H1).
  No footer on this slide.
- Trap: PowerPoint strokes table borders CENTERED on the row boundary — put
  boundaries at nnn.5 px (table y +0.5px) so a 0.5pt border lands on a single
  reference pixel row instead of smearing across two.

## 03 / 04 / 05 — Section statements

Same pattern, three-line two-tone heading; differ by background:

| # | node | Background | Heading box |
|---|------|------------|-------------|
| 03 | 583:81 | `Semi-Light #DEE6FB` | @(50,68) 1569×192 |
| 04 | 562:148 | `White` | @(50,56) 935×252 |
| 05 | 562:167 | `Navy #071A3C` (light text) | @(50,68) |

Two-tone split resolved from the reference renders (heading is 64px, line-height
100%; the dark/main tone is `Graphite #454E63`, NOT `Main-Navy #051736`):
- **03** (Semi-Light bg): heading is MONOTONE `Graphite #454E63` (no accent). No footer.
- **04** (White bg): accent line "Seeing beyond" = `High #00A1FF`, continuation
  ("signals to reveal patterns / hidden in plain sight") = `Gray-Dark #A8B1C7`.
  Footer present.
- **05** (Navy bg): heading is MONOTONE `White-Cool #EDEFF2`. No footer.
The same White-bg split (accent `High` line + `Gray-Dark` rest) applies to 06–09,
11 and 12; the 10/13/14 title style instead pairs `Graphite #454E63` with a `High`
highlight word.

## 06–09 — Text + image placeholder

Heading @(53,50) unless noted; placeholder fill `White-Cool #EDEFF2`. Corner
radius resolved to **0px (sharp corners)** — a strict pixel check on the top-left
corner of every placeholder (06/07/08/09/10/13) shows 0px inset, i.e. square
corners, not the ~8px the token guessed.

| # | node | Heading box | Placeholder @ | Placeholder size |
|---|------|-------------|---------------|------------------|
| 06 | 562:214 | 897×215 | (663,351) | 1207×679 (bottom-right) |
| 07 | 583:88 | — | (970,50) | 900×980 (right half, full height) |
| 08 | 583:105 | — | (970,50) | 900×483 (top-right, landscape) |
| 09 | 583:142 | @(53,432) v-centered | (817,50) | 1053×980 |

## 10 — Four segment cards (node 562:3)

- H1 two-tone @(50,50). Sample: "Addresses $25B TAM".
- Logo frame 190×38 @(1672,50) (top-right).
- 4 H4 labels @y463, x = 50 / 510 / 970 / 1430
  (Automotive / Aviation / Defense / Semiconductors).
- 4 card placeholders @y509, same x, each 440×483, fill `White-Cool`.
- GRID-SNAPPED (client rule 2026-07-26): each card = exactly 3 columns,
  edges on the guides, gaps = the 20px gutters. The Figma canon had
  438px @ x514 — 2–4px off its own grid; corrected. All card rows
  (2/3/4 cards → 900/593.3/440px) quantize to whole columns the same way.

## 11 — Heading + body + image (node 562:231)

> Updated per client rules 2026-07-23 (R5: titles always 64px; R13: empty
> column before the image). The Figma reference PNG shows the OLD state
> (48px Title Case heading, 695px body) — pixel-compare of the text zones
> is no longer meaningful for 09/11/12.

- H1 three-line two-tone heading @(50,36) 593×215, 64px lh 100%.
- Body @(50,830) 593×175 (5 lines, foot ~1002, clear of the footer).
- Image @(817,50) 1053×980 — grid cols 6–12; col 5 stays EMPTY (R13).

## 12 — Heading + 2 bodies + image (node 562:202)

> Same client-rule update as 11: heading now H1 64px @(50,~40) 593 wide,
> sentence case; reference PNG shows the old 48px state.

> Known limit: the reference's 25px body pitch (20px × 124%) is unreachable —
> PowerPoint quantizes exact line spacing to whole points (= even px on the
> 1920 canvas), so the engine renders 26px and the residual ±3px drift is
> centered. Splitting into per-line boxes would fix pixels but break text
> editability — rejected.

- H2 @(50,40); image @(817,50) 1053×980.
- Body block 1 @(50,668) 593×152; body block 2 @(50,868) 593×125.

## 13 — Image left + two captioned blocks (node 562:317)

- H1 two-tone @(50,50). (Figma sample contains typo "Typografy".)
- Image @(50,203) 1053×827 (left).
- Right column @x1277: block A = H4 + body @(1277,235) 593×336;
  block B = H4 "12.43 msec" + body @(1277,662) 593×336.

## 14 — Bar chart, shapes only (node 562:41)

- H2 two-tone @(50,50) 1070×128.
- 5 bars (sharp rects): x = 357 / 665 / 970 / 1277 / 1583, width ≈285.
  Common bottom baseline resolved to **y≈662** (NOT y727). Measured bar tops
  569 / 449 / 318 / 241 / 120 → heights 93 / 213 / 344 / 421 / 542 (ascending).
- Fills: bar 1 `High #00A1FF`, bars 2–5 `High-1`…`High-4`.
- Value labels (Num-Head **48px**, `Graphite #454E63`, left-aligned ~25px inside
  each bar, top ~28px below the bar top): only bars 2–5 carry 30x / 130x / 153x /
  351x. Resolved: there is **NO 5th value label** — the shortest `High` bar (bar 1)
  is unlabelled.
- Baseline vector line under bars.
- Data values: a NATIVE PowerPoint table (client decision 2026-07-23),
  4 rows × 9 cols @(357,731.5) — 5 content columns + 4 narrow SPACER columns
  (widths px: 285/23/283/22/286/21/286/20/288). Underlines are SEGMENTED:
  lnB only on content cells, spacers bare → the line breaks between columns
  exactly as in Figma. Column 1 has values/underlines in rows 1–2 only
  (msec, W); columns 2–5 in all 4 rows. Rows 65px, integer boundaries
  (797/862/927/992 — soft two-row lines), borders 0.5pt `Gray-Dark #A8B1C7`,
  cells 32px Graphite, vertically centered (client rule 2026-07-26).
- Line color note: these separators LOOK lighter in the reference (lum ~216)
  but that is a 1px Gray-Dark stroke on an integer pixel boundary anti-aliased
  50/50 with white (2×211−255 = #A8B1C7 exactly). ALL table separators in the
  system are Gray-Dark.
- Boundary rule (two kinds of lines!): slide 02/15 reference lines are CRISP
  single rows → row boundaries at nnn.5 (stroke lands on one row). Slide 14
  reference lines (and the chart axis, Graphite) are SOFT two-row AA → row
  boundaries at INTEGERS (stroke straddles, 50/50). Always measure which kind
  the reference has before picking the boundary.
- NOTE: the CHART is NOT a native chart object — bars are shapes,
  pixel-perfect (client decision, 2026-07-23).

## 15 — Data table, text + lines (node 562:99)

- H2 "Ultra-high-resolution sensing" @(50,40) 745×128.
- A NATIVE PowerPoint table (client decision 2026-07-23), 7 rows (header +
  6 data) × 5 cols @(50,320.5), width 1820. Style = No Style No Grid, no
  fills, rows freely add/removable.
- Horizontal borders ONLY (no verticals, no line above the header):
  header underline **1.5pt = 3px** (reference rows y391–393), data-row
  underlines **0.5pt = 1px** at y≈493/594/695/795/896/991. All borders
  `Gray-Dark #A8B1C7`. Row boundaries sit at nnn.5 px (centered-stroke trick,
  same as slide 02). Cell text vertically centered (client rule 2026-07-26).
- Header `Column 1` ×5 (32px) glyph tops y336; column origins x =
  50/418/786/1154/1522 — header col2 gets +16px cell marL (its label sits at
  x434 while data below it sits at x418, per the reference).
- Data cells: Table-Numbers (26px), glyph tops 401/504/606/709/811/914.
- Cell text is VERTICALLY CENTERED in its row (client rule 2026-07-26,
  anchor="ctr", marT=0) — the old top-anchored marT calibration is retired.

---

## Implementation notes (apply to every template)

1. **Two-tone headings** = one text frame, multiple runs with different
   colors (accent `High` + muted/main color).
2. **U+2028** line separators inside Figma text → explicit line breaks
   (`add_break`), never literal U+2028 in PPTX.
3. **Tracking** −1%: rPr@spc = −round(size_pt) (1/100 pt units).
4. Line-height = paragraph line_spacing as a multiple (1.0 / 1.15 / 1.32…).
5. px→pt **×0.5** everywhere (960pt / 1920px); positions via `Pt()`, never
   `Inches()` rounding.
