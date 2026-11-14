# Design progress

This is the handoff file between chats. Each chat does the first stage below that isn't done, following [`docs/DESIGN_PROMPT.md`](../DESIGN_PROMPT.md). At the end of the stage, the chat updates this file and writes a commit message in chat. Chats never commit: the owner commits each stage before opening the next chat.

Kickoff line for every new chat:

> Read `docs/DESIGN_PROMPT.md` and `docs/design/PROGRESS.md`, then do the next stage.

## Stages

| # | Stage | Status | Gate |
|---|---|---|---|
| 0 | References (done before this workflow) | ✅ done 2026-11-14 | owner picked the sites |
| 1 | Inspection | ⬜ next | — |
| 2 | Direction and mockups | ⬜ | **required:** choose a direction, answer the proposals and content questions |
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

## Open questions for the owner

These are answered at the Stage 2 gate. Record each answer under Decisions.

- Surname spelling: صفانوایی (our seeds) or صفاءنوائی (Paziresh24)?
- Clinic hours: «روزانه، شیفت عصر» or «ویزیت عصر ۳ روز هفته»?
- Is Imam hospital in Sari (mornings, inpatients) a patient-facing second Clinic Location?
- Show the medical council number (51510)?
- Email provider for Inquiry notifications (not blocking).

## Handoff to next stage

**Stage 1** starts from `main`. There is no frontend at all yet, only the admin. The Playwright MCP server is configured for this project, and Node.js is installed.
