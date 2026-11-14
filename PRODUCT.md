# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Django 5.2, server-rendered templates, SQLite, hosted on Runflare (ADR-0002, ADR-0003). The frontend CSS/JS approach (Tailwind standalone CLI vs plain modern CSS with small vanilla JS) is **undecided**: Stage 2 of `docs/DESIGN_PROMPT.md` recommends one and the owner approves it. Node.js is not available in production builds; no JS framework.

## Users

- **The patient who already has her name.** Referred by another doctor or by word of mouth, often older. They want to confirm she is who they were told she is (qualifications, experience) and then call the clinic.
- **The relative researching for a parent.** A son or daughter on a phone, checking credentials and finding the phone number, address and hours on the parent's behalf.
- **The searcher who doesn't know her yet.** Someone in or near Amol searching for an internist or lung specialist, or for a condition (asthma, COPD, diabetes, bronchoscopy).
- **The Content Editor** (the site's builder, and the doctor's non-technical daughter) maintains all content through the Django admin, never through templates.

## Product Purpose

The public website of Dr. Sepideh Safanavaei (دکتر سپیده صفانوایی), an internal medicine specialist subspecialised in pulmonology, at `dr.safanavaiee.ir`.

- **Primary job: credibility.** A visitor confirms her credentials and finds how to reach her.
- **Secondary job: light organic reach** for internal medicine and lung searches in Amol.
- **Success** is a patient contacting the clinic: mostly by phone (landline or mobile), then the contact form (Inquiry), then walking in with the address and map link. Every page offers that path and never pushes.

## Positioning

Lead with pulmonology (owner decision, 2026-11-14): a lung subspecialist, including interventional pulmonology (bronchoscopy, pleuroscopy, airway stents, tumour ablation, pleural catheters), who is also a full internist.

What a neighbouring doctor could not truthfully copy:
- internal medicine since 1378, then pulmonology and ICU subspecialty at Masih Daneshvari (1387), then a further interventional pulmonology fellowship there (1390–1395),
- eight years heading the Amol diabetes unit at Imam Reza hospital, which became one of Iran's top five referral diabetes centres,
- faculty at Mazandaran University of Medical Sciences since 1395,
- ERS, ATS and Iranian Thoracic Society member since 1387, 30+ papers and 2 books,
- an Amol native who returned to practise in her own city.

## Operating Context

- Iranian patients expect to find, at once: years of experience, the medical council number (used to verify a doctor), the address with a map/route link, both phone numbers, and the hours. Many already know her through her Paziresh24 profile.
- Visitors are mostly on phones, often on slow or filtered connections inside Iran: the site must be light and must not depend on foreign CDNs.
- Content is maintained by a non-technical editor through the admin.

## Capabilities and Constraints

- Public pages: `/`, `/about/`, `/conditions/`, `/conditions/<slug>/`, `/locations/`, `/contact/`. Admin at `/admin/`.
- Domain terms (CONTEXT.md): Doctor Profile, Condition Treated, Procedure Performed, Clinic Location, Inquiry, Content Editor. Avoid "Service", "Specialty", "Branch", "Office", "Lead", "Submission".
- Farsi only, `lang="fa" dir="rtl"`, no i18n (ADR-0001). Embedded Latin terms (COPD, ERS, ATS, ICU, Ablation) are wrapped to render LTR. Persian digits in displayed text; `tel:` links keep ASCII digits.
- 1 to N Clinic Locations, addable from the admin alone. One today (Amol).
- Contact form has no medical-detail field, by design. Email notification is optional and never blocks saving.
- Out of scope: online booking/calendar, blog, testimonials, FAQ, analytics, English, structured per-day hours. A link out to her Paziresh24 profile is allowed as a proposal.
- **Undecided** (owner answers at the Stage 2 gate): surname spelling (صفانوایی vs صفاءنوائی), clinic hours wording, whether Imam hospital in Sari is a patient-facing location, showing the medical council number (51510), the email provider.

## Brand Commitments

- **Logo is a binding brand asset** (owner decision, 2026-11-14): `public/static/assets/img/icon.jpg`, 1080×1080. A circular badge: a dark teal line-drawn pair of lungs with branching airways, a gold stethoscope arcing around them, the name in Nastaliq «دکتر سپیده صفانوایی», then "Dr. Sepideh Safa Navaei" and "PULMONOLOGIST" in Latin, inside a teal ring with a gold inner ring. Its teal and gold are the starting point for the palette. The favicons are cut from it. Only a raster version exists (no SVG).
- **Voice: formal, third person** (owner decision, 2026-11-14), as in the bio: «دکتر صفانوایی…», «ایشان…». Respectful and calm; never salesy.
- Feel references chosen by the owner: Parsley Health for the overall warmth; van Straten's flip card for credentials (see `docs/design/references/README.md`).

## Evidence on Hand

- Real seeded content (migrations `0002_seed_profile`, `0002_seed_location`, `0003_seed_conditions`): the full six-paragraph bio, a tagline, 8 credentials, 15 Conditions Treated, 5 Procedures Performed, the Amol clinic with landline and mobile.
- The logo and favicons in `public/static/assets/img/` (untracked today).
- **No photography of any kind yet**: no doctor portrait (a neutral placeholder SVG stands in), no clinic photos. Never substitute stock people for the doctor.
- **No testimonials, ratings or patient reviews** may appear on the site. Paziresh24 reviews may only be linked to, never copied.
- Condition bodies are starter copy for the doctor to review; they are one or two sentences each.

## Product Principles

1. **Proof before persuasion.** Her qualifications, history and contact details do the convincing; the site never makes claims beyond them.
2. **The phone is always one tap away.** Every page offers the call, the address and the form, quietly.
3. **Legible for a 60-year-old on a phone.** Comfort and clarity win over density and novelty.
4. **Editable by a non-technical person.** Anything that may change lives in the admin, and the layout survives whatever she types.
5. **Honest with what we have.** Complete and dignified without photos or long content; better when they arrive.

## Accessibility & Inclusion

WCAG AA contrast, full keyboard navigation with visible focus, semantic landmarks, correct `lang`/`dir`. Body text 18px or more on phones. `prefers-reduced-motion` respected. Older users and relatives on phones are the core audience.
