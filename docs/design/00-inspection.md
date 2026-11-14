# Stage 1: Inspection

Read-only survey of what the frontend has to work with, done on 2026-11-14 from `main` at `dc00ede`.

Contents:
1. [Product context](#1-product-context)
2. [Frontend today](#2-frontend-today)
3. [Content inventory](#3-content-inventory) (every field the site can show, and where it comes from)
4. [Backend facts the frontend depends on](#4-backend-facts-the-frontend-depends-on)
5. [Edge cases the design must survive](#5-edge-cases-the-design-must-survive)
6. [Reference motions, named](#6-reference-motions-named)
7. [Other findings for Stage 2](#7-other-findings-for-stage-2)

---

## 1. Product context

`/impeccable init` wrote [`PRODUCT.md`](../../PRODUCT.md) at the repo root. It holds the users, purpose, positioning, constraints and evidence. Three facts came from the owner during init and are new:

- **The logo is a binding brand asset.** `public/static/assets/img/icon.jpg` (1080×1080, raster only): a dark teal line-drawn pair of lungs, a gold stethoscope arcing around them, the name in Nastaliq, "Dr. Sepideh Safa Navaei" and "PULMONOLOGIST" in Latin, inside a teal ring with a gold inner ring. Its teal and gold are the palette's starting point.
- **Voice: formal, third person**, as in the bio («دکتر صفانوایی…», «ایشان…»).
- **Lead with pulmonology.** Internal medicine and diabetes are clearly present, but second.

## 2. Frontend today

**There is no public frontend.**
- `config/urls.py` routes only `admin/`.
- Every `apps/*/views.py` is the empty Django stub.
- There is no `templates/` folder (it is already listed in `TEMPLATES["DIRS"]`), no project `static/` folder, no CSS and no JS.
- The only static file in an app is `apps/doctor/static/doctor/doctor-placeholder.svg`.

**The admin** is Django's stock admin, untouched. With `LANGUAGE_CODE = "fa"` its chrome is already Persian and RTL. Its look stays as it is.

| Admin page | What the Content Editor gets |
|---|---|
| Doctor Profile | Singleton: "add" is refused once a row exists, and the list view redirects to the one profile. Credentials are edited in a `TabularInline` on the same page (`title`, `institution`, `year`, `order`, one empty row). |
| Conditions | One list for both categories: columns title, category, slug, published, order. `is_published` and `order` are editable in the list, there is a category filter and search. Slugs are typed by hand (Latin only; not prepopulated from the Persian title). |
| Clinic Locations | List of name, phone, order (order editable in the list). |
| Inquiries | Read-only (no add; the patient's fields can't be changed). Only `is_read` is editable. Newest first. The honeypot `website` field is hidden from the form. |

## 3. Content inventory

### 3.1 Doctor Profile (`apps.doctor.DoctorProfile`, singleton)

| Field | Type / rules | Seeded value | Where the site shows it |
|---|---|---|---|
| `full_name` | required, max 200 | «دکتر سپیده صفانوایی» (the title «دکتر» is **part of the field**) | header lockup, founder card, `<title>`, schema.org `Physician.name` |
| `intro_tagline` | **optional**, max 200 | «متخصص داخلی و فوق تخصص بیماری‌های ریه» | Home hero, header degrees line, meta description |
| `bio` | required, free text | 6 paragraphs, 1,177 characters, split by `\n\n`. Already uses Persian digits (۱۳۷۸…) and Latin acronyms in parentheses («(ERS)», «(ATS)», «ICU») | About page |
| `photo` | **optional** image, `upload_to="doctor/"`, no size or aspect rules, never processed | empty | founder card, About, Open Graph image |
| `photo_url` | property | the placeholder SVG `static/doctor/doctor-placeholder.svg` (400×400, pale blue-grey `#e6eef3` with a `#9fb4c2` silhouette) until a photo is uploaded | always use this, never `photo.url` |

What the bio says, paragraph by paragraph (each paragraph is a natural section of the About page):
1. Internal medicine 1378; two years' service in deprived Kohgiluyeh; returned to Amol; 8 years heading the Amol diabetes unit at Imam Reza hospital.
2. The Amol diabetes centre became one of Iran's top 5 referral centres and was repeatedly commended for world-standard care.
3. Pulmonology subspecialty at Shahid Beheshti, 1385; two years at Masih Daneshvari; returned to Amol in 1387 with pulmonology and ICU.
4. 1390: five more years at Masih Daneshvari for interventional pulmonology.
5. Faculty at Mazandaran University of Medical Sciences since 1395 (mornings); private clinic in Amol, daily, evening shift, for internal, diabetes and lung patients.
6. ERS, ATS and Iranian Thoracic Society member since 1387; 30+ papers and 2 books.

**Derivable numbers** (for the "at a glance" facts patients expect): practising since 1378 (about 27 years by 1405; Paziresh24 says «۲۹ سال تجربه», so the figure needs confirming before it is shown), 8 years heading the diabetes unit, 30+ papers, 2 books. None of these are fields; showing them means either hardcoding (forbidden for content) or a new field (a Stage 2 proposal).

### 3.2 Credentials (`apps.doctor.Credential`, inline under the profile)

Fields: `title` (required, max 200), `institution` (optional, max 200), `year` (optional, **Solar Hijri** integer), `order`. Ordering: `order`, then `-year`.

| order | year | title | institution |
|---|---|---|---|
| 10 | 1378 | متخصص داخلی | دانشگاه علوم پزشکی شهید بهشتی، تهران |
| 20 | 1387 | فوق تخصص بیماری‌های ریه و ICU | دانشگاه علوم پزشکی شهید بهشتی - بیمارستان مسیح دانشوری |
| 30 | 1395 | دوره تخصصی اینترونشن ریه | بیمارستان مسیح دانشوری |
| 40 | 1395 | هیات علمی | دانشگاه علوم پزشکی مازندران |
| 50 | 1387 | عضو انجمن علمی ریه اروپا (ERS) | — |
| 60 | 1387 | عضو انجمن علمی ریه آمریکا (ATS) | — |
| 70 | 1387 | عضو انجمن علمی ریه ایران | — |
| 80 | — | بیش از ۳۰ مقاله علمی و ۲ کتاب در مجلات معتبر خارجی | — |

Two kinds of credential live in one list: **qualifications/posts** (rows 10–40, all with an institution) and **memberships/output** (rows 50–80, none with an institution). **Half the cards have nothing for the back of a flip card** (see 5.2).

### 3.3 Conditions Treated and Procedures Performed (`apps.conditions.ConditionTreated`)

Fields: `category` (`condition` «بیماری» / `procedure` «اقدام درمانی»), `title` (max 200), `slug` (unique, Latin), `short_description` (max 300), `body` (required, free text), `order`, `is_published`. Ordering: `order`, `title`. **Only `is_published=True` rows are public.** All 20 seeded rows are published.

The site shows them as two labelled groups: **Conditions Treated (15)** and **Procedures Performed (5)**.

| Group | Seeded titles, in order |
|---|---|
| Conditions | آسم · COPD (بیماری انسدادی مزمن ریه) · بیماری‌های شغلی ریه · بیماری‌های ریوی ناشی از سیگار · بیماری‌های عفونی ریه · برونشیت · حساسیت‌های ریوی · فیبروز ریه · بیماری‌های روماتیسمی ریه · کانسرهای ریه · بیماری‌های پرده پلور · تنگی نفس · سرفه مزمن · دیابت · بیماری‌های گوارشی |
| Procedures | برونکوسکوپی · پلوروسکوپی · استنت راه هوایی ریه · Ablation تومورهای برونکیال ریه · تعبیه کاتتر پلور |

Shape of the content:
- Titles: 3 to 30 characters today (the field allows 200).
- Bodies: 72 to 176 characters, one or two sentences each. Starter copy, awaiting the doctor's review.
- The 15 conditions are three natural clusters, though the model doesn't record them: lung diseases (11), symptoms (تنگی نفس، سرفه مزمن), and internal medicine (دیابت، بیماری‌های گوارشی). Diabetes, her eight-year specialty, sits 14th of 15 by `order`.
- Some bodies point at a procedure in prose (lung cancer → bronchoscopy, pleural disease → pleural catheter), but there is no link in the model.
- Some bodies name the doctor («دکتر صفانوایی»), so the surname question touches content as well as templates.

### 3.4 Clinic Locations (`apps.locations.ClinicLocation`)

| Field | Rules | Seeded (Amol) |
|---|---|---|
| `name` | required, max 200 | مطب آمل |
| `address` | required, free text | آمل، سبزه میدان، روبروی مخابرات مرکزی، ساختمان پزشکان آنیتا، طبقه اول، واحد ۳ |
| `phone` | required, max 50, free text | `01144229270` (ASCII digits, no separators) |
| `mobile_phone` | optional | `09119970828` |
| `map_url` | optional URL | **empty** |
| `hours` | required, free text (may be multi-line) | پذیرش بیماران: روزانه، شیفت عصر |
| `order` | | 0 |

One location today. **The seeded clinic has no map link**, so the "no map link" edge case is the live state, not a hypothetical.

### 3.5 Inquiry (`apps.inquiries.Inquiry`, contact form)

| Field | Rules | On the form |
|---|---|---|
| `name` | required, max 200 | yes |
| `phone` | required, max 50, no validation today | yes; normalise Persian digits, spaces and dashes (Stage 6) |
| `preferred_contact_time` | optional, max 200, free text | yes |
| `message` | optional | yes |
| `website` | honeypot, `editable=False` | hidden; a filled value drops the submission silently |
| `created_at`, `is_read` | system | no |

No medical-detail field, by design. 0 inquiries in the dev database.

### 3.6 Static assets

- `apps/doctor/static/doctor/doctor-placeholder.svg`: tracked.
- `public/static/assets/img/`: **untracked** (`public/` is gitignored), so lost on deploy: `icon.jpg` (the logo, 1080², 124 KB), `favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png`, `apple-touch-icon.png`, `android-chrome-192x192.png` (59 KB) and `-512x512.png` (286 KB), and `site.webmanifest`.
- `site.webmanifest` is broken: empty `name` and `short_name`, white `theme_color`, and icon paths at the site root (`/android-chrome-192x192.png`) that won't exist under `/public/static/…`.
- No fonts, no photos, no illustrations.

### 3.7 Who shows what, at a glance

| Page | Draws from |
|---|---|
| every page (header, footer, contact tab) | `DoctorProfile.full_name`, `intro_tagline`; every `ClinicLocation` (name, address, phones, hours, map link) |
| `/` | profile (name, tagline, `photo_url`), a selection of credentials, published conditions and procedures (a subset), locations summary |
| `/about/` | `bio` (6 paragraphs), all credentials, `photo_url` |
| `/conditions/` | published rows, grouped by `category`: `title`, `short_description` |
| `/conditions/<slug>/` | one published row: `title`, `short_description`, `body`; plus locations and phones for "when to see a doctor" |
| `/locations/` | all locations, every field |
| `/contact/` | Inquiry form; locations and phones beside it |

## 4. Backend facts the frontend depends on

**Settings**
- `config/settings/dev.py`: `STATIC_URL = "static/"`, no `STATIC_ROOT`, no `STATICFILES_DIRS`. `MEDIA_URL = "/media/"`, `MEDIA_ROOT = BASE_DIR / "media"`, but **no URL pattern serves media in dev**, so an uploaded photo would 404 locally until one is added. Email goes to the console.
- `config/settings/prod.py`: `STATIC_URL = "/public/static/"`, `STATIC_ROOT = "/app/public/static"`, `MEDIA_URL = "/public/media/"`, `MEDIA_ROOT = "/app/public/media"` (ADR-0003). No WhiteNoise. SSL redirect and secure cookies on. Email is the dummy backend unless `EMAIL_HOST` is set.
- **`INQUIRY_NOTIFICATION_EMAIL` is defined only in `prod.py`**, not in `base.py`. Stage 6 must read it with `getattr(settings, "INQUIRY_NOTIFICATION_EMAIL", "")` or move it into `base.py`.
- `LANGUAGE_CODE = "fa"`, `TIME_ZONE = "Asia/Tehran"`, `USE_I18N = True`. There is no context processor for site-wide data yet: the header and footer will need one (or an inclusion tag) for the profile and the locations.
- Dependencies: Django 5.2.17, Pillow, python-dotenv. Nothing for the frontend.

**Tests:** 25, all passing (`venv/bin/python manage.py test apps`). They cover:
- the singleton admin (add allowed once, list redirects, credentials inline), credential ordering,
- the seeds (profile, tagline, 8 credentials, 15 + 5 conditions, all published, bronchoscopy is a procedure, Amol clinic with both phones),
- `photo_url` (placeholder vs upload),
- conditions (default category, ordering, category split, unique slug),
- locations (a second one addable from the admin, ordering, mobile and map link optional),
- inquiries (no add from admin, fields read-only, honeypot hidden, newest first).

None cover a public URL, since none exist.

**Dev database = seeds.** The dev `db.sqlite3` matches the seed migrations exactly: no admin edits yet, no photo, all rows published, one location.

## 5. Edge cases the design must survive

### 5.1 Long and mixed-direction text
- **A title that starts with Latin:** «Ablation تومورهای برونکیال ریه», and «COPD (بیماری انسدادی مزمن ریه)». With `dir="auto"` or a first-strong-character rule these would render LTR. Every container must keep `dir="rtl"`, and the Latin run must be isolated (`<bdi>` or `<span dir="ltr">`), or the parenthesis and word order break.
- **Latin in parentheses inside Persian:** «(ERS)», «(ATS)», «ICU» in credentials and in the bio. The bio is free text typed in the admin, so wrapping can't be done by hand: it needs a template filter that wraps Latin runs automatically.
- **Titles at the field limit:** 30 characters today, 200 allowed. Cards and nav must wrap gracefully, never truncate a medical term.
- **The six-paragraph bio** (1,177 characters, `\n\n` breaks) must not become a wall.
- **Empty `intro_tagline`:** the hero, the header degrees line and the meta description each need a fallback that doesn't leave a hole.
- **Persian digits already present** in typed text (the bio, a credential title): the digits filter must be idempotent and must not touch ASCII inside URLs, `tel:` values or slugs.
- **`hours` is free text** and may span lines: preserve line breaks.

### 5.2 Missing pieces
- **No photo:** the placeholder is a pale blue-grey generic silhouette, the wrong temperature for a warm palette and visibly "stock avatar". The design should frame it so it looks intentional, or Stage 2 should propose a better placeholder (the logo mark, a monogram).
- **A real photo of unknown size and aspect**, not processed: portrait, square or landscape, maybe 4000 px wide and several MB.
- **A credential with no institution** (4 of 8) and **with no year** (1 of 8): the flip card's back would be empty. Either those cards don't flip, or the back shows something else. A card with neither year nor institution is title-only.
- **Shared years:** three credentials in 1387, two in 1395, so year can't be a unique visual key.
- **A location with no mobile and no map link** (the map link is missing on the real clinic today).
- **Zero published procedures** (the editor unpublishes all five): the second group and any "procedures" nav entry must disappear, not render empty.
- **Zero published conditions**, and a condition with a one-sentence body (all of them today).
- **An unpublished condition reached directly by URL** must 404.
- **Zero Clinic Locations** (all deleted in the admin): header phone, footer, contact tab and schema.org must degrade without errors.

### 5.3 Several locations and the contact form
- **Two or three Clinic Locations**, for example Amol plus Imam hospital Sari (mornings, inpatients), with different hours and possibly no mobile. One location must not look like a lonely card in a grid built for three; the header phone and the floating contact tab must choose sensibly between several phones.
- **A long location name or address** (both free text).
- **The contact form phone typed as** «۰۹۱۱ ۹۹۷ ۰۸۲۸», «0911-997-0828», «+98 911…», or with Arabic-Indic digits «٠٩١١…». All normalise to ASCII before saving; errors are in clear Persian.
- **The honeypot filled:** silent drop, same success page.
- **Email unset or failing:** the Inquiry is still saved and the patient still sees success.

## 6. Reference motions, named

Measured on the live sites on 2026-11-14 in the in-app browser (the Playwright MCP server failed to connect this session; the stills in `references/` were already captured). Names follow the `animation-vocabulary` glossary.

| Site | What happens | Name | Measured |
|---|---|---|---|
| van Straten, Awards | A dark tile turns over on hover and shows text on its back | **3D tilt / Flip**, with **Perspective** | Webflow IX2 "Card Flip": `rotateY(180deg)` on `.card-wrapper`, 800 ms in; "Card Flips Hover Out" back to 0°, **1000 ms out** (slower out than in). Easing field empty in the IX2 config. `perspective: 1200px`. Front `backface-visibility: hidden`, `#595B60` fill; back pre-rotated `rotateY(180deg)` with a **white** fill, 30 px padding, 14 px text. Triggers are `MOUSE_OVER` / `MOUSE_OUT` only: no click, tap or focus, so touch and keyboard users never see the back. |
| van Straten, accordions | Accordion opens, chevron turns | **Accordion / Collapse** + **Rotate** | 500 ms, height and a 180° icon turn |
| Parsley, buttons | Primary darkens; secondary drops its fill to become an outline | **Hover effect** (colour-only) | `background-color`/`color`/`border-color` over 150 ms, `cubic-bezier(0.4, 0, 0.2, 1)`. No movement. Pills: `border-radius: 9999px`. |
| Tia, content blocks | Blocks rise 10 px and fade in as their section enters the viewport, one after another | **Scroll reveal** = **Fade in** + **Translate**, with **Stagger** | `.animate.slide-up` `translateY(10px)` → `0` and `opacity 0 → 1` when a parent gets `.is-visible`; `transition: 0.3s ease-in-out`, delay classes `d2` = 400 ms, `d3` = 600 ms (200 ms steps). |
| Tia, buttons | Coral primary shifts toward pink | **Hover effect** | `all 0.3s ease-in-out`. Measured header button radius 8 px; the hero pills are fully round. |
| Tia, other | Logo strip scrolling forever; a floating table of contents sliding in on articles | **Marquee**; **Slide in** + **Fade in** | marquee 70 s linear on mobile; TOC enters with `translateX(-12px)` + opacity |
| Shafer, "Contact Us" | Black pill turns into a white pill with a thin black outline and black text | **Hover effect**, an invert | transitions over 450 ms, `cubic-bezier(0.25, 1, 0.33, 1)` (a strong **ease-out**), fill drawn by a `::before` layer |
| Shafer, "Request an Appointment" | A slate tab fixed to the bottom corner on every scroll position; on hover it turns white and its label inverts | **Hover effect** on a fixed element (no entrance motion) | `position: fixed; right: 20px; bottom: 20px; border-radius: 12px`, `rgb(93,122,137)`, 400 ms `cubic-bezier(0.61, 0.24, 0.41, 0.87)`; label `filter: invert(1)`. **Hidden on mobile** (`mob-display-none`): ours must do the opposite and matter most on phones (tap-to-call). |
| Shafer, images | Images appear as they scroll in, some growing, some flipping in from 25°, some sliding 20% from the side or 100 px from below | **Scroll reveal** variants: **Scale in**, **3D tilt / Flip**, **Slide in** | `opacity 0.5s`; `rotateY(25deg)` + opacity 1 s for flip-in; `translateX(±20%)`; `translateY(100px)`. 42 such images on the home page. |
| Shafer, image cards | Layered cards that tilt toward the cursor | **3D tilt** following the pointer (with **Parallax** between layers) | `parallaxImg` |
| Shafer, testimonials | Flickity carousel | (carousel; testimonials are out of scope) | |

What this tells Stage 2:
- The flip is the only motion the owner asked for by name. The original's 1000 ms un-flip is slow enough to feel laggy; ours should be **interruptible**, with a faster exit.
- Its back face is white on a page with a white ground, so mid-turn the card seems to vanish (`detail-awards-flip-back.jpg`). Ours needs a filled back.
- Parsley's quiet 150 ms colour-only hover is the button baseline. Shafer's invert is the only richer hover candidate.
- Tia's reveal (10 px, 300 ms) is the quiet end of scroll motion; Shafer's (100 px, 20%, 25° flips) is the loud end and is what "AOS fade-up everywhere" looks like.

## 7. Other findings for Stage 2

- **A real portrait already exists publicly.** Her Paziresh24 profile shows a head-and-shoulders photo of her (`references/paziresh24/mobile-hero.jpg`). We can't lift it from there, but the owner can ask the doctor for that original: the shot list should start from it.
- **Logo issues to weigh** (the logo is binding, these are about how to use it):
  - raster only (1080² JPEG), so it needs a vector redraw or a careful crop for the header at small sizes,
  - it reads "PULMONOLOGIST" only, though she is also an internist (consistent with "pulmonology first"),
  - its stethoscope is the "stethoscope" cliché the brief warns against; the lungs-with-airways drawing is the stronger, more specific motif,
  - its Latin spelling is "Safa Navaei", while the domain is `safanavaiee` and Paziresh24 uses صفاءنوائی: the spelling question touches the logo too.
- **Paziresh24 formats the landline as** «۰۱۱-۴۴۲۲۹۲۷۰»: Persian digits, area code split by a dash. That is the format Iranian patients recognise; ours should display the same way while `tel:` keeps `+981144229270`-style ASCII.
- **Clinic hours appear in the bio text too** («روزانه در شیفت عصر»), so answering the hours question means editing the bio in the admin, not only the location.
- **Credential years are Solar Hijri.** Display as is (with Persian digits). If schema.org needs dates, convert or omit them.
- **No context processor or inclusion tag yet** for data shown on every page (profile, locations).
- **Latin-wrapping filter needed**, alongside the Persian-digits filter, because Latin terms arrive inside admin-typed free text.
