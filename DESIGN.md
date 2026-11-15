---
name: Dr. Sepideh Safanavaei
description: A Persian, right-to-left physician's site woven like a Mazandarani chadorshab, in deep teal cloth with saffron-gold and madder-red threads.
colors:
  field: "#0C3438"
  field-2: "#165257"
  gold: "#D4A84E"
  madder: "#A23B2C"
  sea: "#E3ECE6"
  ivory: "#F7F2E7"
  ink: "#0C3438"
  ink-2: "#3B5A5C"
  ivory-2: "#C9D6D1"
typography:
  display:
    fontFamily: "Lalezar, Vazirmatn, system-ui, sans-serif"
    fontSize: "clamp(2.625rem, 1.4rem + 5.6vw, 6.5rem)"
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: "0"
  headline:
    fontFamily: "Lalezar, Vazirmatn, system-ui, sans-serif"
    fontSize: "clamp(2.125rem, 1.5rem + 2.8vw, 4rem)"
    fontWeight: 400
    lineHeight: 1.3
    letterSpacing: "0"
  tagline:
    fontFamily: "Lalezar, Vazirmatn, system-ui, sans-serif"
    fontSize: "clamp(1.5rem, 1.2rem + 1.4vw, 2.375rem)"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0"
  title:
    fontFamily: "Lalezar, Vazirmatn, system-ui, sans-serif"
    fontSize: "clamp(1.375rem, 1.25rem + 0.6vw, 1.75rem)"
    fontWeight: 400
    lineHeight: 1.35
    letterSpacing: "0"
  lede:
    fontFamily: "Vazirmatn, system-ui, -apple-system, Segoe UI, Tahoma, sans-serif"
    fontSize: "clamp(1.1875rem, 1.1rem + 0.45vw, 1.375rem)"
    fontWeight: 400
    lineHeight: 1.9
    letterSpacing: "0"
  body:
    fontFamily: "Vazirmatn, system-ui, -apple-system, Segoe UI, Tahoma, sans-serif"
    fontSize: "clamp(1.125rem, 1.08rem + 0.2vw, 1.1875rem)"
    fontWeight: 400
    lineHeight: 1.9
    letterSpacing: "0"
  label:
    fontFamily: "Vazirmatn, system-ui, -apple-system, Segoe UI, Tahoma, sans-serif"
    fontSize: "1rem"
    fontWeight: 500
    lineHeight: 1.7
    letterSpacing: "0"
  button:
    fontFamily: "Vazirmatn, system-ui, -apple-system, Segoe UI, Tahoma, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0"
rounded:
  square: "0"
  focus: "4px"
  pill: "999px"
spacing:
  thread: "8px"
  s-1: "8px"
  s-2: "16px"
  s-3: "24px"
  s-4: "32px"
  s-5: "40px"
  s-6: "48px"
  s-8: "64px"
  s-10: "80px"
  s-12: "96px"
  s-15: "120px"
  margin: "clamp(20px, 4vw, 64px)"
  measure: "38em"
  wrap: "1312px"
  tap: "48px"
components:
  pill-gold:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.field}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: "10px 24px"
    height: "48px"
  pill-gold-hover:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.field}"
  pill-field:
    backgroundColor: "{colors.field}"
    textColor: "{colors.ivory}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: "10px 24px"
    height: "48px"
  pill-field-hover:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.field}"
  pill-line:
    backgroundColor: "transparent"
    textColor: "{colors.field}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: "10px 24px"
    height: "48px"
  pill-line-hover:
    backgroundColor: "{colors.field}"
    textColor: "{colors.ivory}"
  pill-line-on-field:
    backgroundColor: "transparent"
    textColor: "{colors.ivory}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: "10px 24px"
    height: "48px"
  pill-line-on-field-hover:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.field}"
  calltab:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.field}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: "12px 22px"
    height: "52px"
  calltab-hover:
    backgroundColor: "{colors.field}"
    textColor: "{colors.ivory}"
  flip-front:
    backgroundColor: "{colors.field}"
    textColor: "{colors.ivory}"
    rounded: "{rounded.square}"
    padding: "{spacing.s-3}"
  flip-back:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.field}"
    rounded: "{rounded.square}"
    padding: "{spacing.s-3}"
  fact-chip:
    backgroundColor: "{colors.field-2}"
    textColor: "{colors.ivory}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "10px 20px"
  fact-chip-gold:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.field}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "10px 20px"
  ribbon:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.ink}"
    rounded: "{rounded.square}"
    padding: "16px 24px"
  location-panel:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.ink}"
    rounded: "{rounded.square}"
    padding: "40px 32px"
  see-a-doctor:
    backgroundColor: "{colors.field}"
    textColor: "{colors.ivory}"
    rounded: "{rounded.square}"
    padding: "32px 32px 48px"
  text-field:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.square}"
    padding: "12px 16px"
    height: "56px"
---

# Design System: Dr. Sepideh Safanavaei

## Overview

**Creative North Star: "چادرشب" (the Amol weave)**

The site is woven like a chadorshab, the striped cloth of Mazandaran, re-dyed in the teal and gold of the doctor's own logo. Whole bands of flat colour carry the page: deep teal cloth for the header, the hero, the page heads, the procedures band and the footer; a pale Caspian-green ground for reading; ivory panels where something is filled in or looked up. Saffron-gold and madder-red appear as threads: in the striped selvedge at a seam, in the frame around the portrait, along the woven edge of a swatch. It belongs to Mazandaran, and through the logo's colours it belongs to her.

The surface is calm and legible before it is decorative. Text is Persian, right to left, set large (18 px body on a phone) with generous line height for an older reader. The pills are full-radius Parsley buttons with colour-only hovers. Everything else has the hard edges of cloth: square panels, square fields, flat swatches butted together. There is one 3D moment, the credential flip card, and one floating object with one shadow, the call tab. The phone is always one tap away, and the system never pushes.

There are no photographs yet, and none are faked. The imagery is the weave itself, the lungs mark traced from the logo, and a 4:5 woven portrait frame that makes the placeholder look intentional and a future photo look framed.

**Key Characteristics:**
- Flat colour fields with hard edges; stripes only at seams, never as a pattern.
- One measure: the 8 px thread.
- Lalezar for display at one weight, Vazirmatn for everything read.
- Full pills, colour-only hovers at 150 ms, a 0.97 press.
- One signature motion (the flip card) and one shadow (the call tab).
- RTL and Persian digits throughout; Latin isolated, `tel:` in ASCII.
- Layout survives 1 to N clinic locations without a layout change.

## Colors

Five threads of the cloth (two teals, saffron, madder, and two light grounds) plus two derived secondary inks.

### Primary
- **Deep Teal Cloth** (`field`): the cloth itself, used for the header, hero, page heads, procedures band, see-a-doctor panel, flip-card fronts and footer, and as the body ink on light ground (`ink` is the same value). Ivory on it is 12.0:1, `sea` under it 11.1:1.
- **Second Teal Thread** (`field-2`): portrait ground and placeholder, fact chips, the thin teal band in the woven edges, years in ribbons and the bio margin, and icons on light ground. Ivory on it is 7.9:1; on ivory it is 7.9:1 and on sea 7.3:1.

### Secondary
- **Saffron Thread** (`gold`): the primary button on teal, the call tab, years and counts on teal, flip-card backs, the medical council chip, the outer band of the portrait frame, the current nav item's underline, the focus ring on teal, and text selection. Gold on field is 6.1:1, and field on gold is also 6.1:1.

### Tertiary
- **Madder Thread** (`madder`): the stripe in the selvedge and woven edges, the red band of the portrait frame, the focus ring on light ground, and the error state (invalid field border, field error text, error-summary links, captcha status). Madder on ivory is 5.9:1 and on sea 5.4:1.

### Neutral
- **Pale Caspian Green** (`sea`): the page ground. Deliberately not cream.
- **Ivory** (`ivory`): text on teal, and the ground of ribbons, location and contact panels, form fields and the founder caption.
- **Teal Ink** (`ink`): body text on light ground, 11.1:1 on sea and 12.0:1 on ivory.
- **Muted Teal Ink** (`ink-2`): secondary text on light ground (hints, captions, hours, labels in a definition list), 6.2:1 on sea and 6.7:1 on ivory. Also the resting border of a form field.
- **Faded Ivory** (`ivory-2`): secondary text on teal (ledes, labels, crumbs), 9.0:1 on field and 5.9:1 on field-2.
- Hairlines on teal are ivory at 14–18% alpha; on light ground, teal at 18–35% alpha (link underlines, the urgent-line rule). These are derived, not tokens.

### Named Rules
**The Madder Is a Thread Rule.** Madder is never a button, a panel or surface fill, a heading or ordinary text. It is a woven thread (the selvedge, the woven edges, the portrait frame), a focus ring on light ground, or the error state. Madder on teal is 2.0:1, so it is never used as a foreground on `field`. (The direction said "stripes and focus ring only"; the build added the error state, which reads at 5.4–5.9:1.)

**The Gold Belongs to the Cloth Rule.** Gold is never text, an icon, a hairline or a focus ring on `sea` or `ivory`: it measures 1.8:1 and 2.0:1 there. On light ground gold appears only as a fill carrying teal text (the call tab, a teal pill's hover, the flip-card back, the sent check, the skip link) or as a woven thread (the selvedge, the head of `--weave-head`).

**The Focus Follows the Ground Rule.** The focus ring is a 3 px madder outline, offset 3 px, on light ground, and it switches to gold on any teal surface.

## Typography

**Display Font:** Lalezar (one weight, 400), falling back to Vazirmatn
**Body Font:** Vazirmatn 400 / 500 / 700, falling back to system-ui, Segoe UI and Tahoma

**Character:** Lalezar is a heavy Persian poster face drawn for Persian first, with real Persian digits. It gives the names, headings and years their weight. Vazirmatn is the quiet, highly legible reader at 18 px and up. Both are self-hosted WOFF2 files, subset to Persian, Basic Latin and punctuation (about 122 KB in total). No foreign CDN is used.

### Hierarchy
- **Display** (Lalezar 400, 42→104 px fluid, 1.2): the page `h1`, which is the doctor's name on Home and About and the page title elsewhere. Long condition titles take one smaller step (38→80 px).
- **Headline** (Lalezar 400, 34→64 px, 1.3): section `h2`s, the single location's name, and the gold error code on error pages.
- **Tagline** (Lalezar 400, 24→38 px, 1.5, gold on teal): the doctor's tagline under her name.
- **Title** (Lalezar 400, 22→28 px, 1.35): condition threads, procedure titles, clinic and location names, and panel `h2`s. Fixed display sizes for years: flip card 56 px (40 px on a phone), bio margin 36 px, procedure number 28 px, ribbon year 24 px.
- **Lede** (Vazirmatn 400, 19→22 px, 1.9, max 38em): the opening sentence of a section or a condition overview.
- **Body** (Vazirmatn 400, 18→19 px, 1.9, max 38em): all running text, and form input text (18 px or more, so iOS never zooms).
- **Label** (Vazirmatn 500, 16 px): definition-list terms, chip text, footer headings, the "on this page" title. 16 px is the floor.
- **Button** (Vazirmatn 700, 17 px; 18 px for full-width phone calls and the send button; 19 px for phone numbers in pills): pills and the call tab. Phone numbers set as links are 24 px at 700, and 26→34 px on the contact page.

### Named Rules
**The One Weight Rule.** Lalezar is used only for display and never for running text. It has one weight, so hierarchy comes from size and colour alone, never from faux bold.

**The Latin Fallback Rule.** Lalezar has no Latin glyphs. Every Latin run inside display type is wrapped in `bdi` and set in Vazirmatn 700 so its weight stays close to Lalezar's. One shared rule covers every display component; a new display component joins that list.

**The 18 px Phone Floor Rule.** On a phone (600 px and below), anything an older reader acts on (addresses, hours, the emergency line, field hints, the captcha alternative, condition descriptions) is at least body size. 16 px remains only for labels.

**The No Tracking Rule.** Persian is never letter-spaced. It is a joined script, and tracking breaks the joins. The only tracked text in the build is the Latin captcha answer (0.15em).

### Persian, RTL and digits
- The document is `lang="fa" dir="rtl"`. Layout uses logical properties throughout; physical `left`/`right` appear only where the safe-area insets are physical (the phone call tab).
- **Digits.** Displayed numbers are Persian digits through the `fa_digits` filter, never typed by hand. Phone numbers go through `phone_display`, which groups them as they are read aloud (۰۱۱-۴۴۲۲۹۲۷۰, ۰۹۱۱ ۹۹۷ ۰۸۲۸). `tel:` links keep ASCII digits in international form (`tel_href` → `tel:+98…`).
- **Latin.** Any text an editor types goes through `isolate_latin`. It wraps each Latin run (COPD, ERS, «COVID-19») in `bdi`, and it now also writes every digit outside a Latin run in Persian, so a house number or a year in a title needs no second filter.
- **Numbers that must not reorder** (phones, the council number, years in chips) are set with tabular figures, no wrapping, and an isolated LTR direction. Two Persian-digit runs are never joined by a separator in one inline run (bidi reorders them); they become separate chips.
- Forward arrows point left (forward in RTL). The flip card turns the mirrored way, `rotateY(-180deg)`.

## Layout

**The thread.** Every gap, band and stripe is a multiple of the 8 px thread (`s-1`…`s-15`, 8→120 px). Inside controls and stripes the build also uses the 4 px half-thread, 2 px butted gaps between swatches, and 6/10/12 px control paddings. These are local values, not scale steps.

**Container.** Content sits in a wrap of up to 1312 px plus fluid side margins (20→64 px), padded by the safe-area insets in landscape on a notched phone. Reading columns are capped at 38em. Editor-typed text (addresses, names, descriptions) may break anywhere, so a pasted link never pushes the page sideways; a Latin term in a heading never breaks.

**Grid.** Two-column compositions use unequal fractions (5/7, 4/8, 7/5, 1.35/0.65), never equal halves for text and media. Sections on the pale ground open with 120 px above and 96 px below. A section that follows another tightens to 32 px above. On phones these become 80/64 px.

**Breakpoints.** 1100 px: credentials go from 4 columns to 2. 960 px: the nav becomes a phone menu, all two-column grids stack, sticky sides become static, and the call tab becomes a full-width bar. 700 px: a single location panel stacks. 600 px: call pills go full width at 56 px, and the 18 px phone floor applies. 480 px: the header's degrees line hides (it also hides between 961 and 1100 px, where the nav leaves the lockup too narrow; nav labels never wrap). Phone layouts are their own decisions (the hero puts a small framed portrait above the name), not a shrink.

**Tap targets.** The minimum is 48 px (`tap`). Footer and inline phone links are 44 px, and full-width phone calls and the send button are 56 px.

### 1 to N clinic locations
The layout takes one, two or more clinic locations from the admin, with no template or layout change.
- **One location** is a single wide composition: in the footer, a two-column clinic (name and address beside the phones and hours); on the locations page, one ivory panel with the name at headline size and the facts split off by a 2 px teal rule. It never appears as a lonely card.
- **Two or more** become equal columns: `auto-fit` with a minimum of 240 px in the footer, 340 px on the locations page and 15rem in the stacked contact list. The footer grid rebalances from 4/8 to 3/9.
- Labels that name the clinics switch between «مطب» and «مطب‌ها» through the shared `clinic_word`, never by a hand-written condition.
- The primary location (the first) feeds the hero call, the call tab and the see-a-doctor panel. Every location appears in the hero's where line, the call band, the footer and the contact page.
- With zero locations, call blocks disappear and the contact form takes a single 46rem column.

## Elevation & Depth

The system is flat. Depth comes from tonal fields (teal cloth against the pale ground, an ivory panel on the ground) and from hard-edged bands, never from shadow, blur or glow.

### Shadow Vocabulary
- **Float** (`box-shadow: 0 8px 24px rgb(12 52 56 / 0.28)`): the floating call tab only, because it is the one thing that floats.

### Named Rules
**The One Shadow Rule.** Only the call tab casts a shadow. Panels, cards, pills and fields are flat at rest and on hover. Hover changes colour, never elevation.

## Shapes

Cloth has hard edges. Panels, swatches, chips, ribbons, flip cards, the portrait frame and form fields are all square (`square`, 0). The only round forms are the pills, the call tab, the skip link and the round icon buttons (`pill`, 999 px). The focus outline takes a 4 px corner, except on square fields, where it stays square.

**The weave.** The woven edge is drawn as hard-stopped threads with no blend between them, using exactly two tokens:
- `--weave-foot` sits at the foot of a teal swatch (the flip-card front and the see-a-doctor panel): field-2 6 px, madder 3 px, gold 6 px, then the field.
- `--weave-head` sits at the head of an ivory panel (location panels and the contact form): gold 8 px, madder 4 px, field-2 8 px, then ivory.

**The selvedge** is the full-width seam between the teal cloth and the pale page, a 72 px stack of seven threads: gold 16, field 8, madder 4, ivory 8, field-2 24, gold 8, field 4. It follows every page's teal opening band and tops the footer.

**The portrait frame** is concentric bands: gold 12 px, madder 4 px, ivory 8 px, then the 4:5 portrait (6/2/4 px on the phone hero).

### Named Rules
**The Seams Only Rule.** Stripes appear only at seams (the selvedge), on the portrait frame and on the edges of swatches and panels. They never appear as a background pattern or texture. Overused, the weave tips into folklore: a handicraft shop, not a physician.

**The Two Edges Rule.** A woven edge is `background: var(--weave-foot)` or `var(--weave-head)`, never a new gradient. Hard stops only; no blended gradient anywhere. (The direction said "no gradients"; the build draws the weave as hard-stop gradients, which keeps the intent.)

## Components

### Buttons (pills)
Parsley's full pills: quiet, and generous to the thumb.
- **Shape:** full radius (999 px), at least 48 px tall, 10×24 px padding, a 2 px border, Vazirmatn 700, with an 18 px leading icon when one is used. A small variant is 44 px tall at 16 px.
- **Gold** (the primary on teal): gold with teal text; hover turns ivory.
- **Teal** (the primary on light ground): teal with ivory text; hover turns gold with teal text, which is Shafer's invert done in colour.
- **Line** (secondary): a transparent teal outline that fills teal on hover. On teal the outline is gold with ivory text, and it fills gold on hover.
- **Hover:** colour only, 150 ms, `cubic-bezier(.2,.8,.2,1)`, and only for fine pointers. A hover is a full swap, never a tint.
- **Press:** `scale: 0.97` over 160 ms. This uses the separate `scale` property so it never fights a transform. It does not apply while the send button is busy, and it does not apply under reduced motion.
- **Busy:** the send button is `aria-disabled`, 0.7 opacity, labelled «در حال فرستادن…», and refuses a second press.
- **On a phone:** call pills go full width at 56 px and 18 px text.
- **Round icon buttons** (menu, phone call in the header) are 48 px circles. The gold variant has a teal 20 px icon.

### Fact chips
Flat swatches butted together with a 2 px gap: field-2 with ivory 500 text, and the medical council number in gold with teal text. Each chip appears only when its field is entered. Years of experience and "practising since" are separate chips.

### Credential flip cards (signature)
A swatch of cloth turned over to its reverse. This is the system's one signature motion. Only credentials with an institution flip; the rest are ribbons.
- **Front:** teal cloth with `--weave-foot`, a gold turn cue in the corner, the year in gold Lalezar (56 px) and the title in ivory Vazirmatn 700.
- **Back:** the gold reverse, with «محل:», the institution in teal Lalezar and an optional detail line.
- **Proportion:** each card is an inline-size container. 5:4 is a minimum height (4:5 on a phone), so long text grows the card and its row instead of overflowing. (The direction said fixed proportions; the build treats them as a minimum.) There are 4 columns, 2 below 1100 px, and an 8 px gap on a phone.
- **Motion:** `rotateY(-180deg)` with 1100 px perspective, in over 560 ms and back over 380 ms, `cubic-bezier(.2,.8,.2,1)`. It is a CSS transition, so it can be interrupted.
- **Triggers:** hover (fine pointers only), keyboard focus, and tap or Enter/Space through `aria-pressed`. Escape and blur turn the card back. A mouse click does not toggle, because hover already turned it.
- **Reduced motion:** no turn. The gold back crossfades over the front in 200 ms.
- It is a `button` with both faces in the DOM, so screen readers read the title, year and institution.

### Ribbons
Static credential rows (memberships, publications) in two columns butted with 2 px gaps: an ivory ground, a 72 px year margin in field-2 Lalezar, a 500-weight title and a muted 16 px detail line. One column on tablet and below.

### Named threads (conditions list)
A two-column list (one column below 960 px). Each row has a 2 px teal top rule, the title at title size in Lalezar, a muted description, and a field-2 forward arrow. Hover and press underline the title (2 px, 0.3em offset). The rows do not move.

### Numbered procedures
A list on the teal cloth: a gold Lalezar number, the title at title size, an optional faded-ivory description, and a gold arrow. Rows are at least 72 px, separated by ivory hairlines at 18%. Hover turns the row gold.

### Call band
Closes Home and About. It has a 2 px teal top rule and a 5/7 grid: the heading on one side; on the other, every clinic location's name at title size, its phones as pills (19 px numbers), its hours in muted ink, then text links to locations and contact.

### Call tab
Shafer's floating tab, rebuilt: a gold pill with a phone icon and «تماس با مطب», fixed at the end-bottom corner, carrying the one shadow.
- It is hidden while any element marked as a call anchor (the header phone, the hero call, the see-a-doctor phone, the contact page's first number) is on screen. It rises 16 px in over 260 ms and fades out over 200 ms.
- It starts hidden in the markup, so it never flashes on load; without JS it is always shown.
- It steps aside while a form field has focus.
- On a phone it is a full-width bar, 56 px tall, 12 px from each edge and the safe area.
- Hover turns it teal with ivory text, and its focus ring is madder.

### See-a-doctor panel
Mayo's "when to see a doctor", leading straight to the phone. It is a teal swatch with `--weave-foot`. The emergency line comes first, at body size, with a gold `tel:115`, separated by a hairline. Then a line of guidance, the primary location's phones (a gold pill and a line pill), its name and hours, and text links. It sits sticky beside a condition body, or after the body when the body has an index.

### Location panels
Ivory panels topped by `--weave-head`. The name is in Lalezar. The address is lede-size at 500 weight. Route and copy-address pills follow. Phones are 24 px at 700, with a field-2 icon, and underline on hover. Hours are at 500.
- The copy button appears only where the clipboard API works. It confirms in place («نشانی کپی شد», with a check that settles in over 180 ms) and in a live region, and says «کپی نشد» if the copy is refused.
- For one location versus several, see Layout.

### Inputs / Fields
- **Style:** square, 56 px tall (9rem for a textarea, which resizes vertically), 12×16 px padding, a 2 px `ink-2` border, an ivory ground and body-size text. Labels are 700 above the field. «(اختیاری)» is 400 and muted. Hints are 16 px muted (18 px on a phone).
- **Hover / Focus:** the border turns teal. On focus the madder outline sits 2 px off a square corner.
- **Phone input:** typed LTR with `inputmode="tel"`, but right-aligned with the Persian labels.
- **Error:** the field border turns madder, and a 700-weight madder message with an alert icon sits between the hint and the field. The field gets `aria-invalid` and `aria-describedby` (hint and error). The form is `novalidate`, so the browser's own bubbles never show.
- **Error summary:** at the top of the form, framed in 2 px madder (never a side stripe), focused on load, with a bold «فرم فرستاده نشد.» and a list of madder links to each invalid field.
- **Sent state:** replaces the form in place and takes focus. A 56 px gold check square settles in (from 0.9 scale and transparent, 280 ms after 80 ms; a 200 ms fade under reduced motion), followed by the confirmation and the phone.
- **Captcha:** the server-drawn image (200 px wide, multiplied onto the panel so its white ground disappears) sits beside a 44 px round outline refresh button that fills teal on hover. The refresh swaps the image in place and is `aria-disabled` while loading. A madder status line announces failures. The answer box matches the image width and is centred, with the Latin letters tracked at 0.15em. A phone-number alternative sits below for anyone who cannot read the image.
- **Honeypot:** moved off-screen, never `display: none`.

### Navigation
- **Header:** on the teal cloth, 88 px tall (72 px on a phone). The lockup has the ivory lungs mark (44 px; 36 px on a phone), the name at 700 and the degrees line. Nav links are 500 weight with a 2 px underline that goes gold on hover and stays gold for the current page. The clinic phone is a line pill at the end.
- **Phone menu (below 960 px):** a disclosure panel under the bar on the same cloth, not an overlay, with a 4 px gold thread at its foot. Links are 60 px rows in Lalezar 24 px with ivory hairlines, and the current page is gold. It slides 8 px and fades in over 220 ms, with a 150 ms fade under reduced motion. Escape closes it and returns focus. Without JS it is simply open.
- **Page head:** each inner page opens with a teal band holding the `h1`, a lede and, on the conditions list, jump pills with gold counts. Condition pages add crumbs above the title (faded ivory, with ivory links underlined at 45%). The selvedge follows the band.
- **Footer:** on the cloth, with the selvedge on top. The brand side has a 56 px mark, the name in Lalezar and the degrees; then the clinics (see Layout); then an end row of links with gold current-page underlines.
- **Text links:** 700 weight, 48 px tall, a 1 px underline at 35% teal (45% ivory on teal) that becomes solid on hover or press, and a forward arrow after the text.

### Motion summary
- Flat and exact, like cloth.
- Hovers change colour in 150 ms. Press is `scale 0.97` over 160 ms. The menu takes 220 ms and the call tab 260 ms.
- The flip card (560/380 ms) is the one signature.
- All easing is `cubic-bezier(.2,.8,.2,1)`. Only transform, scale and opacity animate.
- There are no scroll-in entrances, no smooth scrolling and no hover nudges.
- Every motion has a reduced-motion alternative: no movement, with the state still changing instantly or by crossfade.

## Do's and Don'ts

### Do:
- **Do** build every gap, band and stripe from the 8 px thread (or its 4 px half inside a stripe).
- **Do** open every page with a teal cloth band and follow it with the selvedge seam.
- **Do** draw a woven edge with `--weave-foot` (the foot of a teal swatch) or `--weave-head` (the head of an ivory panel).
- **Do** use the gold pill as the primary on teal and the teal pill as the primary on light ground; give secondaries the line pill.
- **Do** switch the focus ring to gold on teal; keep it madder on light ground.
- **Do** run every displayed number through `fa_digits` or `phone_display`, every editor-typed string through `isolate_latin`, and every `tel:` link through `tel_href` (ASCII).
- **Do** wrap Latin inside display type in `bdi` and set it in Vazirmatn 700.
- **Do** keep act-on text at 18 px or more on phones, and tap targets at 48 px (56 px for a full-width call).
- **Do** design every location block for 1, 2 and 3+ locations: one wide composition, or equal columns.
- **Do** gate every hover with `(hover: hover) and (pointer: fine)` and give every motion a reduced-motion alternative.
- **Do** let a real photo drop into the 4:5 woven frame (`object-fit: cover`, focused at 22% from the top); until then, show the gold lungs on field-2.

### Don't:
- **Don't** use stripes as a background pattern or texture. They belong at seams, on the portrait frame and on swatch edges only.
- **Don't** use madder for a button, a panel fill, a heading or ordinary text, or as a foreground on teal.
- **Don't** put gold text, icons, hairlines or focus rings on `sea` or `ivory` (1.8:1 and 2.0:1).
- **Don't** set running text in Lalezar, or fake a bold for it.
- **Don't** letter-space Persian.
- **Don't** add shadows, glows, blur or blended gradients. The call tab's float is the only shadow.
- **Don't** round a panel, card, chip or field. Only pills and round icon buttons are round.
- **Don't** add a second 3D or signature motion, scroll-in entrances or hover nudges. Hovers change colour only.
- **Don't** use stock photos of people, or any image presented as the doctor that is not her.
- **Don't** put a lone location in a small card, or hard-code «مطب» against «مطب‌ها».
