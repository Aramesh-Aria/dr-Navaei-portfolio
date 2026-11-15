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
| 4 | Home and About (credential flip cards) | ✅ done 2026-11-14, gate passed | **required:** confirm the direction holds |
| 5 | Conditions and Locations | ✅ done 2026-11-14 | — |
| 6 | Contact and error pages | ✅ done 2026-11-15 | — |
| 7 | Motion, mobile and cleanup | ⬜ next | — |
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

- **Stage 4:** `/` is `apps.core.views.HomeView` (`core/home.html`), `/about/` is `apps.doctor.views.AboutView` (`doctor/about.html`). The shell preview view, template, CSS and route are deleted.
- **Stage 4:** credentials are split by one helper, `apps.doctor.views.credential_context(profile)`: `cards` (with an institution → flip), `rows` (the rest → static ribbons), `current` (the latest card by year, then order: her present post, «هیات علمی، دانشگاه علوم پزشکی مازندران», used as the founder card's caption). Home shows all of them, like About; there are only 4 + 4.
- **Stage 4:** Home sections in order: hero (founder card + name + tagline + chips + call/route + every location's one-line address and hours) → selvedge → credentials → the first 6 published conditions as "named threads" + «همه‌ی بیماری‌ها و اقدامات» → every published procedure as a numbered list on the cloth (the block disappears with zero) → the call band.
- **Stage 4:** the hero has **no lede sentence**: nothing in the data says it, and I didn't invent copy about her. The proof is the founder card caption and the credentials right below. The route button reads «مسیر مطب آمل» with a `map_url`, else «نشانی مطب آمل» → `/locations/`.
- **Stage 4:** chips (`partials/_facts.html`): «N سال تجربه», «طبابت از YYYY» and «شماره نظام پزشکی …» (gold), each only once its field is entered. Today none show. Years and year are separate chips: joined by «·» the two Persian-digit runs were reordered by bidi.
- **Stage 4:** years of experience: `years_since` filter over `solar_hijri_year(date)` (arithmetic Jalali conversion, tested at Nowruz 1403/1405).
- **Stage 4:** About bio: each `\n\n` paragraph is a row with its **first Solar Hijri year in the margin** (`first_year` filter; paragraph 2 has none, so its margin is empty) and its **opening sentence in bold** (`lead_sentence` filter). The «زندگی‌نامه» heading is sticky on desktop. The last paragraph's ۱۳۸۷ comes after ۱۳۹۵: that's the bio's order, kept as written.
- **Stage 4:** About's meta description is the bio's opening sentence; `og:type` is `profile`.
- **Stage 4 (bug fix from Stage 3):** the meta blocks were in an `{% include %}`d partial, where a child template cannot override blocks. They now live in `base.html`; `partials/_meta.html` is deleted.
- **Stage 4:** the flip card, as specified in Stage 2: a `<button aria-pressed>` with both faces in it (screen readers read title, year and institution). Hover (fine pointers only), `:focus-visible` and `aria-pressed="true"` turn it `rotateY(-180deg)`, 560 ms in / 380 ms out, `--ease-out`. A mouse click doesn't toggle (hover already turned it); a tap or Enter/Space does; Escape turns it back. Under reduced motion there's no turn, and the gold back crossfades in over 200 ms. The front's woven edge is a hard-stop gradient (four flat threads, no blend).
- **Stage 4:** card size: each `li` is an inline-size container; the 5:4 (4:5 below 600 px) is a **minimum** (`min-block-size: 80cqi` / `125cqi`), so a long institution or `detail` grows the card and its row instead of overflowing. 4 columns above 1100 px, 2 below.
- **Stage 4:** the call band (`partials/_call_band.html`) closes Home and About: every Clinic Location's name, both phones, hours, then links to `/locations/` and `/contact/`. Phone pills go full-width only below 600 px (at 768 they looked heavy).
- **Stage 4:** the floating call tab now starts `is-hidden` in the markup (it flashed visible on load before the JS ran); `html:not(.js)` shows it, and the JS reveals it when there's no anchor or no IntersectionObserver.
- **Stage 4:** two icons added to the sprite: `#i-turn` (the card cue) and `#i-forward` (points left: forward in RTL).
- **Stage 4:** UI copy written (formal, third person, no claims beyond the data): «پشت هر کارت آمده است که آن مدرک یا سمت کجا به دست آمده.», «اقدامات تشخیصی و درمانی ریه که دکتر صفانوایی انجام می‌دهند.», «برای گرفتن نوبت یا هر پرسشی، با مطب تماس بگیرید.»
- **Stage 4:** verified at 1440 / 768 / 390 with the seeds and with the worst case (3 locations, one with a long name and no mobile; empty tagline; council number and `practising_since` set; a long `detail`; zero procedures; a 16:9 landscape photo upload). No horizontal scroll, zero console messages, no 404s, one `h1`, every image with alt text, bio at 18 px on a phone. The dev database was restored from a backup afterwards and the test photo deleted.

- **Stage 4 gate (owner, 2026-11-14):** Home and About are **approved** as built; the direction holds. No notes for Stage 5.

- **Stage 5:** `/conditions/` is `apps.conditions.views.ConditionListView` (`conditions/list.html`), `/conditions/<slug>/` is `ConditionDetailView` (`conditions/detail.html`, URL name `condition`), `/locations/` is `apps.locations.views.LocationsView` (`locations/list.html`; the locations come from the context processor). Every internal link now uses `{% url %}` except `/contact/` (Stage 6).
- **Stage 5:** the list page opens with a cloth band (`.pagehead`): the `h1`, one line of copy, and two jump pills with each group's count in gold. The jumps appear only when both groups have rows; an empty group disappears with its jump. Conditions reuse the named threads; procedures reuse Home's numbered list on the cloth, now with their short descriptions.
- **Stage 5:** the threads and the numbered procedures are shared partials now (`_threads.html`, `_procedures.html` with `describe=True`); Home uses them too.
- **Stage 5:** the condition page, in Mayo's order: crumbs (list / category) → `h1` title (a smaller display size, `.pagehead__title--long`) → `short_description` as the lede → selvedge → body → "when to see a doctor" → back link. The body's untitled opening section is set at lede size, so today's one or two sentences read as an overview, not a stub.
- **Stage 5:** two layouts, chosen by the view's `toc` (the body's `## ` sections, only when there are 2 or more): **without an index** (today), the body sits beside a sticky "when to see a doctor" panel; **with an index**, a sticky "در این صفحه" sits at the start, and the panel follows the body. Phones stack both.
- **Stage 5:** the "when to see a doctor" panel (`conditions/_see_doctor.html`) is a teal swatch with the flip card's woven edge: the first location's phone (gold, a `data-call-anchor`) and mobile, its name and hours, links to `/locations/` and `/contact/`, and an emergency line. Procedures get «نوبت و مشاوره» instead. The detail page has no call band (the panel is its call to action).
- **Stage 5:** UI copy written for the doctor's review (formal, no claims about her): condition «اگر این علائم را دارید، یا با درمان فعلی بهتر نشده‌اید، برای گرفتن نوبت ویزیت با مطب تماس بگیرید.»; procedure «تصمیم به انجام این اقدام پس از ویزیت و بررسی پرونده گرفته می‌شود…»; emergency «در شرایط اورژانسی، مانند تنگی نفس شدید یا درد قفسه‌ی سینه، با ۱۱۵ تماس بگیرید یا به نزدیک‌ترین اورژانس بروید.» (`tel:115`). The emergency line is general safety guidance; it goes on the doctor's pre-launch review list.
- **Stage 5:** structured data: condition pages add `MedicalCondition`, procedure pages add `MedicalProcedure` (the correct schema.org type for them), with `name`, `description`, `url`, beside the site-wide `Physician`. `og:type` is `article`.
- **Stage 5:** `/locations/`: one location is a single wide ivory panel under a woven top edge, with the name (display size) and address plus actions on one side and the phones and hours on the other, split by a teal rule. It stays two columns down to 700 px. 2+ locations are equal columns (`auto-fit`, min 340 px). The `h1` reads «مطب» / «مطب‌ها». No map link → no route button, address only.
- **Stage 5:** a **«کپی نشانی»** button per location (for pasting into a taxi or map app): shown only where the async clipboard is available, it turns into «نشانی کپی شد» with a check icon for 2.4 s and announces it through a live region. Icons added: `#i-copy`, `#i-check`.
- **Stage 5:** Home's procedures lede hardcoded «دکتر صفانوایی»; it now uses `profile.full_name`, so the surname answer stays an admin edit.
- **Stage 5:** verified at 1440 / 768 / 390: one `h1` per page, no horizontal scroll, zero console messages, every internal link resolves except `/contact/` (Stage 6), focus ring visible (madder on the light ground, gold on the panel), tab order follows the reading order. Worst cases checked in the dev DB (restored from a backup afterwards): a 4-section body with Latin (PFT), the long Latin procedure title, 2 and 3 locations (a long name, no mobile, Persian digits and spaces in a phone, two-line hours, a map link). Zero procedures, zero locations and unpublished/unknown slugs (404) are covered by tests.

- **Stage 6:** `/contact/` is `apps.inquiries.views.ContactView` (`inquiries/contact.html`, URL name `contact`) with `apps.inquiries.forms.InquiryForm` (name, phone, preferred contact time, message; no medical-detail field). Every internal link now uses `{% url %}`.
- **Stage 6:** a sent form redirects back to `/contact/` (a reload never sends twice); the confirmation shows once, carried by a one-time `messages` entry. It replaces the form in place and takes focus.
- **Stage 6:** phones are normalised by `normalise_phone`: Persian or Arabic-Indic digits, spaces, dashes, brackets and a `+98`/`0098` prefix are accepted and saved as 11 ASCII digits starting with 0; anything else is refused. Letters are refused, not stripped. The error message gives one example written without spaces (a grouped number in a plain-text message is reordered by bidi).
- **Stage 6:** the honeypot `website` is off-screen (not `display:none`), `aria-hidden`, `tabindex="-1"`. Filled → nothing saved, no email, but the same confirmation (a bot learns nothing).
- **Stage 6:** email: `notify()` sends only when `INQUIRY_NOTIFICATION_EMAIL` is set (read with `getattr`, so dev and tests need no setting), after the save; a failing send is logged, never raised. The body has name, phone, time, message and the admin link.
- **Stage 6:** errors: Persian messages for every field; an error summary at the top (links to each field, focused on load); each invalid field gets `aria-invalid` and `aria-describedby` = its hint + its error. The form is `novalidate`, so the browser's own (possibly English) bubbles never show.
- **Stage 6:** fields are square (the cloth has hard edges), 56 px tall, 18–19 px text (no iOS zoom), `autocomplete` and `inputmode="tel"`; the phone is `dir="ltr"` but right-aligned with the labels. The send button says «در حال فرستادن…» and refuses a second press; `pageshow` resets it after back/forward.
- **Stage 6:** contact layout: the phones on the start side (sticky on desktop, numbers at 26–34 px, the first one a `data-call-anchor`), the form in an ivory panel with the woven top edge beside them. Below 960 px the phones come first and 2+ clinics sit in columns where they fit.
- **Stage 6:** UI copy written (for the doctor's review): the page lede, «نام و شماره‌تان را بنویسید تا مطب با شما تماس بگیرد.», the sent text «مطب در نخستین فرصت با شماره‌ای که گذاشتید تماس می‌گیرد.» (a promise about the clinic's process: confirm it with her), the privacy hint on the message field, and «این فرم برای شرایط اورژانسی نیست…» with `tel:115`.
- **Stage 6:** the unread Inquiry count: `apps.core.admin.SiteAdminSite.get_app_list` appends «(N)» in Persian digits; `apps.core.admin_config.SiteAdminConfig` replaces `django.contrib.admin` in `INSTALLED_APPS`. Checked in Jazzmin's sidebar and the index.
- **Stage 6:** error pages: `handler404` = `apps.core.views.page_not_found` (`404.html`: «۴۰۴» in gold, home / conditions / phone, then the first six published conditions as threads, `noindex`). `handler500` = `server_error` (`500.html` stands alone: no `base.html`, no context processors; it reads the profile and first location in a `try`, so without a database it still renders, without the phone; if the template fails, a plain «Server Error (500)»). `CSRF_FAILURE_VIEW` = `csrf_failure` (`403_csrf.html`, «فرم منقضی شد», a link back to the form): added because the contact form left open too long is its realistic cause.
- **Stage 6:** one icon added: `#i-alert` (field errors).
- **Stage 6:** verified at 1440 / 768 / 390: no horizontal scroll, zero console messages on `/contact/`, no 404s among assets, focus order header → phones → form (honeypot skipped), visible focus on fields, a real submit with «۰۹۱۲ ۱۲۳-۴۵۶۷» saved as `09121234567` (then deleted). 404 and 500 checked on a temporary `DEBUG=False` server (removed afterwards). Worst case: 3 locations (a long name with Latin «ICU», no mobile, Persian digits and spaces in a phone, two-line hours) in the dev DB, restored from a backup afterwards. No new motion this stage beyond 150 ms colour transitions, so reduced motion needs nothing new.

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

**Stage 7 (Motion, mobile and cleanup) is next.** Stage 6 has no gate.

Screenshots (`docs/design/screens/stage6/`): `contact-1440-full.png`, `contact-1440-errors.png`, `contact-1440-focus.png`, `contact-768-three-locations.png`, `contact-390-full.png`, `contact-390-errors.png`, `contact-390-sent.png`, `404-390-full.png`, `500-1440-full.png`.

### Template structure (updated)
- `base.html` blocks: unchanged. The error pages put `<meta name="robots" content="noindex">` in `head`.
- New templates: `inquiries/contact.html`, `404.html`, `403_csrf.html`, `500.html` (standalone; keep it free of anything that needs the database or a context processor).
- Icons: `#i-alert` added to the sprite.
- New components: `.form`, `.field` (`__hint`, `__error`, `__optional`, `--invalid`), `.form__summary`, `.form__trap`, `.form__send`, `.form__urgent`, `.sent`, `.pagehead__code`, `.pagehead__actions`; page layout `.contact` (`__grid`, `__call`, `__clinics`, `__clinic`, `__panel`).
- `site.js` part 5: `[data-focus-on-load]` takes focus; `[data-form]` / `[data-send]` / `[data-send-label]` for the sending state.

### For Stage 7
- Candidates for `find-animation-opportunities`: the sent state appearing (today it just renders), the error summary. Keep it quiet; the flip card stays the one signature moment.
- `mobile-native`: check the form on a real phone keyboard (the `tel` pad, autofill of name and phone), and the safe area under the full-width call tab on `/contact/` (the tab hides while the first phone is on screen).
- The academy-style `apps/core/admin.py` imports `Inquiry` inside the method to avoid an app-loading cycle; leave it there.

Pending, but not blocking:
- The doctor's answers ([`questions-for-doctor.md`](questions-for-doctor.md)). Record them under Decisions when they arrive.
- The medical review before launch: the condition texts, the "when to see a doctor", procedure and emergency lines (Stage 5), **and now the contact page copy, especially the promise that the clinic calls back** (Stage 6).
- The email provider. Until then `INQUIRY_NOTIFICATION_EMAIL` stays empty and Inquiries are read in the admin.

Tooling: the Playwright MCP server works against `http://127.0.0.1:8018`. To see the 404/500 pages, run a second server with `DEBUG = False` and `--nostatic` (a scratch settings module importing `config.settings.dev`); the dev server shows Django's debug pages instead.
