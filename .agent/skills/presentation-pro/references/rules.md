# Prznt Perfect — Design Rules

Normative rules extracted from the six "Rules" slides of the source Figma
library (file `[private]`). Where a rule slide contradicts the
Figma variables, the variables win (see
`design-tokens.json > known_discrepancies`).

All generated decks are **English only**.

## R1 — Sentence case only

Never set text in ALL CAPS. Never Capitalise Each Word of a headline.

- Wrong: `SECTION HEADING`, `Section Heading`
- Correct: `Section heading`

## R2 — Swiss paragraphs

Multiple paragraphs are separated by a blank line, never by a first-line
indent (red line).

## R3 — Tracking −1% on all text

Every text run uses letter-spacing of −1% of its font size. This applies to
all 10 type styles without exception.

## R4 — No period at the end of headings

A heading is a label, not a sentence. `Our key results` — never
`Our key results.`

## R5 — Slide title size: always H1 64px (= 32pt in PowerPoint)

Every slide title is **64px H1, line-height 100%**, regardless of word
count (client rule 2026-07-23 — supersedes the earlier H1/H2 word-count
split from the Figma rules slides). H2 48px remains in the scale for
non-title uses (agenda list items and similar large text). The 72px cover
heading (template 01) is the single canonical exception.

## R6 — H1 limits

An H1 heading must not exceed **3 lines** of text, must not be taller than
**6 grid rows**, and must not be wider than **6 grid columns**.

## R7 — Bottom line alignment

Text blocks and images that share a zone align to a common bottom line.

## R8 — Typography system

Only **Arial Regular**. The 10 styles (H1, H2, H3, H4, Body, Body-Small,
Caption, Num-Head, Table-Numbers, Pagination) are defined in
`design-tokens.json`. Never invent intermediate sizes; never use bold or
italic.

## R9 — Color system

Only the 14 palette colors from `design-tokens.json`. Accent = `High
#00A1FF`, used sparingly (accent words in two-tone headings, primary chart
series). Chart series follow the fixed order High → High-1 → High-2 →
High-3 → High-4.

## R10 — Layout grid

- 12 columns, 20px gutter; 26 rows, 14px gutter.
- Margins: 50px on top/left/right; **bottom margin is 86.5px** — the bottom grid
  boundary sits at **y=993.5** (client rule 2026-08-06), which is where a
  PowerPoint drawing guide reads **8.00 cm below slide center**. (Not 1030, and
  not the earlier over-raised 942.)
- Content area: **1820×943.5px** (top-left origin 50,50; bottom edge y=993.5).
- Every element snaps to the grid. Canonical templates (layouts.md) may use
  measured coordinates; **new** compositions must be built on the grid and must
  not cross y=993.5 (the footer band below is reserved for caption/pagination).

## R11 — Footer

Caption (16px) bottom-left at (52,1033); page number (14px) bottom-right at
y~1048. Applies to slides of type 04 and 06–15. NO footer on full-color
statement/agenda slides (02, 03, 05). Cover: caption at (50,1016), no page
number. The footer is UNCHANGED by the R10 bottom-boundary raise: it sits in
the enlarged bottom margin band, below the grid boundary (y=942) by design.

## R12 — Flat design

No shadows, no blurs, no masks, no strokes-as-decoration. Allowed effects:
the cover gradient and flat fills only.

## R13 — Empty column between text and image

Whenever a text block and an image sit SIDE BY SIDE (overlap vertically),
at least **one full empty grid column** separates them — on whichever side
the image is (client rule 2026-07-23). E.g. image starting at column 6
(x817) → text occupies columns 1–4 (boxes end at x643); image at column 7
(x970) → text occupies columns 1–5 (end x797). Text ABOVE or BELOW an image
(no vertical overlap) is exempt.

## R15 — Table cell text is vertically centered

In every native table (agenda 02, chart values 14, data table 15 and any
new one), cell text is vertically centered within its row (client rule
2026-07-26): tcPr anchor="ctr", zero top margin. Never position cell text
with top-anchored margin calibration.

## R16 — Paragraphs stay together

One or two body paragraphs are ONE GROUP: a single tight vertical stack that
never drifts apart, treated as a unit (client rules 2026-07-26 / 2026-08-06).

- The gap between the two paragraphs is **exactly two paragraph spacings**
  (`2 × the font size` — ~52px for Body 26px; the earlier "~56px" example).
- The GROUP is **bottom-anchored to the bottom grid line** (y=993.5): its
  bottom edge sits on the grid, like a card (R27) — it does not float centered.
- Never scatter paragraphs down the slide to fill vertical space.

Build it with `components.add_paragraph_group(slide, [p1, p2], cols=4)` — it
balances each paragraph (R31), stacks them two-spacings apart, and bottom-anchors
the group. Pass `y_px=` to top-place instead.

## R17 — Paragraph width: 4 columns, 5 max

A body paragraph is never wider than **5 grid columns (746px)**. Prefer
**4 columns (593px)**; use 5 only for genuinely large volumes of text
(client rule 2026-07-26). This holds with or without an adjacent image
(R13 still applies on top when an image is present).

## R18 — No eyebrows, kickers, or labels above the title

The slide title is ALWAYS the topmost text element on a slide (client rule
2026-07-26). Small category labels above the heading — "Press release",
"Case study", section kickers, accent-colored eyebrows — do not exist in
this design system and are forbidden. Footer caption/pagination and the
cover are the only canon exceptions.

## R19 — No badges, pills, or text inside filled shapes

Pagination is plain 14px text via the engine footer — never a filled
rounded "Page N / M" badge. Text never sits INSIDE a filled shape: cards
are bare White-Cool rectangles with separate text boxes on top (use the
sanctioned card components), tables are native table objects. Rounded
corners do not exist anywhere in the system.

## R20 — Series slides: invert the hierarchy

A source run of slides sharing one title ("How X works" ×N with subtitles)
is normalized (client rule 2026-07-26): strip "n/m" counters; short parts
collapse into ONE slide (series title + card row); long parts get an
overview slide (series title + title-cards) followed by per-part slides
where the H1 is the PART's own topic and the shared series title becomes a
one-line H3 36px Gray-Dark subtitle BELOW the H1 (never above — R18). Part
slides carry a full-height right image placeholder (817,50) 1053×980.

## R21 — Theme palette = design system

Every generated deck ships with its PowerPoint **theme color scheme**
overwritten by the Prznt Perfect palette (client rule 2026-08-05), so the
color picker's *Theme Colors* row offers design-system colors and nothing
off-brand. The engine applies this automatically in `Deck.save()`
(`brand_theme=True`); the linter fails any deck whose scheme is not the brand
palette. Slot mapping (`przntperfect/theme.py`, keyed to the "Color System"
board — White is kept only as the lt1 background, "except white" per the
request):

| slot | token | hex | picker |
|------|-------|-----|--------|
| lt1 | White | `#FFFFFF` | Background 1 |
| dk1 | Black | `#161A22` | Text 1 |
| lt2 | White-Cool | `#EDEFF2` | Background 2 |
| dk2 | Navy | `#071A3C` | Text 2 |
| accent1 | High | `#00A1FF` | Accent 1 (primary) |
| accent2 | Graphite | `#454E63` | Accent 2 |
| accent3 | Gray-Dark | `#A8B1C7` | Accent 3 |
| accent4 | Grey-Light | `#CCD1DB` | Accent 4 |
| accent5 | Semi-Light | `#DEE6FB` | Accent 5 |
| accent6 | High-1 | `#75C3F0` | Accent 6 (chart tone 2) |

This is purely additive: templates paint with explicit sRGB, never scheme
references, so the theme changes only the picker — no rendered pixel moves.

## R22 — Chart bar width auto-scales with the count

A bar is always a **whole number of grid columns** wide and sits on a column
boundary — never a thin, off-grid bar (client rule 2026-08-05). The count is
free — a chart may have as many bars as fit the width (client rule 2026-08-06):

* **up to 6 bars → two columns each** (286.67px); 6 two-column bars fill the
  full 12-column width.
* **7–12 bars → one column each** (133.33px), so the extra bars still fit.

Build geometry with `composites.bar_chart_geometry(n, start_col=0)` → `(xs,
width)`; with the default `span_cols=None` it auto-picks 2 or 1 columns from `n`
and lays the bars one step apart with a gutter between them. Bars are
grid-aligned from the left, so 6 (two-col) or 12 (one-col) span the full width;
in-between counts use `n` columns from the left. Pass the SAME `n`/`start_col`
to `components.add_chart_data_table` so its segmented underline tracks the bars
(R14). Never hand-pick a narrow bar width.

## R23 — Reusable components snap to the grid by construction

The card / subhead / annotation / table variants live in
`przntperfect/components.py` and are placed by **grid column**, never raw
pixels ("элементы встают всегда чётко по сетке"). Each builder takes a 0-based
`col`; its width is a fixed column span, so an element can only land on the
12-column grid. Canonical row placements: span 6 (bio/market) at cols 0,6;
span 4 (metric) at 0,4,8; span 3 (problem/solution/annotation) at 0,3,6,9;
span 5 (numbered table) at col 7. Card inner padding is **64px** (not the 40px
of the older `cards.add_card_row`). Component → builder map:

| Figma | builder | span |
|-------|---------|------|
| Subhead | `add_subhead` | ≤4 |
| Card-1 / Card-1a (bio) | `add_bio_card` | 6 |
| Card-2 (market) | `add_market_card` | 6 |
| Card-3 (problem) | `add_problem_card` | 3 |
| Card-4 (solution) | `add_solution_card` | 3 |
| Card-5 / Card-5a (metric) | `add_metric_card` (native table) | 4 |
| Card2-Table-Numbers | `add_numbered_table` (native table) | 5 |
| Annotation-1 / Annotation-2 | `add_annotation` | 3 |

Card-5 and Card2-Table-Numbers are real `GraphicFrame` tables (rows
addable/editable), horizontal rules only, Grey-Light separators — same
"No-Style-No-Grid" technique as the agenda/data tables (see `tables.py`).

## R24 — Subhead is balanced and ≤ 4 columns

The subhead under a title is **Body-Small 20px Gray-Dark**, never wider than
**4 grid columns**, and its lines are **balanced** — even length, never a long
first line then a single orphaned word (client rule 2026-08-05). `add_subhead`
does this automatically. Line balancing is available for ANY paragraph via
`textbalance.balance_lines(text, max_width_px, size_px)` (used by the card
bodies too); it inserts explicit `\n` so the wrap comes out even.

## R25 — Card typography is fixed

Text INSIDE any card follows one standard, in PowerPoint points (client rule
2026-08-05):

- **Text heading** — 18pt (36px)
- **Body / main text** — 16pt (32px)
- **Number heading** (a heading that is a bare number, e.g. "01") — 24pt (48px)

This holds for every card: `cards.add_card_row` and all `components.py` variants
(bio, market, problem, solution, metric, numbered table). The sizes live in the
`CARD_TITLE_PX` / `CARD_BODY_PX` / `CARD_NUM_PX` constants in `cards.py`; never
hand-set a card's font size. (The bio card's role sub-label stays a small
Body-Small caption — it is neither the heading nor the main text.) Reminder:
px = pt × 2 because the engine's px→pt is ×0.5.

## R26 — A number heading and its title are one tight block

When a card's heading is a **number** (e.g. "01", "$4M", "3x") and the title
word sits on the line below it, there is **NO gap** between the two — the number
and the title read as two tight consecutive lines (client rule 2026-08-06). The
title sits directly under the number (one number-line down, ~48px), not spaced
away from it. `cards.add_card_row` and `components.add_solution_card` already do
this; never widen the number→title gap.

## R27 — Cards sit on the bottom grid line

A card row is **bottom-anchored to the bottom grid line** (y=993.5) — the card's
bottom edge lands on it — never centred vertically on the slide (client rule
2026-08-06). `cards.add_card_row` does this by default: pass only `h_px` (the
card height) and omit `y_px`. For the `components.py` card builders (which take
an explicit `y_px`), bottom-anchor with `y_px=components.bottom_anchor(h_px)`
(= `GRID_BOTTOM_PX - h_px`). Give the card a height and let its bottom fall on
the grid line; do not center it.

## R28 — A person's role is Graphite

In a bio/person card, the job title under the name (e.g. "Chief growth
officer") is **Graphite** #454E63, not the muted Gray-Dark (client rule
2026-08-06). `components.add_bio_card` does this.

## R29 — Title → subhead gap is 20px

The subhead sits **20px** below the slide title (visual gap, glyph bottom to
glyph top — client rule 2026-08-06). `components.add_subhead` computes this from
the title's y and size; if the title wraps, pass `title_lines`. Do not hand-place
the subhead.

## R30 — Subhead is 12pt

The slide subhead is always **12pt (24px)**, Gray-Dark (client rule 2026-08-06).
Built by `components.add_subhead`.

## R31 — Balanced paragraphs, no widows/orphans, no short word at a line end

Every body paragraph AND every subhead is line-balanced (client rule
2026-08-06): even line lengths — never "one long line, then a two-word line".
No widow/orphan. **No article or 1-2 letter word (a, an, the, of, to, in, is …)
sits at the end of a line** — it is glued to the following word with a
non-breaking space and wraps with it. Always run paragraph/subhead text through
`textbalance.balance_lines(text, width_px, size_px)` (card bodies, subheads, and
the components already do; free `add_text` paragraphs MUST too).

## R32 — En-dash only, never the em-dash

All copy the skill writes uses the **en-dash (–)**, never the em-dash (—) —
titles, headings, subheads, body, everything (client rule 2026-08-06). The
engine enforces it: `primitives.add_text` converts every em-dash to an en-dash
on the way in, and `balance_lines` normalizes too.

## R33 — Titles obey the line-end rule too

The short-word rule (R31) applies to **titles**, not just body: a 1-letter
article ("a") or a 1-2 letter preposition ("of", "to", "in", "on"…) never sits
at the END of a title line — it moves to the next line with its word (client
rule 2026-08-06). The engine glues short words (NBSP) on every run, so a title
that SOFT-WRAPS in its box is handled automatically. For a title you HAND-BREAK
with `\n`, put the break so the short word starts the next line (e.g.
`"From snapshot\nto shippable asset"`, never `"From snapshot to\nshippable"`).
For a monotone multi-line statement, run it through
`textbalance.balance_lines(text, width, size)` and it balances + glues for you.
Two-tone titles glue within a run but not across the color split — hand-break
those.

## R34 — Text rests ON the bottom grid line

A bottom-anchored text block **rests on the grid line** (y=993.5): the last
line's LOWEST point — the descender bottom of g/p/y — sits on the line, so the
block stands on it and NOTHING crosses below (client choice 2026-08-06).
`components.add_paragraph_group` does this (Arial descender ≈ 1.15·size below a
line box top, pixel-measured). The chart data table is bottom-anchored so it
never runs past the line either.

## R35 — Titles snap to the top grid line, identically on every slide

Every slide title's **cap-top sits on the top margin grid line** (y=50) and its
left edge on the left margin (x=50) — the capitals start exactly on the corner
of the grid, in the SAME position on every slide, never floating or wandering
(client rule 2026-08-06). Place titles with `components.add_title(slide, content)`
(not a raw `add_text`); it returns the line count for `add_subhead(title_lines=…)`.

**Why titles "wandered" (root cause, fixed 2026-08-06).** With exact `spcPts`
line spacing, PowerPoint's first-line position drifts two ways, so the naive
"box top = 50 − 0.0625·size" landed the caps anywhere from y46 to y50 depending
on the slide:
  1. the cap-top sits `0.0388·size + 1.27` px below the box top — this GROWS with
     size, so 0.0625·size was right at 64px but ~3px off at 110px (the cover
     floated high);
  2. a MULTI-line title lifts its own first line ~2px higher than a one-liner of
     the same size — so a wrapping title sat higher than a single-line one, the
     per-slide wander.
`add_title` now offsets the box by a lead calibrated on BOTH size and line count
(`_title_box_top`, pixel-measured via fitz baselines across 36–110px), landing
every title's caps within <1px of y=50 regardless of size or wrapping. This
includes DARK section statements (`add_section_statement`, they ARE the title)
and the 110px cover/closing heading (`add_gradient_cover`).

## R37 — A two-tone accent phrase never splits with a word hanging

When two or more consecutive words are in the accent colour (High), they are ONE
phrase and must not break across lines leaving a single accent word at a line end
while the rest wraps (client rule 2026-08-06). The whole accent phrase moves to
the next line together. The engine enforces it: `primitives.add_text` glues every
word of a two-tone heading's accent (High) run with non-breaking spaces, so the
accent phrase wraps as a unit. Keep accent runs short (1–3 words).

## R36 — Text boxes hug their content

Text boxes are SET to the measured text bbox, like Figma HUG — a selected box is
snug, with no dead space around the copy (client rule 2026-08-06). Unlike
PowerPoint auto-fit (which trims only height, and only once the text is edited),
`primitives.add_text` measures the text up front — **width = the longest rendered
line, height = line count × pitch** — and creates the box at that size, so it is
tight the moment the deck opens and there is no first-line "sag". On by default
(`hug=True`) for top-anchored boxes, including titles (`add_title`). Width hugs
only for LEFT-aligned text (shrinking a centre/right box would move the copy);
height always hugs. The rendered text is unchanged — only the box bounds tighten.

## R14 — A chart never ships without its data table

Template 14's supporting data table under the chart is a REQUIRED part of
the layout, not an optional extra (client rule 2026-07-23). Never emit the
bar chart alone: if no separate table data is provided, derive the rows
from the chart's own values.

**The data table's row underline is SEGMENTED to the bars** (client rule
2026-08-06): each row's underline breaks into one segment under every bar with
a gap over each inter-bar gutter — never one continuous full-width rule. Build
it with `components.add_chart_data_table(slide, y_px, rows, n, start_col=…)`
passing the SAME geometry args used for `composites.bar_chart_geometry`, so the
segments line up exactly under the bars. Do NOT hand-roll the table with a plain
continuous-underline helper for a chart slide — that is the regression this rule
prevents.

## R38 — Cover and closing: gradient, 110px title, date + quarter pills

The **cover and the closing (last) slide** share one design (client rule
2026-08-06, Figma nodes 670-1022 / 670-1017 / 670-1025). Build both with
`components.add_gradient_cover(slide, title, date=…, quarter=…)`:

* **Background** — a vertical Navy → brighter-blue gradient (`COVER_GRADIENT`),
  not the old Graphite ramp.
* **Title** — 110px (= 55pt), two-tone (High accent + Gray-Dark muted). Its
  cap-top snaps ONTO the top grid line (y=50) like every title (R35), and the
  box hugs the text (R36). It carries **Condensed 1.5pt** letter spacing
  (absolute, `COVER_TRACK_PT`), not the −1% used elsewhere.
* **Bottom-left pills** — the date + quarter element (Figma node 670-1017): two
  adjacent, fully-rounded, **1px-outlined, UNFILLED** chips — BOTH the text and
  the outline are High accent blue (client rule 2026-08-06). The wide chip is
  the creation date (`2026.11.12`, dots not slashes), the narrow one the quarter
  (`Q4`). `primitives.add_pill`.
* **Bottom-right arrow — COVER ONLY** — a circular "next" button (Figma node
  670-1025): an UNFILLED circle outline + a right-arrow, both High, drawn as
  NATIVE flat shapes (`primitives.add_arrow_button`), never an imported
  SVG/raster. It's a "start viewing" affordance, so it belongs on the FRONT
  cover only; the CLOSING (back) cover passes `arrow=False` (client rule
  2026-08-06).
* **Closing phrase — always two lines** — the back cover's statement is forced
  onto two balanced lines: `add_gradient_cover(..., arrow=False, lines=2)`
  (client rule 2026-08-06).

The pills and the arrow circle are the ONLY sanctioned rounded outlines; being
unfilled they are not badges, and every filled shape still stays sharp (R12). No
footer caption on these slides — the pills replace it.

**Simple vector marks (a logo, an arrow, a geometric icon) are drawn as native
PowerPoint shapes** — ovals, connectors, freeforms, all theme-colored and flat —
never imported as an SVG file or raster. Reserve an embedded SVG only for a
genuinely complex illustration that is not worth rebuilding from shapes.

## R39 — Section (divider) slides are two-tone on navy

A section / divider ("перебивочный") slide is a big claim on a **dark navy
background with TWO text colours — white base + High accent** (client rule
2026-08-06), exactly like every other slide's two-tone title. Not all-white any
more. Build it with `components.add_section_statement(slide, [(text, WHITE_COOL),
(accent, HIGH), …])`; the statement is that slide's title, so it snaps to the
top grid line (R35) and is line-balanced (R31). A plain string renders all-white.

## R40 — A monotone title defaults to Graphite

A one-colour slide title (a plain string, e.g. "Agenda") renders in **Graphite**
— the same dark tone as the base of every two-tone title (client fix
2026-08-06). `components.add_title` applies this automatically, so a monotone
title never falls back to the theme default and never looks darker than the
titles on neighbouring slides.

## R41 — Top-right brand mark: logo or company name

Every deck carries a brand mark in the **top-right corner** of **every slide** —
cover, content, section dividers, AND the closing (Figma node 674-1100, client
rule 2026-08-06). Ask for it at the START, right after the content question
(SKILL Step 0b), then place it with `components.add_logo`:
  * **User has a logo** → their image, fit within a **143.5×38** zone (half the
    original Figma 287×76 — client rule 2026-08-07; a logo stands 38px = 19pt
    tall), RIGHT+TOP aligned to the grid corner (right edge x=1870, top y=50):
    `add_logo(slide, image_path=…)`. This is the ONE sanctioned raster in a deck
    — a brand asset, not a content image. Accepted formats (python-pptx): **PNG,
    JPG, GIF, BMP, TIFF** — recommend PNG. **SVG and WEBP are NOT supported** —
    convert to PNG first. The upload popup (SKILL Step 0b) shows the accepted
    formats + recommendation, but must NOT mention transparency/other jargon.
  * **No logo (or it wasn't supplied)** → the **company name** as a text
    wordmark at **10pt (= 20px)**, right-aligned to the right margin with its
    cap-top on the top grid line: `add_logo(slide, name=…)`.

On DARK slides (cover / closing gradient, navy sections) the mark must be light,
so pass `dark=True` (name → White-Cool). This is built into the dark builders:
`add_gradient_cover(…, logo_name=…/logo_image=…)` and `add_section_statement(…,
logo_name=…/logo_image=…)` draw it in `dark=True` for you — so pass the brand
mark to THOSE too, not only to the white content slides. A full-height image
(col 6/7 to the right margin) may cover the mark — that is fine, don't move it.
The mark sits opposite the title (title is top-LEFT), so they never collide.
(Note: for the NAME case, if a cover/closing title already IS the company name,
the top-right name repeats it — use a tagline title there, or omit the mark on
that one slide.)

## R42 — Data table that is NOT full width: table + side text

A data table need not span the full width. The narrow variant (Figma node
674-1028, client rule 2026-08-06) is an **8-column data table** beside a
**3-column text block** (H3 heading + Body), with **one empty grid column**
between them — 3 + 1 + 8 = 12. Build it with
`components.add_side_table(slide, headers, rows, heading, body, side="left")`:
`side="left"` puts the text on the left (cols 0–2) and the table on the right
(cols 4–11); `side="right"` flips them (table cols 0–7, text cols 9–11). Both
bottom-anchor to the grid line so their bottoms align. The table itself is the
native template-15 object (`add_data_table`, placeable at any columns): a header
row (1.5pt underline) over data rows (0.5pt), Gray-Dark rules, cells vertically
centered, no verticals or fills.

## R43 — Delivered file carries only the master + Blank layout

The saved `.pptx` ships with ONE slide master (its theme and fonts) and ONLY the
**Blank** slide layout that every slide is built on — the ~10 unused default
layouts (Title Slide, Two Content, Comparison, …) are stripped, so the
PowerPoint Slide Master view is clean (client rule 2026-08-07). `Deck.save()`
does this automatically; a layout in use by a slide is never removed, and
the master's title/body (theme fonts) stay. The delivered file is also
de-chromed: the **footer band** (date, footer, slide-number placeholders) is
removed from the master, and the Blank layout is stripped of EVERY
placeholder so it is genuinely blank — slides draw their own footer as plain
text boxes, so nothing on a slide is lost. Opt out with `Deck(strip_layouts=False)`.
