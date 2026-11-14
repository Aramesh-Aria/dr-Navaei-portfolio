# Design progress

This is the handoff file between chats. Each chat does the first stage below that isn't done, following [`docs/DESIGN_PROMPT.md`](../DESIGN_PROMPT.md). At the end of the stage, the chat updates this file and writes a commit message in chat. Chats never commit: the owner commits each stage before opening the next chat.

Kickoff line for every new chat:

> Read `docs/DESIGN_PROMPT.md` and `docs/design/PROGRESS.md`, then do the next stage.

## Stages

| # | Stage | Status | Gate |
|---|---|---|---|
| 0 | References (done before this workflow) | ✅ done 2026-11-14 | owner picked the sites |
| 1 | Inspection | ✅ done 2026-11-14 | — |
| 2 | Direction and mockups | ✅ done 2026-11-14, gate passed | **required:** choose a direction, answer the proposals and content questions |
| 3 | Foundation (branch, approved backend changes, tokens, `base.html`) | ✅ done 2026-11-14, gate passed | **required:** approve the shell |
| 4 | Home and About (credential flip cards) | ⬜ next | **required:** confirm the direction holds |
| 5 | Conditions and Locations | ⬜ | — |
| 6 | Contact and error pages | ⬜ | — |
| 7 | Motion, mobile and cleanup | ⬜ | — |
| 8 | Final review and report | ⬜ | **required:** decide on the merge |

Status values: ⬜ not started · 🟡 in progress (see its checkpoint) · ⏸ waiting at gate · ✅ done

## Decisions

Append one line per decision, with the stage it was made in. Never delete a line; if a decision is reversed, add a new line that says so.

- **Stage 0:** reference sites and the owner's notes are in [`references/README.md`](references/README.md).
  - Overall feel: Parsley.
  - Buttons: Parsley, Tia, Shafer.
  - Credentials: the van Straten flip card.
  - Condition page: Mayo.
  - Trust patterns: Digestive Health UK.
  - Expectations of an Iranian patient: Paziresh24.
- **Stage 0:** placeholder doctor photo through `DoctorProfile.photo_url`, no stock photos of people.
- **Stage 0:** email provider not chosen. `EMAIL_*` stays empty, prod uses the dummy backend, and inquiries are still saved.
- **Stage 0:** the site must support 1 to N Clinic Locations, with a second one addable from the admin alone.
- **Stage 1:** `/impeccable init` wrote [`PRODUCT.md`](../../PRODUCT.md) (product context for every later stage).
- **Stage 1 (owner):** the logo `public/static/assets/img/icon.jpg` (teal lungs, gold stethoscope, Nastaliq name) is a **binding brand asset**; its teal and gold are the palette's starting point.
- **Stage 1 (owner):** copy voice is **formal, third person**, as in the bio («دکتر صفانوایی…»، «ایشان…»).
- **Stage 1 (owner):** **pulmonology leads**; internal medicine and diabetes are clearly present but second.
- **Stage 1:** reference motions were measured in the in-app browser because the Playwright MCP server failed to connect; the stills were already in `references/`.
- **Stage 2:** three directions in [`01-direction.md`](01-direction.md), each with a mockup in `mockups/`:
  - **A «چادرشب»** (the Mazandarani woven cloth, re-dyed in the logo's teal and gold): Lalezar + Vazirmatn. Assigned by impeccable's concept roll (seed `seed:f14243bdf9bb95a4`, candidate 7 of 7); all six catalogue challengers were declined, and their disciplines were added to A.
  - **B «سربرگ»** (her letterhead, kept fixed beside the scrolling page, with a ۳×۴ photo slot): Amiri + Vazirmatn. My own first-ranked candidate.
  - **C**, the category standard (Parsley played straight): Noto Naskh Arabic + Vazirmatn.
  - **Recommendation: A**; B is the strong alternative.
- **Stage 2:** all three directions share these rules:
  - Only credentials **with an institution** flip; the rest are static rows.
  - The flip turns `rotateY(-180deg)` (mirrored for RTL) on hover (fine pointers only), on keyboard focus and on tap (`aria-pressed`). It goes in over 560 ms and back over 380 ms, `cubic-bezier(.2,.8,.2,1)`, and is interruptible because it's a CSS transition. Under reduced motion it becomes an opacity crossfade. Both faces stay in the DOM, so screen readers read both.
  - The floating call tab is hidden while the first screen's own call button is visible.
  - Latin runs are isolated with `<bdi>`.
- **Stage 2:** Markazi Text was tried for B and rejected: its Arabic-script design reads like the sans at bold.
- **Stage 2:** the decision page from impeccable `shape` was replaced by this document and the mockups, because the staged workflow makes the document the gate.
- **Stage 2:** Node v26 **is** installed on this machine (the prompt assumed it wasn't). Runflare still has none, so the stack recommendation doesn't depend on it.
- **Stage 2 gate (owner, 2026-11-14):** the direction is **A «چادرشب»**, with **Lalezar + Vazirmatn**.
- **Stage 2 gate (owner):** of the backend proposals in `01-direction.md` §7.1, these are approved:
  - **a** `DoctorProfile.medical_council_number`,
  - **b** `DoctorProfile.practising_since`,
  - **c** `DoctorProfile.paziresh24_url`,
  - **d** `Credential.detail`,
  - **f** `## ` sections in `ConditionTreated.body`.

  **e** (condition ↔ procedure many-to-many links) is **rejected for now**: nobody on the admin side has the medical knowledge to curate the links. The condition page has no "Associated procedures" block.
  - The owner numbered these 7.1–7.6 in reply; read as rows a–f of the §7.1 table (7.5 = e matches "many to many").
- **Stage 2 gate (owner):** this **reverses "leave the admin's look alone"**. The admin gets the same **django-jazzmin** theme as ArameshMusicAcademy-website, installed in Stage 3. The unread Inquiry count in the sidebar is added in Stage 6. The setup to copy is in `docs/plan.md` ("Admin theme"); `DESIGN_PROMPT.md` Stages 3 and 6 were updated to match.

- **Stage 2 gate (owner):** the stack is **plain modern CSS + small vanilla JS** (§7.2). No Tailwind, no htmx.
- **Stage 2 gate (owner):** **CSS and JS changes must reach visitors on a normal page load, never needing a hard refresh.** How Stage 3 delivers it:
  - **Production:** the manifest storage already gives every static file a content-hashed name, cached for a year. A changed file gets a new URL.
  - **The HTML pages carry `Cache-Control: no-cache`,** so the browser always fetches the page that links the new hashed name.
  - **Development:** static goes through WhiteNoise (`whitenoise.runserver_nostatic`) with `WHITENOISE_MAX_AGE = 0`, so an edited file shows on a plain reload.
  - **Tests**, written first:
    - `{% static %}` renders a hashed name with `DEBUG` off;
    - public pages send `Cache-Control: no-cache`.
- **Stage 2 gate (owner):** §7.3 approved as recommended:
  - **a** process the uploaded photo with Pillow (1200 px and 600 px WebP, original kept);
  - **b** the lungs-mark placeholder on the direction's own ground, replacing the blue-grey silhouette;
  - **c** the lungs as an SVG. A careful trace now; a designer's redraw can replace it later. The circular badge stays for favicons and Open Graph;
  - **d** fix `site.webmanifest`.

- **Stage 2 gate (owner):** the owner doesn't know the §7.4 answers and will ask the doctor later.
  - The questions are written out for her in [`questions-for-doctor.md`](questions-for-doctor.md), in Persian, one section each.
  - It includes the values for the new fields, plus two more items:
    - the clinic's map link (`map_url` is empty today),
    - optional text for `Credential.detail`, and a check of the credential years.
- **Stage 2 (owner):** the sheet asks only for what exists now or is needed to build. Everything else is moved to before launch, not asked now.
  - **The medical review of the 20 condition and procedure texts is a pre-launch task.** Once Stage 5 has built the condition pages, the doctor reviews them on the running site. Stage 8's report lists it under "what the owner must do".
  - The texts stay as the seeded starter copy until then.

- **Stage 2 gate passed (owner, 2026-11-14):** build with the current seeds while the doctor's answers are pending.
  - The new fields start empty (`medical_council_number`, `practising_since`, `paziresh24_url`, `Credential.detail`). Don't seed 51510 or a year until the doctor confirms them.
  - The surname, hours and single location stay as seeded.
  - Every answer must later fit with an admin edit or a seed update alone, never a layout change.

- **Stage 3:** branch `frontend-design` created from `main` at `adada23`. All later work happens there.
- **Stage 3:** new fields on `DoctorProfile` (`medical_council_number`, `practising_since`, `paziresh24_url`) and `Credential.detail`, migration `doctor/0003`. All start empty; no seed values (per the gate). Terms added to `CONTEXT.md`.
- **Stage 3:** a new `apps/core` app owns the public plumbing (no models): template filters, the context processor, the HTML caching middleware and the temporary shell view.
- **Stage 3:** photo processing: on save, `DoctorProfile` writes `<name>-600.webp` and `<name>-1200.webp` beside the original (never enlarged, EXIF-rotated). `photo_url` returns the 1200 copy, else the original, else the placeholder; `photo_srcset` gives both widths or "".
- **Stage 3:** the lungs mark is a contour trace of `mockups/assets/lungs-gold.png` (`static_dev/assets/img/lungs.svg`, 30 KB, one even-odd path). It is drawn with CSS `mask`, so one file takes any colour. The new placeholder (`doctor/doctor-placeholder.svg`) is gold lungs on `--field-2` at 4:5.
- **Stage 3:** fonts: the Google split files of Vazirmatn v33.003 (400/500/700) and Lalezar 1.004, copied from the owner's `vet-pharmacy` project (no download), subset with `pyftsubset` to Persian + Basic Latin + punctuation, 122 KB in total. **Lalezar has no Latin glyphs**, so Latin inside display type falls back to Vazirmatn 700 (a CSS rule on `bdi` keeps the weight close).
- **Stage 3:** HTML responses get `Cache-Control: no-cache` from `RevalidateHtmlMiddleware` (no-cache, not no-store, so the back/forward cache still works). Dev serves static through `whitenoise.runserver_nostatic` with `WHITENOISE_MAX_AGE = 0`; edited files come back as 304/200 on a plain reload.
- **Stage 3:** `SITE_URL = "https://dr.safanavaiee.ir"` (base settings) feeds the canonical link, Open Graph and JSON-LD. The default OG image is the circular badge `assets/img/icon.jpg`.
- **Stage 3:** JSON-LD: `Physician` (medicalSpecialty `Pulmonary`) with one `MedicalClinic` per Clinic Location. `openingHours` carries the free-text hours as they are (no structured hours, by design). `identifier` and `sameAs` appear only once the council number and Paziresh24 link are entered. No `addressLocality` is invented; the address goes in `streetAddress`.
- **Stage 3:** the header lockup shows `full_name` + `intro_tagline`; below 480 px the tagline line is hidden (it wrapped and crowded the bar).
- **Stage 3:** the nav label reads «مطب» for one location and «مطب‌ها» for more; the footer heading follows suit.
- **Stage 3:** the phone menu is a disclosure panel under the bar (not an overlay), with a 4 px gold thread at its foot. Escape closes it and returns focus. Without JS it is simply open.
- **Stage 3:** the floating call tab hides while any `[data-call-anchor]` is on screen (today: the header's phone pill and the phone call icon). Stage 4 marks the hero's call button with the same attribute.
- **Stage 3:** focus ring: `--madder` on light ground, `--gold` on teal (`.on-field`). Gold is never used on `--sea` (1.8:1).
- **Stage 3:** Jazzmin admin set up as in the academy. One extra RTL fix in `admin.css`: below 992 px AdminLTE hid the closed sidebar with `margin-left`, which in RTL left it covering the page; it now hides off the right edge.
- **Stage 3:** sidebar icons: `fa-user-md` (profile), `fa-lungs` (conditions), `fa-clinic-medical`/`fa-map-marker-alt` (locations), `fa-envelope-open-text` (inquiries).

- **Stage 3 gate (owner, 2026-11-14):** the shell and the admin are **approved**. One change asked: the admin logo shows an «S» instead of AdminLTE's «A» (`assets/img/admin-logo.svg`, set as Jazzmin's `site_logo`, which also becomes the admin favicon). While doing it, a second RTL fix went into `admin.css`: the brand text's gap was on the wrong side and the name touched the logo.

## Open questions for the owner

Waiting on the doctor (sent as [`questions-for-doctor.md`](questions-for-doctor.md)). Record each answer under Decisions when it comes back, then update the seeds or tell the Content Editor what to change in the admin.

- Surname spelling: صفانوایی (our seeds) or صفاءنوائی (Paziresh24)?
- Clinic hours: «روزانه، شیفت عصر» or «ویزیت عصر ۳ روز هفته»?
- Is Imam hospital in Sari (mornings, inpatients) a patient-facing second Clinic Location?
- Show the medical council number (51510)? (The field is approved; is 51510 the value to seed?)
- Email provider for Inquiry notifications (not blocking).
- Years of experience: Paziresh24 says ۲۹, the bio implies about ۲۷ (since 1378). The field (`practising_since`) is approved; which year goes in it?
- Can we get the original of the portrait on her Paziresh24 profile?
- **Still open at the Stage 2 gate:**
  - **Values for the approved fields:**
    - the council number to seed (51510?),
    - `practising_since` (1378, or the year behind Paziresh24's ۲۹ years),
    - the Paziresh24 URL.
  - **The content questions above**, or the owner's word to build with the seeds as they are.

## Handoff to next stage

**Stage 4 (Home and About) is next.** The Stage 3 gate is passed (shell and admin approved).

Screenshots to review (`docs/design/screens/stage3/`):
- shell: `shell-1440-top.png`, `shell-1440-full.png`, `shell-768-full.png`, `shell-390-top.png`, `shell-390-full.png`, `shell-390-menu.png` (phone menu open), `shell-390-scrolled.png` (call tab), `shell-390-footer.png`, `shell-1440-focus.png` (keyboard focus);
- worst case, three locations: `footer-1440-3-locations.png`, `shell-768-full-3-locations.png`;
- admin: `admin-1440-profile.png`, `admin-390-profile.png`, `admin-1440-logo.png`, `admin-logo-closeup.png`.

### Tokens (`static_dev/assets/css/site.css`, `@layer tokens`)
- **Colour:** `--field #0C3438`, `--field-2 #165257`, `--gold #D4A84E`, `--madder #A23B2C`, `--sea #E3ECE6`, `--ivory #F7F2E7`; derived inks `--ink` (= field), `--ink-2 #3B5A5C` (6.2:1 on sea), `--ivory-2 #C9D6D1` (9:1 on field). Gold never on sea. Madder only for stripes and focus.
- **Type:** `--font-display` (Lalezar, display only), `--font-text` (Vazirmatn). Sizes `--fs-small` 16 · `--fs-body` 18→19 · `--fs-lede` 19→22 · `--fs-h3` 22→28 · `--fs-tagline` 24→38 · `--fs-h2` 34→64 · `--fs-h1` 42→104 (px, fluid). `--lh-text 1.9`, `--lh-display 1.35`. Classes: `.display-1/2/3`, `.display-tagline`, `.lede`, `.prose`, `.eyebrow`, `.num` (tabular, LTR-isolated digits).
- **Space:** the 8px thread `--t`; `--s-1 … --s-15` (8 → 120); `--margin` clamp(20px, 4vw, 64px); `--wrap` 1312px; `--measure` 38em.
- **Shape:** `--r-0`, `--r-pill`, `--r-focus`, `--tap` 48px.
- **Motion:** `--ease-out cubic-bezier(.2,.8,.2,1)`, `--dur-hover 150ms`, `--dur-menu 220ms`, `--dur-tab 260ms`, `--dur-flip-in 560ms`, `--dur-flip-out 380ms`. Reduced motion is handled at the bottom of the file.
- **Layers:** `reset, tokens, base, layout, components, pages, utilities`. Page styles go in `@layer pages`.

### Components already built
`.wrap`, `.on-field` (teal surface, switches the focus ring to gold), `.stack`, `.actions`, `.mark` / `.mark--gold` (the lungs), `.selvedge` (via `partials/_weave.html`), `.pill` + `--gold` (primary on teal) / `--field` (primary on light) / `--line` (secondary on light) / `--line.--on-field` (secondary on teal) / `--small`, `.icon-button` (+`--gold`), `.clinics` / `.clinic` (1 location = one wide composition, 2+ = equal columns; reuse on Home and `/locations/`), `.calltab`, `.skip-link`, `.sr-only`.

### Template structure (`templates/`)
- `base.html` blocks: `title`, `description`, `og_type`, `og_title`, `og_description` (all in `partials/_meta.html`), `head` (extra head tags, e.g. a page's own JSON-LD), `body_class`, `content` (inside `<main id="main">`).
- Partials: `_meta.html`, `_icons.html` (sprite: `#i-phone`, `#i-route`, `#i-menu`, `#i-close`, `#i-out`), `_header.html`, `_nav_links.html`, `_footer.html`, `_calltab.html`, `_weave.html` (the selvedge; `{% include "partials/_weave.html" %}`).
- Context on every public page (`apps.core.context_processors.site`): `profile`, `locations` (list), `primary_location`, `site_url`, `default_description`. Empty on `/admin/`.
- Filters (`{% load site %}`): `fa_digits`, `phone_display`, `tel_href`, `isolate_latin` (escapes, then wraps Latin runs in `<bdi>`), `paragraphs` (splits on blank lines; use for the bio), `body_sections` (the `## ` sections: list of `{id, heading, paragraphs}`; build "On this page" from the ones with a heading). Tag: `{% physician_json_ld profile locations site_url %}` (already in `base.html`).
- JS: `static_dev/assets/js/site.js` (menu, call tab). Stage 4 adds the flip card there, reproducing `mockups/mockup.js`'s flip logic and the reduced-motion crossfade from `mockups/a.html`.
- Nav links are literal paths (`/about/`, `/conditions/`, `/locations/`, `/contact/`) in `_nav_links.html`; switch them to `{% url %}` as each view lands.

### For Stage 4
- **Delete the temporary pieces:** `apps/core/views.py` `ShellPreviewView`, `templates/core/shell_preview.html`, the `.preview-*` rules in `@layer pages`, and the `""` route in `config/urls.py`. The `ShellTests` in `apps/core/tests.py` request `/`; keep them passing against the real home page.
- Mark the hero's call button `data-call-anchor`.
- Use `profile.photo_url` with `profile.photo_srcset` + `sizes` on the portrait.
- Years of experience from `practising_since` still needs a test-first helper (Solar Hijri current year).
- Credentials: flip only the ones with an `institution`; `detail` goes on the back when present.

Pending, but not blocking:
- The doctor's answers ([`questions-for-doctor.md`](questions-for-doctor.md)). Record them under Decisions when they arrive.
- The medical review of the condition texts, before launch.
- The email provider.

Tooling: the Playwright MCP server works against `http://127.0.0.1:8018` (start the server first with the `django` launch config). Node v26 is available locally. `pyftsubset` (system Python's fontTools) was used for the fonts.
