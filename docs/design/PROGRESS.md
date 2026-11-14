# Design progress

This is the handoff file between chats. Each chat does the first stage below that isn't done, following [`docs/DESIGN_PROMPT.md`](../DESIGN_PROMPT.md). At the end of the stage, the chat updates this file and writes a commit message in chat. Chats never commit: the owner commits each stage before opening the next chat.

Kickoff line for every new chat:

> Read `docs/DESIGN_PROMPT.md` and `docs/design/PROGRESS.md`, then do the next stage.

## Stages

| # | Stage | Status | Gate |
|---|---|---|---|
| 0 | References (done before this workflow) | ✅ done 2026-11-14 | owner picked the sites |
| 1 | Inspection | ✅ done 2026-11-14 | — |
| 2 | Direction and mockups | ⬜ next | **required:** choose a direction, answer the proposals and content questions |
| 3 | Foundation (branch, approved backend changes, tokens, `base.html`) | ⬜ | **required:** approve the shell |
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

## Open questions for the owner

These are answered at the Stage 2 gate. Record each answer under Decisions.

- Surname spelling: صفانوایی (our seeds) or صفاءنوائی (Paziresh24)?
- Clinic hours: «روزانه، شیفت عصر» or «ویزیت عصر ۳ روز هفته»?
- Is Imam hospital in Sari (mornings, inpatients) a patient-facing second Clinic Location?
- Show the medical council number (51510)?
- Email provider for Inquiry notifications (not blocking).
- Years of experience to show: Paziresh24 says ۲۹, the bio implies about ۲۷ (since 1378). Which, and as a field or not?
- Can we get the original of the portrait on her Paziresh24 profile?

## Handoff to next stage

**Stage 2** starts from `main` once Stage 1 is committed. Read [`00-inspection.md`](00-inspection.md) and [`PRODUCT.md`](../../PRODUCT.md).

- The full content inventory, the edge-case list and the measured reference motions are in `00-inspection.md`. The dev database equals the seeds (no edits, no photo, one location, all published).
- Things Stage 2 must address beyond the prompt's list:
  - **Half the credentials (4 of 8) have no institution**, so a flip card would have an empty back. Decide what those cards do (don't flip, or show something else), alongside the `Credential.detail` proposal.
  - **The logo is binding but raster only** (1080² JPEG). Propose how it appears in the header at small sizes (vector redraw, or the lungs mark alone). Its stethoscope is the cliché the brief warns about; the lungs-and-airways drawing is the stronger motif.
  - **The placeholder SVG is cold blue-grey** and reads as a stock avatar; propose a warmer or branded placeholder (a monogram or the logo mark).
  - **Latin-wrapping filter**: Latin runs (ERS, ATS, ICU, COPD, Ablation) arrive inside admin-typed text, so they need automatic isolation, not hand-wrapping. Titles that *start* with Latin must stay RTL.
  - **Site-wide data** (profile, locations) needs a context processor or inclusion tag.
  - **Static layout proposal** must include the broken `site.webmanifest` (empty name, root-relative icon paths) and media serving in dev (no URL pattern today).
  - `INQUIRY_NOTIFICATION_EMAIL` is defined only in `prod.py`.
- The Playwright MCP server timed out at startup this session. If it fails again, the in-app browser can't reach `localhost`, so screenshots of local mockups would need another route; check it first.
