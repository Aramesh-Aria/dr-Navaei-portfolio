# Stage 8: final review and report

Written on 2026-11-15 on `frontend-design`. It covers Stages 3–7 plus the owner's commit `339396f` (the captcha, the 400/403 pages, the primary bio button), and the fixes made in this stage.

**The decision this report asks for** is at the end: [merge or not](#the-merge-decision).

Contents:
1. [Summary](#1-summary)
2. [The $10K checklist, with evidence](#2-the-10k-checklist-with-evidence)
3. [Speed](#3-speed)
4. [What the reviews found, and what was done](#4-what-the-reviews-found-and-what-was-done)
5. [Known gaps](#5-known-gaps)
6. [Photo shot list for the doctor](#6-photo-shot-list-for-the-doctor)
7. [What the owner must do](#7-what-the-owner-must-do)
8. [Pre-launch content tasks for the doctor](#8-pre-launch-content-tasks-for-the-doctor)
9. [Proposals that need your decision](#9-proposals-that-need-your-decision)

All screenshots are in [`screens/stage8/`](screens/stage8/). Each page has a full-page capture at **1440×900**, **768×1024** and **390×844** (`<page>-<width>.png`), plus the first screen alone (`<page>-<width>-fold.png`). The 404 page is captured at all three widths and the 400 page at 390 and 1440, all from a `DEBUG=False` server. They were taken on the final build with the seeded content, which is the site as it would launch today.

---

## 1. Summary

The site is built as approved: direction A «چادرشب», set in Lalezar and Vazirmatn, in plain CSS with small vanilla JS. It has six public pages, the 400/403/404/500 and expired-form pages, and the Jazzmin admin.

| Review | Result |
|---|---|
| impeccable `critique` (two isolated reviewers) | design review **30/36 (Good)**. Verdict: "authored, not interchangeable". The detector found **0** issues in the templates. The browser overlay flagged a contrast false positive and one real minor issue, an 86-character line on About (section 5) |
| impeccable `audit` | **16/20 (Good)**: Accessibility 3, Performance 3, Theming 3, Responsive 3, Implementation Integrity 4 (pass) |
| `code-review` (standards + spec) | 4 bugs or gaps fixed; 6 findings kept on purpose or deferred, each with its reason (section 4 and appendix B) |
| `break-ui` (whole site; worst-case, sparse and three-clinic data at 1440/1024/768/390) | 4 breaks found and fixed: the phone footer with 2+ clinics, a pasted URL that scrolled every page sideways, nav labels wrapping beside a long tagline, and «COVID-19» split at its hyphen in a heading |
| Tests | **152 pass** (143 at the start of the stage) |
| LCP | **60–96 ms** on localhost, **684–760 ms** on simulated slow 4G, on every page; transfer **218–262 KB** |

My recommendation is to merge. Nothing in section 5 blocks a merge. Launching needs the owner tasks in section 7 and the doctor's review in section 8.

---

## 2. The $10K checklist, with evidence

### 1. Point of view, not a template ✅
- **The concept:** the Mazandarani chadorshab, re-dyed in the logo's teal and gold.
  - Flat colour fields carry the page.
  - The woven selvedge marks only the seams: under the hero, on the card feet and on panel heads. It is never used as a background pattern.
  - The logo's lungs, traced as an SVG, sit in the portrait frame and the header.
- **Competitor test:** a reviewer working blind (critique Assessment A) concluded that another doctor's name "would break" it. The reasons it gave:
  - the Jalali-year credential swatches;
  - the bio set as a timeline of years in the margin;
  - the Amol-specific procedure list on the cloth.
- **Evidence:** [`home-1440-fold.png`](screens/stage8/home-1440-fold.png), [`about-1440.png`](screens/stage8/about-1440.png), [`about-768.png`](screens/stage8/about-768.png), [`about-390.png`](screens/stage8/about-390.png).
- **Where it is weakest:** the condition pages, because their bodies are one or two sentences. The cloth header promises more than the text delivers. This resolves once the doctor's reviewed text arrives (section 8). The layout already supports `## ` sections and an "on this page" index.

### 2. Typography that does work ✅
- **Faces:**
  - Lalezar (display only, one weight);
  - Vazirmatn 400/500/700 for text.
  - Both are self-hosted woff2, subset to Persian plus Basic Latin, with `font-display: swap`. Two of them are preloaded. Together they are 122 KB.
- **Latin inside display type:** Lalezar has no Latin glyphs, so Latin falls back to Vazirmatn 700 inside `<bdi>`. Seen in «COPD (بیماری انسدادی مزمن ریه)»: [`copd-390-fold.png`](screens/stage8/copd-390-fold.png).
- **Size floor:** body text measures 18.06 px on a phone. This stage raised the address, hours, the emergency line, field hints and the condition descriptions to body size on phones (they were 16 px). 16 px now carries only labels.
- **Digits:** Persian digits everywhere go through `fa_digits` / `isolate_latin`. As of this stage, `isolate_latin` also turns ASCII digits that an editor types (for example «طبقه 3») into Persian ones, and keeps «COVID-19» whole inside its `<bdi>`.
- **Evidence:** every `*-390.png`.

### 3. A restrained colour system ✅
- **Five tokens plus one tint:** `--field` teal, `--field-2`, `--gold`, `--madder`, `--sea`, `--ivory` (`--ivory-2` for secondary text on teal).
- **Measured contrast**, with zero failures on any page:

  | Pair | Ratio |
  |---|---|
  | ink on sea | 11.1:1 |
  | ivory on field | 12.0:1 |
  | ivory-2 on field | 9.0:1 |
  | gold on field | 6.1:1 |
  | ink-2 on ivory | 6.7:1 |
  | madder on ivory | 5.9:1 |

- **Rules kept:**
  - Madder is used only for stripes, the focus ring and error text. This stage removed its one use as link colour, on the contact page's «۱۱۵».
  - Gold never sits on `--sea`.
- Dark mode was never part of the brief, and the audit didn't mark it down.

### 4. Hierarchy that breathes ✅
- **The six-paragraph bio** has each paragraph's first Solar Hijri year in the margin and its opening sentence in bold, and the «زندگی‌نامه» heading is sticky on desktop.
  - This stage stopped a one-sentence paragraph from turning entirely bold. On a phone it had read as a wall of bold.
  - See [`about-390.png`](screens/stage8/about-390.png).
- **The 20 conditions and procedures** are two labelled groups, with jump pills that show each group's count: conditions as "named threads", procedures as a numbered list on the cloth. See [`conditions-1440.png`](screens/stage8/conditions-1440.png) and [`conditions-390.png`](screens/stage8/conditions-390.png).

### 5. Imagery with intent ✅ (better with photos)
- **Without photos:** the gold lungs mark on `--field-2`, inside a woven portrait frame at 4:5. This is the LCP element on Home at 1440 and on About.
- **With a real portrait:** uploads are converted to 600 and 1200 px WebP on save (`srcset`), shown with `object-fit: cover` and framed the same way.
- **No stock photos of people anywhere.** The medical illustration is the logo's own lungs, traced.
- The shot list is in section 6.

### 6. Motion that whispers ✅
- **The one signature:** the credential flip. It turns `rotateY(-180deg)` (mirrored for RTL) over 560 ms in and 380 ms out on `cubic-bezier(.2,.8,.2,1)`, and under reduced motion it becomes a crossfade. See [`about-1440-card-turned.png`](screens/stage8/about-1440-card-turned.png).
- **Everything else:**
  - 150 ms colour hovers;
  - a `scale: .97` press;
  - the sent-check and copy-check settles;
  - a 150 ms menu fade under reduced motion.
- **Fixed this stage:**
  - A keyboard user could not turn a card back, because CSS `:focus-visible` held it turned. Now, with JS, focus turns the card through `aria-pressed`, so Enter, Space and Escape toggle it and leaving it turns it back. Without JS, focus alone still turns it. Verified with real key presses in Playwright.
  - The captcha's "new image" button was missing from the reduced-motion list. It now has no press scale there.
- **Animation reviews:** `review-animations` and `animation-performance` passed in Stage 7. This stage added no new animation. It made the two fixes above and gave the captcha button the shared 160 ms press transition. `review-animations` approved that button's motion (section 4, row 26). Everything still animates only `transform`, `opacity` and `scale`.

### 7. Mobile that's designed, not shrunk ✅
- **Navigation:** a disclosure panel under the bar, with the clinic's phones in it. Escape closes it and focus returns to the button. See [`home-390-fold.png`](screens/stage8/home-390-fold.png).
- **Tap-to-call:**
  - The header carries a gold call icon.
  - Call pills are full-width, 56 px tall.
  - The floating call tab appears once the first screen's call buttons scroll away, and steps aside while you type.
- **The 20 conditions:** jump pills to each group, then the threads.
- **Credential cards:** two columns at 4:5, turning on tap.
- **Locations:** one wide panel with «کپی نشانی» (for a taxi app), and a route button once a map link exists.
- **The form:**
  - 56 px fields at 18–19 px text, so iOS never zooms;
  - `inputmode="tel"`;
  - an error summary that takes focus. See [`contact-390-errors.png`](screens/stage8/contact-390-errors.png).
- **Fixed this stage:**
  - With 2 or more clinics, the phone footer kept its desktop columns. That squeezed the doctor's name into a 76 px column.
  - The footer phone links are now 44 px tall (they were 31).

### 8. The invisible expensive stuff ✅ (one known gap: the captcha, section 5)
- **Speed:** LCP is far under 2 s, even on simulated slow 4G (section 3).
- **Keyboard:** full keyboard path, and a 3 px focus ring (madder on light ground, gold on teal).
- **Structure:**
  - landmarks, a skip link, one `h1` per page, headings in order;
  - `lang="fa" dir="rtl"`;
  - zero console errors or warnings and no 4xx among 217 responses: seven pages (including a procedure page) at all three widths, on the final build served as in production.
- **Meta on every page:** title, description, Open Graph and canonical.
  - This stage removed the canonical and `og:url` from the 400/403/404 and expired-form pages. A missing page must not name itself as the canonical address.
- **Structured data:** `Physician` plus one `MedicalClinic` per location, `MedicalCondition` / `MedicalProcedure` on detail pages.
- **The form:**
  - Persian errors for every field;
  - `aria-invalid` / `aria-describedby`;
  - the error summary takes focus.
  - This stage gave the captcha its own Persian "required" message; it used to show Django's generic «این فیلد اجباری است.».

---

## 3. Speed

Measured with Playwright Chromium against a **`DEBUG=False` server with `--nostatic`**: the committed hashed and gzipped files, served by WhiteNoise as in production. The cache was disabled for every load.

**These are lab numbers on localhost.** The "slow 4G" rows are throttled to 1.6 Mbps down and 150 ms RTT. A real Iranian mobile connection can be worse, so check after launch.

| Page | LCP, localhost (390 / 1440) | LCP, slow 4G (390 / 1440) | LCP element | Transfer | Requests |
|---|---|---|---|---|---|
| `/` | 88 / 72 ms | 748 / 760 ms | a hero text line at 390 / the portrait at 1440 | 239 KB | 11–12 |
| `/about/` | 80 / 96 ms | 740 / 748 ms | portrait | 237 KB | 11 |
| `/conditions/` | 68 / 92 ms | 684 / 708 ms | lede / `h1` | 225 KB | 10 |
| `/conditions/copd/` | 80 / 72 ms | 704 / 704 ms | body / `h1` | 219 KB | 10 |
| `/locations/` | 60 / 88 ms | 692 / 712 ms | address | 218 KB | 10 |
| `/contact/` | 96 / 92 ms | 744 / 724 ms | lede / `h1` | 261–262 KB | 11 |

Where the bytes go:
- fonts: 122 KB (four woff2 files; on later pages they come from the cache);
- CSS: 11 KB gzipped;
- JS: 2.7 KB gzipped;
- `lungs.svg`: 12 KB gzipped;
- each HTML page: 13–21 KB;
- the contact page also loads the 400×140 captcha image.

There are no outside requests: no CDN, no analytics, no web fonts from Google.

---

## 4. What the reviews found, and what was done

### Fixed in this stage (test-first where a test can see it)
| # | Found by | Problem | Fix |
|---|---|---|---|
| 1 | code-review (standards) | `fa_digits\|isolate_latin` split «COVID-19» into `<bdi>COVID</bdi>-۱۹`, which is the bidi break `<bdi>` exists to prevent | `isolate_latin` accepts Persian digits inside a Latin run (3 tests) |
| 2 | code-review (both) | Address, clinic name, titles and the bio skipped `fa_digits`, so «طبقه 3» from the admin showed ASCII digits | `isolate_latin`, which every editor-typed field goes through, now writes digits outside Latin runs in Persian |
| 3 | code-review (spec) | A keyboard user couldn't turn a flip card back | see checklist item 6 |
| 4 | code-review (spec), audit | Error pages declared a canonical address for the missing URL | a `{% block address %}`, emptied on the 400/403/404/CSRF pages (tests) |
| 5 | code-review (spec) | The honeypot was checked only after validation, so a bot that sent invalid data saw the error page | checked first in `post()`: same confirmation, nothing saved (test) |
| 6 | critique, audit | The captcha had no alternative for someone who can't read the image (WCAG 1.1.1) | a line under it: «اگر خواندن تصویر برایتان دشوار است، با … تماس بگیرید.», linking the clinic phone (test) |
| 7 | audit | The captcha was blurry on 2× and 3× phones | drawn at 400×140 and shown at 200×70 CSS px (test) |
| 8 | audit | The captcha's "required" error didn't name the field | «لطفاً کد امنیتی تصویر را بنویسید.» (test) |
| 9 | audit | A failed "new image" said nothing, and the button dropped focus | «تصویر تازه نیامد. دوباره امتحان کنید.» in a live region; `aria-disabled` keeps focus. Verified with the request blocked |
| 10 | critique | «نشانی مطب و مسیر» promised a route that doesn't exist (`map_url` is empty) | «و مسیر» appears only once some location has a map link (`has_route`, 2 tests) |
| 11 | critique | The emergency line was the last, smallest item on the condition panel | moved directly under the panel title, at body size |
| 12 | critique | Madder used as text colour (the contact form's «۱۱۵») | now `--field`, underlined |
| 13 | critique | A one-sentence bio paragraph was entirely bold | bold only when a paragraph has more than one sentence |
| 14 | audit | 16 px reading text on phones | raised to body size on phones (checklist item 2) |
| 15 | audit | Footer phone links were 31 px tall | 44 px |
| 16 | break-ui | Phone footer with 2+ clinics: the name squeezed into 76 px | `:has(.clinics--many)` outranked the phone rule; both are now stacked |
| 17 | code-review (standards) | Four hashed static copies were no longer named by the manifest | deleted |
| 18 | hygiene | 21 Playwright MCP session files had been committed | `.playwright-mcp/` is now in `.gitignore` and removed from the index |
| 19 | break-ui | A URL pasted into an address («… https://neshan.org/maps/places/d2c1…») scrolled every page sideways, at every width | `overflow-wrap: break-word` on the body, and `anywhere` on the editor-typed address, name and description classes |
| 20 | break-ui | With a long tagline at 961–1100 px, the nav labels wrapped to three lines and the header grew to 202 px | nav labels never wrap; the header's degrees line hides between 961 and 1100 px (it is also in the hero and the footer) |
| 21 | break-ui | «COVID-19» in a heading split at its hyphen, so «19» began the next line | Latin runs in `h1`–`h3` don't wrap |
| 22 | code-review follow-up | A space let a Latin run swallow a following number («ICU 2» kept an ASCII 2) | a space continues a run only into a letter (2 tests) |
| 23 | craft floor | An eyebrow «درباره‌ی دکتر» above About's `h1` (the floor bans eyebrows) | removed |
| 24 | craft floor | Colored side borders over 1 px: the error summary's 4 px stripe, the index's 2 px rail | a full 2 px madder frame on the summary; a 1 px rail. The `side-tab` hook flag is gone |
| 25 | craft floor | The header's degrees line was 14 px | 16 px (the label floor) |
| 26 | review-animations | The captcha button's press `scale` snapped; every other pressable eases over `--dur-press` | the same 160 ms press transition. Verdict: **Approve** |

### Checked and kept on purpose
- **The detector's `gray-on-color` on `--ivory-2` over teal:** a false positive. The pair measures 9.0:1, and the colour is a teal-tinted secondary-text token, not a muddy grey.
- **The flip still turns on keyboard focus.** That is the approved Stage 2 spec. The critique suggested Enter/Space only; the fix in row 3 answers the real problem, which was that a card couldn't be turned back.
- **The `openingHours` JSON-LD holds the free-text hours.** This is the Stage 3 decision: per-day hours are out of scope. schema.org validators will warn; Google ignores the field.
- **`medicalSpecialty: "Pulmonary"`.** Pulmonology leads (owner decision), and schema.org has no internal-medicine value.
- **Hand-written Persian digits in fixed UI copy** (the «۱۱۵» links, the error codes «۴۰۴»…, the phone example in the error message): the rule targets data. These are constants in the copy, so `fa_digits` would add nothing.
- **Code smells the standards review flagged, deferred as judgement calls:**
  - `templatetags/site.py` mixes digits, phones, the calendar, text parsing and JSON-LD;
  - JSON-LD builds condition URLs by hand and compares `category` to a string;
  - the 400/403/404/CSRF page heads are near-identical;
  - the nav compares literal paths.
  
  None changes behaviour; each is a refactor for after the merge.
- **Additions not in the prompt** (spec review), all recorded in earlier stages and kept: the «کپی نشانی» button, the expired-form page, `MedicalProcedure` JSON-LD, and the emergency «۱۱۵» lines.

---

## 5. Known gaps

Read these before launch. None blocks the merge.

1. **The captcha is still an image of Latin letters.** It is the owner's choice (`339396f`), and it is kept.
   - It is now sharp, it has a phone alternative, and it names its errors.
   - But an older patient on a Persian keyboard must still switch to English letters. It is the hardest moment on the site; both reviewers rated it the top issue.
   - A screen-reader user's alternative is the phone, not the form.
   - See proposal 9.1.
2. **The phone's first screen carries no proof until the doctor answers.**
   - The chips «N سال تجربه», «طبابت از …» and «شماره نظام پزشکی …» appear as soon as `practising_since` and `medical_council_number` are entered.
   - Until then the phone hero shows the name, the degrees line and the address.
   - Checked with the worst-case data: with the chips filled, they sit on the phone's first screen, under the name and degrees.
3. **Condition pages are thin** until the doctor's reviewed texts arrive. The "on this page" index appears only once a body has two or more `## ` sections, which no seeded body has today.
4. **Not checked on a real phone:** the keyboard with the call tab stepped aside, the landscape notch padding, autofill, and the flip at 120 Hz.
5. **Left for later, small:**
   - nine `rgb(… / alpha)` literals that repeat token colours (they could use `color-mix()`);
   - `lungs.svg` and the placeholder are 30 KB each before gzip (12 KB gzipped); a simplified path would cut about 75%;
   - the Stage 7 simplify items that need a model change (proposal 9.2).
6. **Drift found while writing `DESIGN.md`:** the 14 px degrees line, the eyebrow and the over-1 px side borders. All three were fixed afterwards (section 4, rows 23–25), and `DESIGN.md` describes the fixed build.
7. **One About paragraph runs to about 86 characters a line at 1440** («ایشان از سال ۱۳۸۷ عضو انجمن…»), slightly over the 80 target. It is borderline for Persian at this size, so it was left.
8. **With zero procedures published**, the list page's `h1` and the nav still say «بیماری‌ها و اقدامات». The procedures block and its jump pill do disappear. Nobody plans to unpublish all five, so it was left.
9. **Error pages:**
   - **This stage:** 404 and 400 were rendered and captured on a `DEBUG=False` server.
   - **Not rendered this stage:** 403, the expired form and 500. Their templates changed only by emptying the `address` block, and tests cover all three; they were last seen in Stage 6 and in `339396f`.
   - The dev server always shows Django's own debug pages instead.

---

## 6. Photo shot list for the doctor

Nothing on the site waits for these. Each one makes it better.

| # | Photo | Where it goes | Framing and size | Notes |
|---|---|---|---|---|
| 1 | **Portrait** (most important) | founder card on Home, About, link previews | **4:5 portrait**, head and shoulders, face in the upper third, at least **1200×1500 px** | Plain, light or teal-grey background, daylight, white coat optional. The frame crops with `object-fit: cover`, focused on the upper third. Start from the original of the photo on her Paziresh24 profile |
| 2 | Clinic exterior | a future Locations panel | **3:2 landscape**, the building's entrance with its signboard readable, at least 1600 px wide | It helps a patient recognise the door. Take it in daylight with no people's faces |
| 3 | Clinic interior | a future Locations or About panel | **3:2 landscape**, the waiting room or consulting room, tidy, at least 1600 px wide | No patients and no screens with patient data |
| 4 | (optional) A procedure room | a future procedures section | **3:2**, the bronchoscopy room or equipment, with no patients | Only if the hospital allows it |

The portrait needs no code change: upload it in the admin (Doctor Profile → photo). Photos 2–4 would need a small template change to place them, so ask before building.

---

## 7. What the owner must do

**On Runflare, once merged and deployed:**
1. Run `python manage.py migrate`. It applies `doctor/0003` and creates the captcha table, which the contact form needs. **Never run `collectstatic` there.**

**In the admin, as the doctor answers** ([`questions-for-doctor.md`](questions-for-doctor.md)):
2. Doctor Profile:
   - `medical_council_number` (51510, if she confirms it);
   - `practising_since` (1378, or the year behind Paziresh24's ۲۹);
   - `paziresh24_url`;
   - the photo.
3. The Amol clinic: its **`map_url`** (Neshan or Google Maps). Once it is set, the route button and the «و مسیر» labels appear.
4. Credential `detail` text, if she writes any. Check the credential years.
5. The surname, the hours, and a second location (Imam hospital, Sari), if she says so. Each is an admin edit; no layout changes.
   - The admin's own Jazzmin titles contain the surname in `config/settings/base.py`. They would need a one-line code change if the spelling changes.

**Not blocking:**
6. Choose an email provider, then set `EMAIL_*` and `INQUIRY_NOTIFICATION_EMAIL`. Until then, read Inquiries in the admin. The sidebar shows the unread count.
7. After launch, check the site on a real phone over a mobile connection (section 5, item 4).

---

## 8. Pre-launch content tasks for the doctor

Do these on the running site, before launch:

1. **Review the medical text of all 20 condition and procedure pages.** It is starter copy: the title, the short description and the body.
   - For any page she wants to expand, start each section with a line beginning `## ` (for example `## علائم`). The page then builds its own "on this page" index.
2. **Review the UI copy that speaks for the clinic or gives medical guidance:**
   - the "when to see a doctor" panel: «اگر این علائم را دارید، یا با درمان فعلی بهتر نشده‌اید…»;
   - the procedure panel: «تصمیم به انجام این اقدام پس از ویزیت و بررسی پرونده گرفته می‌شود…»;
   - **the emergency line** «در شرایط اورژانسی، مانند تنگی نفس شدید یا درد قفسه‌ی سینه، با ۱۱۵ تماس بگیرید…», which now opens that panel;
   - the contact page: «مطب در نخستین فرصت با شماره‌ای که گذاشتید تماس می‌گیرد.» This is a promise about the clinic's process, so confirm it;
   - the contact form's emergency line and its privacy hint;
   - **new in this stage:** «اگر خواندن تصویر برایتان دشوار است، با … تماس بگیرید.» and «تصویر تازه نیامد. دوباره امتحان کنید.»;
   - the copy button's «کپی نشد».
3. **Answer the open questions** in [`questions-for-doctor.md`](questions-for-doctor.md).
4. **Content suggestions from the critique** (optional):
   - «Ablation تومورهای برونکیال ریه» opens a display line with Latin. «ابلیشن (Ablation) تومورهای…» would read more evenly.
   - Several short descriptions only repeat the title (for example «برونکوسکوپی تشخیصی و درمانی»). One sentence on when it is done would help a relative compare.

---

## 9. Proposals that need your decision

Each one is optional; none is built.

| # | Proposal | Why | Cost |
|---|---|---|---|
| 9.1 | **Make the captcha friendlier to Persian keyboards:** use `captcha.helpers.math_challenge` (or digits only), accept Persian or ASCII digits in the answer, and change the hint | Both reviewers' top issue: an older patient on a Persian keyboard must switch to English letters. Digits are typed the same on both keyboards. Alternatively, drop the image and rely on the honeypot plus a time-to-submit check | small: a setting, a normaliser like `normalise_phone`, a hint text, tests |
| 9.2 | **The deferred clean-ups that touch models** (from Stage 7 simplify and this code review): a `ConditionTreated.published()` queryset; recording the photo's WebP copies at save instead of `storage.exists()` on every render; deleting old WebP copies when a photo is replaced; refusing a corrupt upload with a form error instead of a 500 | Fewer queries and file checks per page, and two admin edge cases | small to medium; model code only, no migration for the first three |
| 9.3 | **A `## ` section structure in the seeded condition texts** once the doctor reviews them | Turns on the Mayo-style "on this page" index | content only |

---

## Appendix A: critique run

- **Method:** dual-agent (A: design review · B: detector and browser evidence). The two ran isolated and in parallel, and were synthesised here.
- **Snapshot:** `.impeccable/critique/2026-11-15T20-58-43Z__templates.md`.
- **Trend:** this is the first run for this target, so there is no trend yet. The snapshot stays open, because its P1 (the captcha) remains (proposal 9.1).
- **Questions skipped:** the staged workflow ends this stage at the merge gate, so the critique's questions are carried into section 9 and the gate instead of being asked mid-stage.

## Appendix B: code-review run

The fixed point is `main` (merge-base `adada23`). The diff is source only: it excludes `public/static/`, the design screenshots, references and mockups, and `.playwright-mcp/`.

### Standards
- **Hard violations:**
  - stale hashed static copies (fixed, row 17);
  - uneven `fa_digits` on editor text (fixed, row 2);
  - hand-written digits in fixed copy (kept, section 4);
  - the surname in the Jazzmin settings (kept; owner task 5).
- **Bugs:**
  - the `fa_digits|isolate_latin` order (fixed, row 1);
  - `medicalSpecialty` / `openingHours` (kept, section 4);
  - photo save leaving orphan WebP copies, and a corrupt upload giving a 500 (deferred, proposal 9.2).
- **Smells (judgement):** deferred, section 4.

### Spec
- **Missing or partial:**
  - the "on this page" index never shows with today's bodies (by design; proposal 9.3);
  - the Stage 8 deliverables (now written).
- **Not asked for:** the copy button, the expired-form page, `MedicalProcedure`, the «۱۱۵» lines, and Jazzmin extras (all kept, section 4).
- **Implemented wrong:**
  - the flip couldn't be turned back by keyboard (fixed, row 3);
  - `fa_digits` coverage (fixed, row 2);
  - `openingHours` (kept);
  - the canonical on error pages (fixed, row 4);
  - the honeypot checked after validation (fixed, row 5).

**Summary:**
- **Standards:** 4 hard findings, 3 bugs and 6 smells. The worst was the bidi split of «COVID-19», now fixed.
- **Spec:** 2 partial, 5 additions and 5 wrong. The worst was the flip card that a keyboard user couldn't turn back, now fixed.

## The merge decision

`frontend-design` is ready to merge into `main`. **It has not been merged or pushed.** That is your call. After merging, deploy and run `migrate` on Runflare (section 7, item 1).
