# Stage 2: Direction and mockups

Written on 2026-11-14 from `main` at `ae49b13`. Reads: [`00-inspection.md`](00-inspection.md), [`PRODUCT.md`](../../PRODUCT.md), [`references/README.md`](references/README.md).

**This stage ends at a gate.** Section 7 lists everything you need to decide. Nothing is built until you answer.

Contents:
1. [How the directions were made](#1-how-the-directions-were-made)
2. [Direction A: «چادرشب» (the Amol weave)](#2-direction-a-چادرشب-the-amol-weave)
3. [Direction B: «سربرگ» (the letterhead)](#3-direction-b-سربرگ-the-letterhead)
4. [Direction C: the category standard](#4-direction-c-the-category-standard)
5. [Recommendation](#5-recommendation)
6. [Page and section inventory](#6-page-and-section-inventory)
7. [For you to decide](#7-for-you-to-decide) (proposals and content questions)

Mockups: [`mockups/a.html`](mockups/a.html), [`mockups/b.html`](mockups/b.html), [`mockups/c.html`](mockups/c.html), and a type specimen [`mockups/specimen.html`](mockups/specimen.html). Screenshots are in [`mockups/screens/`](mockups/screens/).

To flip through them, serve the folder and use ← / → or the black bar at the bottom of the page:

```bash
python3 -m http.server 8731 --directory docs/design/mockups
```

Then open `http://127.0.0.1:8731/a.html`.

---

## 1. How the directions were made

- **Discovery** came from `PRODUCT.md` and the Stage 1 decisions (logo binding, formal third-person voice, pulmonology first). `impeccable shape` didn't need a new interview round: the brief already answers its questions.
- **The surface is "Persuade"** (impeccable's modes): the visitor must believe her credentials and then call.
- **Rut, named so we avoid it:**
  - the category default is clinical blue with a stethoscope and a stock doctor;
  - its predictable opposite is cream, a serif and terracotta, which is also what AI-generated sites converge on.
- **Seven candidate worlds** were taken from the audience's own world, in order of how strongly they resonate:
  1. the doctor's letterhead and prescription pad (سربرگ و نسخه),
  2. the wall of framed diplomas in an Iranian doctor's office,
  3. Nastaliq manuscript illumination (the logo's own lettering),
  4. Hyrcanian forest and Caspian air,
  5. the clinic signboard (تابلوی مطب),
  6. the bronchial tree drawn as a botanical plate (the literal "lungs" idea, allowed once),
  7. the Mazandarani **chadorshab** (چادرشب), the striped hand-woven cloth found in homes across the province.
- **impeccable's concept roll** (seed `seed:f14243bdf9bb95a4`) assigned **candidate 7**. It also dealt six challengers from its catalogue (a HyperCard stack, an oscilloscope, a Weimar cabaret bill, a Toyism plate, a curved-crease paper shell, a tensegrity column).
  - Each was fused with our facts and weighed against the chadorshab on two axes: whether an Amol patient recognises themself in it, and how clearly it states who she is and how to call.
  - **All six were declined.** What each one's discipline added to Direction A is listed under "Raised by" in section 2.
- **Direction B** is my own top candidate (impeccable's "pick"). **Direction C** is the category standard played straight: Parsley's structure in the logo's colours. It's here so you can see what the familiar route costs and gives.
- **taste-skill** dealt three ways of composing a page:
  - "split stage", which became Direction B's fixed letterhead;
  - "dressed as something else", which became Direction A's textile;
  - "the place carries it". This one needs photographs we don't have, so it was set aside.

Two departures from the skills' own procedure, said plainly:
- **The choice is made here, in this document.** impeccable would normally serve an interactive decision page and wait for your answer. Your staged workflow makes this document and the mockups the gate, so I used that instead.
- **The mockups load fonts from Google Fonts.** They are throwaway. The real build self-hosts subset woff2 files (Stage 3).

**Shared by all three directions** (it comes from the brief, not from the look):
- the founder card with her face, name and titles on the first screen;
- the clinic phone in the header;
- tap-to-call as the main action;
- the floating call tab;
- the credential flip card (its mechanics are in section 2.5).

---

## 2. Direction A: «چادرشب» (the Amol weave)

**Concept.** The site is woven like a chadorshab: deep teal cloth with saffron-gold and madder-red threads. Whole bands of colour carry the page, and the striped selvedge marks the seams. It belongs to Mazandaran, and through the logo's teal and gold it belongs to her.

**Draws on:**
- Parsley: richness from colour fields rather than photos, and full pills with quiet colour-only hovers;
- van Straten: the structure, and the flip card;
- Digestive Health UK: the founder card;
- Shafer: the floating tab.

**Screenshots:**
- [desktop hero](mockups/screens/a-1440-hero.png), [desktop full page](mockups/screens/a-1440.png)
- [phone hero](mockups/screens/a-390-hero.png), [phone full page](mockups/screens/a-390.png), [phone after scrolling, with the call tab](mockups/screens/a-390-scrolled.png)
- cards: [turned](mockups/screens/a-1440-flipped.png), [mid-turn](mockups/screens/a-1440-midturn.png), [reduced motion](mockups/screens/a-1440-reduced-motion.png)

### Type
- **Display: Lalezar.** A heavy Persian display face by Borna Izadpanah, drawn for Persian first, with poster weight and real Persian digits.
- **Text: Vazirmatn** (400/500/700). It has the best Persian digits and Latin of the open faces, and is the most legible at 18px for older readers.
- **Sample** ([specimen](mockups/screens/type-specimen.png)): «COPD و آسم · از ۱۳۷۸», and in text, «عضو انجمن علمی ریه اروپا (ERS) … تلفن مطب: ۰۱۱-۴۴۲۲۹۲۷۰».
- **Risk:** Lalezar has a single weight. Hierarchy has to come from size and colour, and it must never be used for running text.

### Palette (tokens)
| Token | Value | Role |
|---|---|---|
| `--field` | `#0C3438` | deep teal cloth: header, hero, card fronts, text ink |
| `--field-2` | `#165257` | second teal thread: portrait ground, fact chips |
| `--gold` | `#D4A84E` | saffron thread: primary button, years, card backs |
| `--madder` | `#A23B2C` | madder-red thread: **stripes and focus ring only**, never text or buttons |
| `--sea` | `#E3ECE6` | page ground, a pale Caspian green (deliberately not cream) |
| `--ivory` | `#F7F2E7` | text on teal |

A **thread unit** of 8px: every band, gap and stripe is a multiple of it.

### Imagery without photos
- **The weave itself**: flat colour bands, hard edges, no gradients.
- **The portrait frame**: concentric gold, red and ivory bands, like a woven border.
- **The lungs-and-airways drawing** from her logo, cut out of the raster for now (section 7.3).
- **A real portrait** drops into the 4:5 frame with `object-fit: cover`, focused on the upper third. The frame makes the placeholder look intentional and makes a real photo look framed.

### Motion character
- **Flat and exact**, like cloth.
- **Hover:** colour only, 150 ms.
- **The floating call tab** rises 16 px in when the hero's own call button scrolls out of view.
- **The flip card** is the one 3D moment:
  - front: a teal swatch with the year in gold Lalezar and the title in ivory, edged with a woven selvedge;
  - back: the gold reverse of the cloth, with the institution in teal.

### Home page sketch
1. **Header** on the teal cloth: lungs mark and name lockup at the start, four links, the clinic phone as an outline pill at the end.
2. **Hero** on the same cloth:
   - the name huge in Lalezar, the tagline in gold, one sentence of proof;
   - three "at a glance" chips: practising since, medical council number, ERS/ATS (each depends on section 7);
   - «تماس با مطب» in gold and «مسیر مطب آمل» in outline;
   - the location line.
   - Beside it, the founder card in its woven frame.
   - On a phone, the small framed portrait sits above the name.
3. **The selvedge stripe**, the seam between the cloth and the page.
4. **Credentials** on the pale ground:
   - the four with an institution as flip swatches;
   - the four memberships and publications as woven ribbon rows.
5. *(Stage 4 adds:)* the top conditions as a list of named threads, then the locations summary with the map link, then the footer on the cloth with the selvedge on top.

### Raised by the declined challengers
- **Raised by the oscilloscope:** one measure. Everything is measured against the 8px thread; no stray spacing.
- **Raised by the Weimar cabaret bill:** two states, no midtone. A card is either its front or its back (an exact colour swap), and a hover is a full swap, never a tint.
- **Raised by the Toyism plate:** a fixed palette with hard edges. No gradients, glows or blur anywhere; shadows only on the floating call tab, the one thing that actually floats.
- **Raised by the HyperCard stack:** fixed proportions. Credential swatches keep their aspect ratio and never stretch to fill a row.
- **Raised by the tensegrity column:** every fact is pinned to its source. Each credential carries its year as its pin, and the back says where it was earned.
- **Raised by the curved-crease shell:** nothing kept.

### Honest risk
- **Overused, the stripes tip into folklore** (a handicraft shop, not a physician). The rule that prevents it: the weave appears only at seams, on the portrait frame and on card edges, never as a background pattern.
- **Some will read chadorshab as rural.** I think the teal-and-gold re-dyeing keeps it dignified, but you know the audience better.

---

## 3. Direction B: «سربرگ» (the letterhead)

**Concept.** The site is her letterhead made spatial: the header every Iranian patient knows from a prescription pad. It has her name, her degrees, the نظام پزشکی number, the address, both phones and the hours, and a ۳×۴ ID-photo slot. On desktop it stays fixed while the rest of the page scrolls past it, so the proof and the phone never leave the screen.

**Draws on:**
- Paziresh24: what a patient expects to find at once;
- van Straten: the name-and-degrees lockup;
- Digestive Health UK: the founder card and the phone always visible;
- Parsley: the buttons;
- taste-skill's "split stage" composition.

**Screenshots:**
- [desktop hero](mockups/screens/b-1440-hero.png), [desktop full page](mockups/screens/b-1440.png) (the letterhead is sticky, so the full-page capture shows it once)
- [phone hero](mockups/screens/b-390-hero.png), [phone full page](mockups/screens/b-390.png), [phone after scrolling](mockups/screens/b-390-scrolled.png)
- cards: [turned](mockups/screens/b-1440-flipped.png), [mid-turn](mockups/screens/b-1440-midturn.png)

### Type
- **Display: Amiri**, a classical Naskh with real stroke contrast. It reads like a printed letterhead.
- **Text: Vazirmatn.**
- I tried Markazi Text first. Its Arabic-script design is too close to the sans at bold, so the headline didn't look chosen.
- **Sample:** see the [specimen](mockups/screens/type-specimen.png). Amiri's Persian digits are elegant at display sizes (the phone numbers are set in it).
- **Risk:** Amiri is Arabic-first, so every Persian form (ی، ک، گ، ژ) must be checked in Stage 3. None looked wrong in the mockup.

### Palette (tokens)
| Token | Value | Role |
|---|---|---|
| `--sheet` | `#FFFFFF` | the letterhead, card fronts |
| `--ground` | `#E9EFEB` | the desk the sheet lies on |
| `--ink` | `#0F3A3E` | text, primary button, card backs |
| `--ink-2` | `#3E5F62` | secondary text (AA on both grounds) |
| `--gold` | `#C29A45` | the printed band: fills only |
| `--gold-ink` | `#8A6A24` | large gold numerals on white |

### Imagery without photos
- **The letterhead's printed bands**, in ink and gold.
- **The ۳×۴ photo slot**, the Iranian document-photo convention. A real portrait of any aspect is cropped to 3:4, and the lungs mark sits in the placeholder.
- **The lungs mark** small in the nav.
- Otherwise type does the work. It is the quietest direction.

### Motion character
- **Paper-quiet.**
- **Nav links** draw a gold underline (150 ms). **Topic pills** become outlines on hover (Parsley's secondary).
- **The flip card:**
  - front: a white certificate slip with a gold band on top and the year in large gold Amiri;
  - back: filled teal with the institution in ivory Amiri. That is the opposite of van Straten's white back, which vanished against a white page.

### Home page sketch
1. **Desktop, 42 / 58:**
   - The letterhead column is fixed: name, tagline, ۳×۴ photo, gold rule, the medical council number / address / hours lines, both phones in large type, and «تماس با مطب».
   - The scrolling column holds: the nav, then a statement headline («بیماری‌های ریه، از تشخیص تا برونکوسکوپی»), one paragraph, the top conditions as pills with «همه‌ی ۲۰ مورد», and the credentials (2×2 flip slips plus the membership lines).
2. **Phone:** the letterhead is the whole first screen (photo beside the name, both phones as full-width tap rows). The floating call tab takes over once it scrolls away.
3. *(Stage 4 adds)* locations and the footer in the scrolling column.

### Honest risk
- **The quietest of the three.** You said van Straten "doesn't feel rich", and B's richness is in typography and arrangement, not colour.
- **The fixed column needs care with 2–3 Clinic Locations:** the letterhead lists only the first one plus a «همه‌ی مطب‌ها» link, or it overflows.
- This is my own first-ranked candidate, which also means it's the one most runs would land on.

---

## 4. Direction C: the category standard

**Concept.** Parsley's structure played straight: a deep teal header bar, a warm sand hero with a large Naskh name, the portrait as a half-screen panel bleeding to the edge, teal pill buttons, and van Straten's row of dark tiles for credentials. Familiar and effective, with no surprises.

**Screenshots:**
- [desktop hero](mockups/screens/c-1440-hero.png), [desktop full page](mockups/screens/c-1440.png)
- [phone hero](mockups/screens/c-390-hero.png), [phone full page](mockups/screens/c-390.png)
- cards: [turned](mockups/screens/c-1440-flipped.png)

- **Type:** Noto Naskh Arabic (display) and Vazirmatn (text).
- **Palette:**

  | Token | Value |
  |---|---|
  | `--bar` | `#173F42` |
  | `--teal` | `#1F4F52` |
  | `--sand` | `#EADFCD` |
  | `--sand-2` | `#DCCBAE` |
  | `--page` | `#FAF7F1` |
  | `--gold` | `#C9A04A` |

- **Imagery:** this direction needs the portrait most. Its half-screen panel holds only the lungs mark until a photo arrives, and that is where it looks emptiest.
- **Motion:** Parsley's 150 ms colour hovers. Shafer's tab inverts on hover (400 ms). The flip goes from a teal tile to a gold back.
- **Honest risk:**
  - It fails the competitor test: put another doctor's name on it and it still fits.
  - Cream plus a serif is exactly the AI default the brief warns against.
  - It's the safest to build and the least memorable.

---

## 5. Recommendation

**I recommend Direction A, «چادرشب».**

- **It answers your own critique of the references.** van Straten "isn't rich"; Parsley feels richer, and its richness comes from colour and type, not motion. A gets that richness from flat colour fields, and that holds without a single photograph (checklist item 5).
- **It passes the competitor test.** It belongs to Mazandaran, and through the logo's teal and gold, to her. A Tehran pulmonologist couldn't wear it.
- **It keeps the proof first.** Name, titles, council number, the phone and the clinic are all on the first screen at 1440 and at 390.
- **Its one signature moment, the flip, is native to it:** a swatch of cloth turned over to its reverse.

**B is the strong alternative.** It is the clearest and the most Iranian in function: the letterhead and the ۳×۴ photo are things every patient already trusts. Choose B if you'd rather the site feel like her prescription pad than like her province.

I would not choose C, but it's a legitimate choice if you want the familiar route.

---

## 6. Page and section inventory

**Every page:**
- header with the lockup (`DoctorProfile.full_name`, plus `intro_tagline` or a fallback when it's empty);
- the clinic phone (the first `ClinicLocation.phone` by `order`);
- the floating call tab;
- a footer listing every Clinic Location with all its fields;
- default meta tags and `Physician` / `MedicalClinic` JSON-LD.

Site-wide data comes from **one context processor** (`profile`, `locations`).

### `/` Home
| Section | Fields |
|---|---|
| Hero + founder card | `full_name`, `intro_tagline` (fallback: hide the line, and the meta description falls back to the first sentence of `bio`), `photo_url`, the at-a-glance chips (each is **proposal-dependent**: council number, practising since), first location `phone`, `map_url` (the route button is hidden when it's empty), `name`, a short `address`, `hours` |
| Credentials preview | `Credential` rows with an `institution` → flip cards (up to 4); the rest → static rows (`title`, `year`) |
| Top conditions | the first 6 published `ConditionTreated` (category `condition`, by `order`): `title`, `short_description`, link to the detail page; then «همه‌ی بیماری‌ها و اقدامات» |
| Procedures teaser | the first published rows of category `procedure`; **the whole block is hidden when there are none** |
| Locations summary | each `ClinicLocation`: `name`, `address`, `phone`, `mobile_phone` (hidden when empty), `hours` (line breaks kept), `map_url`. One location is set as a single wide block, not a card in a grid; 2–3 become columns |

### `/about/`
| Section | Fields |
|---|---|
| Intro | `photo_url` (large), `full_name`, `intro_tagline` |
| Bio | `bio` split on `\n\n` into its 6 paragraphs, set as a reading column with the opening sentence of each paragraph as its lead (no invented headings). With Latin isolation applied. |
| Credentials | all `Credential` rows by `order`, `-year`: flip cards for those with an `institution` (and `detail`, if approved); a title-only card doesn't flip and sits in the static list |
| Contact strip | the shared phone/map block |

### `/conditions/`
| Section | Fields |
|---|---|
| Two labelled groups | «بیماری‌هایی که درمان می‌شوند» (category `condition`) and «اقدامات درمانی» (category `procedure`), published only, by `order`, `title`: each row shows `title` and `short_description` |
| Phone | 20 rows are one long list, so each group gets a heading jump at the top. A group with zero rows disappears together with its jump link |

### `/conditions/<slug>/` (Mayo structure)
| Section | Fields |
|---|---|
| Title + summary | `title` (Latin isolated, container stays RTL), `short_description` |
| "On this page" index | shown only when the body has 2 or more sections (proposal 7.1d) |
| Body | `body`, as paragraphs today; as sections with headings if 7.1d is approved |
| When to see a doctor | a fixed block leading to the first location's phones and the contact page |
| Associated procedures | only if 7.1c is approved; otherwise omitted |
| Meta | `<title>` = `title` + name, description = `short_description`, `MedicalCondition` JSON-LD. **An unpublished slug returns 404** |

### `/locations/`
Every `ClinicLocation`, all fields, ordered by `order`.
- **1 location:** a single wide composition (address, phones, hours, map link).
- **2–3:** equal columns.
- `map_url` empty → no route button, address only.

### `/contact/`
- The `Inquiry` form: `name`, `phone`, `preferred_contact_time`, `message`, the hidden honeypot `website`.
- Beside it: the phones and the address.
- The form says calling is fastest, and never pushes.

**Every model is placed:**
- `DoctorProfile`: every page;
- `Credential`: Home and About;
- `ConditionTreated`: Home and both conditions pages;
- `ClinicLocation`: every page;
- `Inquiry`: Contact.

---

## 7. For you to decide

Answer each one; they're independent.

### 7.1 Backend proposals (each optional; none built without your yes)

| # | Proposal | What it gives | Cost |
|---|---|---|---|
| a | `DoctorProfile.medical_council_number` (blank allowed) | the number patients use to verify a doctor, next to her name and in the JSON-LD | small: one field, one migration, a seed update, one admin line, a CONTEXT.md term |
| b | `DoctorProfile.practising_since` (Solar Hijri year, blank allowed) | an "experience" chip computed from the year, so it never needs updating | small. The template computes the years. Needs your answer on ۲۹ vs ۲۷ (7.4) |
| c | `DoctorProfile.paziresh24_url` (blank allowed) | «نظرات بیماران در پذیرش۲۴» as an outbound link; no reviews copied, no booking built | tiny |
| d | `Credential.detail` (optional text) | a longer back for the flip card, and something for the 4 cards that have no institution | small, plus content the doctor has to write |
| e | condition ↔ procedure links (`ManyToMany` from condition to procedure rows) | Mayo's "Associated procedures" (lung cancer → bronchoscopy) | medium: a migration and an admin widget, and someone has to curate the links |
| f | structured condition body. Recommended form: **keep one `body` field and let the editor start a section with a line beginning `## `**. The template splits on those lines into headed sections and builds "On this page" from them | Mayo sections now, with no new fields; today's 1–2 sentence bodies still render as one plain section | small: a template filter, test-first. The alternative (separate fields for symptoms, causes and so on) costs a migration and a much heavier admin form |

### 7.2 Frontend stack: **I recommend plain modern CSS plus small vanilla JS**

- **Plain CSS:** custom properties for the tokens, `@layer` for reset, base, components and pages, and logical properties for RTL.
- **JS:** about 3 small files (the flip card, the call tab, the mobile menu).
- **Why not Tailwind:**
  - Node is installed on this machine (v26; the prompt assumed it wasn't), but Runflare's build has none. Tailwind would mean a standalone CLI binary and a build step on every CSS change, with its output committed.
  - The site is 6 templates. A few hundred lines of hand-written CSS is smaller, needs no tool, and is easier to edit for whoever touches the templates next.
- **The cost:** no utility classes, so components need names and a little discipline.
- **htmx** is not needed: the form is a normal POST with a redirect.
- Sources live in `static_dev/`, then `collectstatic` as usual.

### 7.3 Images, logo and placeholder

| # | Proposal | Cost |
|---|---|---|
| a | **Process the uploaded photo with Pillow** when the profile is saved: make a 1200px and a 600px WebP, keep the original. Without it, an unedited 4000px, several-MB phone photo would be the LCP image on every page | medium: a small service and a test. Pillow is already installed |
| b | **A new placeholder:** the lungs mark from the logo on the direction's own ground (as in the mockups), replacing the cold blue-grey silhouette | tiny |
| c | **The logo's lungs as SVG.** For now the mark is cut from the 1080² JPEG (as in the mockups; it looks fine at 40–150px). A clean vector redraw by a designer, or a careful trace, is better for the header and favicons. The full circular badge stays as is, for the favicon set and Open Graph | tiny now; the redraw is external |
| d | **Fix `site.webmanifest`**: name «دکتر سپیده صفانوایی», the theme colour from the chosen palette, icon paths under `/public/static/…` | tiny (Stage 3) |

### 7.4 Content questions (only you or the doctor can answer)

The owner is asking the doctor. The full Persian version she reads is [`questions-for-doctor.md`](questions-for-doctor.md); it also asks for the clinic's map link and credential details. The medical review of the condition texts waits until the pages are built (a pre-launch task).


1. **Surname spelling:** صفانوایی (our seeds and the logo) or صفاءنوائی (Paziresh24)? The other spelling would go only in the meta keywords and JSON-LD `alternateName`, for search.
2. **Clinic hours:** «پذیرش بیماران: روزانه، شیفت عصر» or «ویزیت عصر ۳ روز هفته»? The bio mentions the hours too, so it needs editing in the admin as well.
3. **Imam hospital, Sari** (mornings, inpatients): a patient-facing Clinic Location, or not? All three designs take a second location without a layout change.
4. **Medical council number 51510:** show it? (Depends on 7.1a.)
5. **Years of experience:** ۲۹ (Paziresh24) or about ۲۷ (since 1378)? Show it at all? (Depends on 7.1b.)
6. **The portrait:** can you get the original of the photo on her Paziresh24 profile? Everything else on the shot list can wait until Stage 8.
7. **Email provider** for Inquiry notifications (not blocking).

### 7.5 The direction

**A, B or C?** Or "B's letterhead with A's colour" if you want a mix. I'd rather fold one into the other deliberately than average them, so say what you want kept.
