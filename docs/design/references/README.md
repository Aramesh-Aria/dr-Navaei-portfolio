# Design references

These are the reference sites chosen by the owner for the frontend design (Phase 3 in [`docs/plan.md`](../../plan.md)). They were captured on 2026-11-14 with Playwright, in headless Chromium.

Each folder holds:
- `desktop-hero.jpg`: 1440×900, the first screen,
- `desktop-full.jpg`: the whole page,
- `mobile-hero.jpg` / `mobile-full.jpg`: 390×844,
- `detail-*.jpg`: close-ups of the parts the owner pointed at.

Cookie banners were declined where a decline button existed.

Stills can't show motion. For anything listed under **Motion**, visit the live site.

The owner's own words are quoted in each section, in Persian as given. The other notes are observations from the screenshots and from the computed styles measured on the live pages.

None of these sites is Persian or RTL. Every borrowed idea has to be re-made for `lang="fa" dir="rtl"` (ADR-0001), and Latin type choices don't carry over.

---

## Design references (look and feel)

### 1. Dr André van Straten (`van-straten/`)
https://drandrevanstraten.com is **the closest match to what this site is**: a single specialist, credentials first, two practice locations.

> این سایت شبیه ترین به کار ما هست. دیزاینشم بد نیست ولی خیلی ریچ هم بنظر نمیرسه. اینیمشن قسمت awards جالبه و اگر بشه تو کارمون جایی استفادش کرد باحاله.

- **Use it for structure, not looks.** The owner finds the visual design not rich enough. What to keep is the information order:
  1. the name with post-nominal degrees in the header lockup,
  2. a short "why see this kind of specialist" hero,
  3. "Conditions managed" as a top-level nav item,
  4. both practice locations named in the primary button ("Available at Cape Gate & Paarl").
- **Awards flip cards** (`detail-awards.jpg`, `detail-awards-flip-mid.jpg`, `detail-awards-flip-back.jpg`): this is **the motion the owner wants to reuse.**
  - Three dark-grey tiles in a row. Each front shows the prize and year plus the awarding society.
  - On hover the tile turns over in 3D (`rotateY(180deg)`, `backface-visibility: hidden` on the front face) and the back shows the detail: the presentation type, the congress and the paper title.
  - **Maps to our `Credential`:** the front holds `title` + `year`, the back holds `institution` and any longer detail.
  - **Fix what the original gets wrong:** it is hover-only, so touch and keyboard users never see the back. Ours must turn on tap and on focus, keep both faces readable to screen readers, and use a crossfade instead of a 3D turn under `prefers-reduced-motion`.
  - In RTL the turn direction should be mirrored.

### 2. Parsley Health (`parsley/`)
https://www.parsleyhealth.com/ is **the main reference for the overall feel.**

> این سایت ریچ تر بنظر میاد. طراحی دکمه هاش بیشتر باب میلم هست و حسی که سایت میده بهتره.

- **Feel:** warm and editorial, not clinical. A large serif headline in dark teal on a warm sand ground, a calm portrait photo bleeding off one edge, generous whitespace, and a deep teal header bar.
- **Buttons** (`detail-button-1-*`, `detail-button-2-*`), the part the owner likes most:
  - Full pills (`border-radius: 9999px`), medium-weight geometric sans at 14px, no shadow.
  - **Primary:** solid deep teal `rgb(40,72,73)`, white text, padding 8–12px × 24px. On hover it only darkens to `rgb(19,45,46)`.
  - **Secondary:** a light pill with a 2px border of the same colour. On hover the fill drops out and it becomes an outline pill.
  - Both transition colour and background only, over 150ms with `cubic-bezier(0.4, 0, 0.2, 1)`. They are quiet, with no movement and no glow.
- **Motion:** almost none beyond accordions. The richness comes from type, colour and photography, not animation.

### 3. Tia (`tia/`)
https://asktia.com/

> دکمه ها و انیمیشن های این سایت جالبه و طراحی مدرنی داره.

- **Buttons:**
  - Primary: a coral pill (`rgb(246,84,74)`, radius 90px, padding 15×35px, bold grotesque 16px) that shifts to pink on hover, `all 0.3s ease-in-out`.
  - Secondary: a cream pill with no border.
  - In the hero, the two pills sit side by side under a check-mark list of benefits.
- **Feel:** a serif display headline with one italic word for emphasis ("care for *women*"), a cream and sand palette, and a split hero: text on one side, an interior photo on the other.
- **Motion:** content blocks slide up as they scroll into view (`slide-up` classes). Watch it live.

### 4. Shafer Plastic Surgery (`shafer/`)
https://www.shaferplasticsurgery.com/

> دکمه ها و انیمیشن های این سایت جالبه و طراحی مدرنی داره.

- **Use it for the sense of expense only.** It is an aesthetic-surgery clinic, and its tone (beauty, "the art of") is wrong for an internist. Borrow the craft, not the voice.
- **Buttons:**
  - "Contact Us" (`detail-button-1-*`): a solid black pill with a Playfair Display label. On hover it **inverts** to a white pill with a thin black outline and black text.
  - "Request an Appointment" (`detail-button-2-*`): a floating slate-blue tab pinned to the bottom corner with an arrow, present on every scroll position. **This maps to an always-reachable contact path** (on mobile, tap-to-call).
- **Feel:** a full-bleed dark video hero, a high-contrast serif with one italic word ("The *Art* Of"), small tracked uppercase sublines, and a slate and white palette. Never letter-space Persian, though: tracking breaks the joins.
- **Motion:** many images animate in on scroll (`img-with-animation`, 42 of them), there are layered parallax-tilt image cards (`parallaxImg`), and slide-out panels and a Flickity carousel for testimonials. Watch it live, and pick one or two of these at most. The whole set is more than a doctor's site needs.

---

## Content references (what to say and how to structure it)

### 5. Mayo Clinic, condition page (no folder)
https://www.mayoclinic.org/diseases-conditions/asthma/symptoms-causes/syc-20369653 is **the model for our condition detail page** (`/conditions/<slug>/`).

> این سایت هم برای الگوی ساخت صفحه جزییات بیماری جالبه.

Mayo blocks headless browsers, so there are no screenshots. Its page structure was read in the in-app browser:

- **Section order:** Overview → Symptoms → When to see a doctor (split into "Seek emergency treatment" and "Contact your doctor") → Causes / triggers → Risk factors → Complications → Prevention → Associated procedures → Related content.
- **An "On this page" index** at the top, so a long page stays scannable.
- **"When to see a doctor"** is what turns an information page into a contact. On our site it should lead straight to the clinic phone numbers.
- **"Associated procedures"** links a condition to the procedures used for it, for example lung cancer → bronchoscopy, or pleural disease → pleural catheter. Our model doesn't support this yet; see "Backend gaps" below.

**Our `ConditionTreated.body` is one free-text field today**, and the seeded bodies are one or two sentences. A Mayo-style page needs either structured sections or a body format that supports headings. This is a Phase 3 decision to propose, not build.

### 6. Digestive Health UK (`digestive-health-uk/`)
https://digestivehealthuk.com was added by Claude as a content reference.

> دو سایت دیگه رفرنس محتوا که گفتی دقیقا نفهمیدم از چیشون میخوایم رفرنس بگیریم ولی اگر بدرد میخورن اینارم به عنوان رفرنس اضافه کن.

Its visual style (bright blue and cyan, dotted shapes) is **not** a reference. Two patterns are:

- **The founder card in the hero:** the doctor's photo with the full name and post-nominal degrees on it, as the first thing on the page. For a site whose first job is "confirm her credentials", the doctor's face and titles belong above the fold.
- **Navigation by what the patient has, not by what the clinic sells:** Symptoms / Conditions / Tests / Treatments as separate menus. This matches our two categories, Conditions Treated and Procedures Performed, and supports the decision to list them as two labelled groups.
- **The phone number in the header** at all widths ("For private consultation call …").

The second content site, Chahal Cardiovascular Centre, was **dropped**. Its page is a generic stock-photo template and showed nothing the other references don't show better.

### 7. The doctor's Paziresh24 profile (`paziresh24/`)
https://www.paziresh24.com/dr/دکتر-سپیده-صفاءنوائی/

> این صفحه ی پذیرش ۲۴ دکتر ما هستش.

This is **not a design reference.** It is where many of her patients already find her, and it shows what an Iranian patient expects to see at once:

- years of experience ("۲۹ سال تجربه"),
- the medical council number (کد نظام پزشکی), which Iranian patients use to verify a doctor,
- a star rating with a count (4.3 of 5, 43 reviews),
- the address, landline and mobile, and a map / route link,
- a way to book (an internet appointment through "دکترتو").

Patient reviews there **must not be copied** onto our site. We have no consent to republish them, and testimonials are out of v1 scope. A link out to the profile ("نظرات بیماران در پذیرش۲۴") is the honest way to borrow that trust.

---

## Data that disagrees with our seeds (confirm with the doctor before Phase 3)

The Paziresh24 profile contradicts or extends what we seeded in Phase 2:

| Item | Our seed | Paziresh24 |
|---|---|---|
| Spelling of the surname | صفانوایی | **صفاءنوائی** |
| Clinic hours | «پذیرش بیماران: روزانه، شیفت عصر» | **«ویزیت عصر ۳ روز هفته»** |
| Second location | none (open question in `plan.md`) | **Sari mornings: inpatients at Imam hospital, Sari** (بیماران بستری بیمارستان امام ساری) |
| Medical council number | not in the model | **51510** |
| Experience | not in the model | 29 years |

The spelling matters for search: patients may search either form. The surname should be confirmed, and the other spelling can be kept in page metadata.

## Backend gaps these references expose (proposals only, not approved)

- `DoctorProfile.medical_council_number`, shown next to her name as a verifiable credential.
- `DoctorProfile.paziresh24_url` (or a general "external profile" link) for reviews and booking. Linking out is not the same as building booking, which stays out of scope.
- `Credential.detail`: longer text for the back of a flip card (the van Straten pattern).
- A link from a condition to its related procedures (Mayo's "Associated procedures").
- Structured sections on the condition page, or a body that allows headings (Mayo's section order).
