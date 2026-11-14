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
| 3 | Foundation (branch, approved backend changes, tokens, `base.html`) | ⬜ next | **required:** approve the shell |
| 4 | Home and About (credential flip cards) | ⬜ | **required:** confirm the direction holds |
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

**Stage 3 (Foundation) is next.**
- Start from `main` once Stage 2 is committed, then create the `frontend-design` branch.
- The gate is passed: build with the seeds.

Decided, and to build:
- **Direction A «چادرشب».** Tokens, type, imagery and motion are in [`01-direction.md`](01-direction.md) §2. The page inventory is in §6. Fonts are Lalezar + Vazirmatn, self-hosted as subset woff2.
- **Backend fields, test-first with migrations:**
  - `DoctorProfile.medical_council_number`, `practising_since` (Solar Hijri year) and `paziresh24_url`, all blank allowed;
  - `Credential.detail`, optional text;
  - the `## ` section filter for `ConditionTreated.body` (a template filter, no model change).
  - Add the new terms to `CONTEXT.md` through `domain-modeling`.
  - **Not** the condition↔procedure links.
- **Stack:** plain modern CSS + small vanilla JS, with **no hard refresh ever needed**:
  - hashed static names,
  - `Cache-Control: no-cache` on HTML,
  - `whitenoise.runserver_nostatic` and `WHITENOISE_MAX_AGE = 0` in dev,
  - tests for both.
- **Images:**
  - Pillow processing of the uploaded photo (1200 and 600 px WebP);
  - the lungs-mark placeholder;
  - an SVG trace of the lungs;
  - fix `site.webmanifest`.
- **The django-jazzmin admin,** set up like ArameshMusicAcademy-website: see `docs/plan.md` "Admin theme" and `DESIGN_PROMPT.md` Stage 3 step 5.

What to reuse and what to leave:
- The mockups (`mockups/*.html`, `mockup.js`) are throwaway. Rebuild from the tokens.
  - Reproduce `mockup.js`'s flip behaviour and the reduced-motion CSS.
  - `mockups/assets/lungs-*.png` is the interim mark until the SVG trace exists.
- Already settled before this stage:
  - media is served by `config/urls.py` at `/public/media/`;
  - static goes through WhiteNoise from `static_dev/`;
  - the manifest storage is `config/storage.py`.

Pending, but not blocking:
- The doctor's answers ([`questions-for-doctor.md`](questions-for-doctor.md)). Record them under Decisions when they arrive.
- The medical review of the condition texts, before launch.
- The email provider.

Tooling: the Playwright MCP server connected in Stage 2. Node v26 is available locally if a tool needs it.
