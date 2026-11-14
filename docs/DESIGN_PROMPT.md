# Prompt: Dr. Sepideh Safanavaei: public frontend design and build

The work is split into **8 stages, one chat each**, so every chat starts with a fresh context.

To start any stage, open a new Claude Code chat in this project and send only this:

> Read `docs/DESIGN_PROMPT.md` and `docs/design/PROGRESS.md`, then do the next stage.

`PROGRESS.md` says which stage is next and what earlier chats decided. Everything below the line is the instruction for every chat.

---

You are designing and building the public frontend of **Dr. Sepideh Safanavaei's website** (دکتر سپیده صفانوایی), a Persian-language site for an internal medicine specialist subspecialised in pulmonology, at `dr.safanavaiee.ir`. It is built with Django 5.2 server-rendered templates.

There is **no frontend yet**: no public views, URLs or templates exist, only the Django admin. Design it from scratch. The goal is a site that feels like a $10K commission, not a $200 template.

## How the work is staged (read this first, every chat)

**One stage per chat.**
- Each chat does exactly one stage: the first stage in `docs/design/PROGRESS.md` that isn't marked done. If a stage was interrupted, continue it from its checkpoint.
- Never start the next stage in the same chat, even if there is room left.

**Never commit.** You don't run `git commit`, `git push`, `git merge` or `git stash`, ever. I commit myself, using the commit message you write in chat at the end of each stage. Other git commands that don't change history are fine: `status`, `diff`, `log`, and creating or switching branches.

**Starting a chat.**
1. Run `git status`. If the previous stage's work is still uncommitted, stop and ask me to commit it first, using the message the previous chat gave me. Each stage must start from a clean tree, so that its own changes are easy to review.
2. Read this file, then `docs/design/PROGRESS.md` in full.
3. Read the outputs of the earlier stages that the current stage lists under "Reads".
4. Don't re-derive decisions recorded in `PROGRESS.md`; build on them.
5. If the current stage has a gate that `PROGRESS.md` doesn't record as passed, stop and ask me for it.

**Ending a stage.** Every stage ends the same way:
1. Check every item in the stage's "Done when" list. If one isn't met, the stage isn't done.
2. Run `venv/bin/python manage.py test apps` (from Stage 3 on) and make sure it passes.
3. Update `docs/design/PROGRESS.md`:
   - mark the stage done, with the date,
   - record every decision made (and every answer I gave) in the "Decisions" log,
   - record anything left open, and anything the next stage must know, under "Handoff to next stage".

   Keep it short. It's a handoff, not a diary.
4. **Don't commit.** Write a commit message for the stage's work, `PROGRESS.md` included, as a fenced code block in your reply:
   - a Conventional Commit subject line,
   - a body that lists what changed,
   - ending with the `Co-Authored-By` line from the session's attribution instructions.

   From Stage 3 on, say that it belongs on the `frontend-design` branch.
5. Then **stop** and end your reply with this message, in Persian, with the blanks filled in:

   > ✅ مرحله‌ی N («نام مرحله») تمام شد. [یک یا دو جمله درباره‌ی آنچه ساخته شد]
   > قبل از باز کردن چت جدید، تغییرات را با commit message بالا کامیت کن.
   > [اگر گیت دارد: آنچه باید بررسی و تأیید کنی، با مسیر فایل‌ها یا اسکرین‌شات‌ها]
   > برای مرحله‌ی بعد («نام مرحله‌ی بعد») یک چت جدید باز کن و این را بفرست:
   > `Read docs/DESIGN_PROMPT.md and docs/design/PROGRESS.md, then do the next stage.`

**Gates.** A gate is a decision only I can make.
- When a stage has a gate, end the stage by presenting what I need to decide, then stop.
- When I answer, in the same chat or in the next one, record my answer in `PROGRESS.md` before any work that depends on it.

**Running out of room mid-stage.** If the context gets long before the stage is done, don't rush the remaining work:
1. Write a "Checkpoint" under that stage in `PROGRESS.md`: what's finished, what's left, and the exact next step.
2. Write a commit message for the work in progress, in chat (don't commit).
3. Tell me in Persian to open a new chat to continue that same stage, using the same kickoff line.

## What the site is for

Read these first. They are current, and they outrank anything in this prompt that disagrees with them:
- `agents.md`
- `CONTEXT.md`
- `docs/plan.md`
- `docs/adr/`
- `docs/design/references/README.md`

Use the domain vocabulary from `CONTEXT.md` (Doctor Profile, Condition Treated, Procedure Performed, Clinic Location, Inquiry, Content Editor), and avoid the terms it lists as ones to avoid.

- **Primary job: credibility.** A patient who already has her name, through a referral or word of mouth, confirms her credentials and finds how to reach her.
- **Secondary job: light organic reach.** Patients searching for an internist or pulmonologist in Amol (lung disease, asthma, COPD, diabetes, bronchoscopy…) who don't know her name yet.
- **Conversion:** the patient contacts the clinic. For an Iranian patient that is mostly **a phone call** (landline or mobile), then the contact form, then walking in with the address and map link. Every page should offer that path clearly, and never push.
- **Audience:** patients of all ages, often older, and often a relative (a son or daughter) researching on a phone on behalf of a parent. Design for trust, legibility and calm. Body text must be comfortable for a 60-year-old reader on a phone.
- **Out of scope by design** (see `docs/plan.md` backlog): online booking or a calendar, blog, testimonials, FAQ, analytics, English/bilingual, structured per-day hours. Don't design or propose them. Linking out to her existing Paziresh24 profile is allowed as a proposal, because it doesn't build booking.

## Ground rules

- **Branch.** Stages 1–2 only write documents and mockups, and I commit them to `main`. Stage 3 creates and switches to a `frontend-design` branch from `main`, and from then on all work happens there. Check with `git branch --show-current` at the start of every chat. You never commit, merge or push (see "Never commit" above).
- **Gate.** Don't build anything until I approve the direction at the end of Stage 2. Stages 1–2 are read-only, plus writing documents and throwaway mockups.
- **Backend: what you may build.** Public views, URL confs and templates that follow the URL structure in `docs/plan.md`:
  - `/`
  - `/about/`
  - `/conditions/` and `/conditions/<slug>/`
  - `/locations/`
  - `/contact/`

  Build the views **test-first** with the `tdd` skill, and keep the existing test suite passing.
- **Backend: what needs approval.** Don't change models, migrations or the admin unless you propose the change in Stage 2 and I approve it. `docs/design/references/README.md` already lists candidate model changes ("Backend gaps"). They are proposals, not approvals.
- **Admin.** Leave the Django admin's look alone.
- **Language and direction.** The site is `lang="fa" dir="rtl"` (ADR-0001). Every layout, icon direction, animation direction and number format must be right for RTL Persian.
  - Embedded Latin terms must be wrapped so mixed sentences stay readable. Seeded titles already contain them: "COPD (بیماری انسدادی مزمن ریه)", "Ablation تومورهای برونکیال ریه", "ERS", "ATS", "ICU".
  - Show Persian digits everywhere through one template filter, never by hand. Phone `tel:` links keep ASCII digits.
- **Doctor photo.** Always render it through `DoctorProfile.photo_url`. The real photo hasn't arrived, so it currently falls back to a neutral placeholder SVG.
  - The design must look intentional with the placeholder and with a real portrait of unknown size and aspect ratio. Uploads are not processed or cropped.
  - Never use stock photos of other people as the doctor.
- **Clinic Locations.**
  - There is one location today, the Amol clinic.
  - A second one may be added later from the admin alone. A test already guarantees that adding one needs no code change.
  - Design for 1 to N locations. One location must not look like a lonely card in a grid built for three.
- **Contact form (Inquiry).** This pulls Phase 4 of `docs/plan.md` forward into Stage 6, because the contact page can't be designed and verified without it.
  - Build the form, its validation and the honeypot check (the `website` field: drop the submission silently if it's filled), test-first.
  - Send an email only when `INQUIRY_NOTIFICATION_EMAIL` is set. No email provider is chosen yet, and prod uses the dummy backend. The submission must always be saved and never fail because of email.
  - No medical-detail field, by design.
- **Frontend stack.** `docs/plan.md` proposes Tailwind, Vazirmatn, and htmx only if needed. Treat that as a starting point, not a decision. In Stage 2, recommend one of:
  - Tailwind (the standalone CLI binary; **Node.js is not installed on this machine**),
  - or plain modern CSS (custom properties, `@layer`) with small vanilla JS.

  Keep the dependency list short either way.
- **Static and media files** are already set up, the same way as in ArameshMusicAcademy-website. Don't change the layout.
  - Edit sources only in `static_dev/`. It is **gitignored and dev only** (`STATICFILES_DIRS`), and the favicons already live in `static_dev/assets/img/`. App-level static files (for example `apps/doctor/static/doctor/doctor-placeholder.svg`) are collected too.
  - **After any static change, run `venv/bin/python manage.py collectstatic --noinput` locally.** Its output, `public/static/`, **is committed**: include it in the stage's commit message, together with `staticfiles.json` and the hashed copies. Delete hashed copies the manifest no longer names, so old ones don't pile up.
  - Production serves that committed `public/static/` through WhiteNoise, with `config.storage.StaticFilesStorage` (compressed manifest).
    - With `DEBUG` off, `{% static %}` links hashed names cached for a year, and a path missing from the manifest is an error.
    - **The test runner always runs with `DEBUG` off, so a forgotten `collectstatic` makes tests fail.** Run it before the tests.
  - **Never run `collectstatic` on Runflare.** `static_dev/` isn't deployed, so running it there would rewrite the manifest without the site's own files.
  - URLs are `/public/static/` and `/public/media/`.
    - Uploads go to `public/media/` (gitignored), served by `config/urls.py` whatever `DEBUG` is.
    - On Runflare a disk is mounted at `/app/public/media` only. A disk at `/app/public` would hide the committed static files.
  - To try production serving locally, run with `DEBUG=False` and `runserver --nostatic`.
- **Running locally.**
  - Use `venv/bin/python manage.py runserver 8018`, which uses `config.settings.dev`, or the `django` entry in `.claude/launch.json`.
  - The dev database already holds the seeded real content. If you build a fresh database, `migrate` re-seeds it.
  - Run the tests with `venv/bin/python manage.py test apps`.

## Open content questions (don't resolve these yourself)

The references README lists data on her Paziresh24 profile that disagrees with our seeds:
- the surname spelling صفانوایی vs **صفاءنوائی**,
- clinic hours, «روزانه» vs **«ویزیت عصر ۳ روز هفته»**,
- a possible second location, **mornings at Imam hospital in Sari, for inpatients**,
- her medical council number, **51510**.

Don't hardcode any of these into templates. Repeat them as questions for me at the Stage 2 gate, and design so that every answer fits without a layout change.

## Skills to use

They are installed in `.claude/skills/` (gitignored). The `tdd`, `prototype`, `grilling`, `domain-modeling` and `code-review` skills come from the user-level skill set. Invoke each with the Skill tool and actually follow it; don't just name it.

1. **`impeccable`**: the backbone of the process.
   - Start with `/impeccable init` to capture product and design context.
   - Use `shape` to form the direction, and `craft` / `layout` / `typeset` / `colorize` while building.
   - Use `critique` and `audit` to review, `harden` for edge cases and `polish` to finish.
   - Let it produce `DESIGN.md` documenting the final system.
2. **`design-taste-frontend`** (taste-skill): the art direction.
   - Propose distinct directions grounded in the real references in `docs/design/references/`.
   - Follow its anti-slop rules (`references/tells.md`).
   - Use its browser inspector and its screenshot look-and-fix loop on every page.
3. **`apple-design`** (Emil Kowalski): the motion and interaction standard.
   - Physical, interruptible motion where it fits, used with restraint.
   - Correct typographic detail (leading, optical sizes; never letter-space Persian).
   - `prefers-reduced-motion` support, and feedback on every interaction.
4. Supporting skills, each tied to a phase:

   | Skill | Stage | Use it for |
   |---|---|---|
   | `animation-vocabulary` | 1 | Name the exact motions in the references (for example the Awards flip card, Tia's slide-up, Shafer's button invert), so Stage 2 can specify them precisely. |
   | `prototype` / `emil-prototype` | 2 | Throwaway mockups of the home hero and the credential section for each direction, so I can compare them before choosing. |
   | `grilling` | Between 2 and 3 | I may run it myself to stress-test the chosen direction. Wait for the outcome before building. |
   | `domain-modeling` | 3, only if I approved a model change | Add any new term (for example the medical council number) to `CONTEXT.md` with the change. |
   | `tdd` | 3–6 | Every new view, URL, form, model change and template filter, test-first. |
   | `emil-design-eng` | 3–6 | Component polish and the small details that make UI feel right. |
   | `animate` | 4, then 7 | Stage 4: the credential flip card. Stage 7: whatever `find-animation-opportunities` approves. For each: purpose, property, curve, duration, interruption, exit. |
   | `find-animation-opportunities` | 7 | Decide where motion helps and where it doesn't, with exact values. It's read-only, so act on what it finds with `animate`. |
   | `mobile-native` | 3–7 | The phone pass: tap-to-call, tap highlights, `100vh`, input zoom on the form, safe areas, sticky hover. |
   | `simplify` | 7 | Clean up the new templates, CSS, JS and views. |
   | `review-animations` | 7–8 | A strict review of all motion. It only runs when called by name, so call it explicitly. |
   | `animation-performance` | 7–8 | Keep motion on composite-only properties and inside the frame budget. |
   | `break-ui` | 4–6 (each page), 8 (whole site) | Push the worst-case content from Stage 1 through each page. |
   | `code-review` | 8 | Review the branch against `main` for standards and spec. |

   `impeccable`, by stage:
   - `init` in Stage 1,
   - `shape` in Stage 2,
   - `craft` / `layout` / `typeset` / `colorize` in Stages 3–6,
   - `critique` / `audit` / `harden` / `polish` in Stage 8,
   - `document` in Stage 8.

   Most of Emil Kowalski's skills assume React and Framer Motion. Translate their advice into plain CSS (transitions, `@keyframes`, `linear()` easing for springs) and vanilla JS (WAAPI). Don't add a framework to follow them.

If two skills disagree, the order of authority is: my approved direction → the 10K checklist below → impeccable → taste-skill → apple-design. Tell me about real conflicts instead of silently picking one.

## What the references ask for

`docs/design/references/README.md` has the owner's own words and the measured details. In short:
- **Overall feel: Parsley Health.** Warm, editorial and rich, never clinical-blue. Richness comes from type, colour and photography, not animation.
- **Buttons: Parsley first, then Tia and Shafer.**
  - Full pills, quiet colour-only hover states (about 150ms).
  - A secondary pill that turns into an outline on hover.
  - Shafer's invert-on-hover is one candidate for the primary contact button.
- **Credentials: van Straten's Awards flip card,** which the owner asked for explicitly. Use it for `Credential`: the front shows `title` + `year`, the back shows `institution` (and a longer detail, if I approve that field).
  - It must work on tap and on keyboard focus, not only on hover.
  - It must stay readable to screen readers.
  - It becomes a crossfade under reduced motion.
  - The turn is mirrored for RTL.
- **Structure: van Straten.** Name and degrees in the header lockup, conditions as a top-level nav item, and all practice locations named near the primary call to action.
- **Always-reachable contact: Shafer's floating appointment tab,** re-made as a contact/call affordance (tap-to-call on mobile).
- **Trust above the fold: Digestive Health UK's founder card,** with her face, name and titles on the first screen, and the clinic phone in the header.
- **Condition detail page: Mayo Clinic's structure.**
  - The section order, an "on this page" index, and a "when to see a doctor" block that leads straight to the clinic phone.
  - Today's `ConditionTreated.body` is one short free-text field, so the design must work with one or two sentences now and with longer structured content later (propose how in Stage 2).
- **Paziresh24: what Iranian patients expect to find at once.** Years of experience, the medical council number, the address with a map/route link, both phone numbers, and the hours.
  - Don't copy any patient reviews onto the site.

## The $10K checklist (acceptance criteria)

The finished site must pass all eight. Each one becomes a section of the final report, with evidence.

1. **Point of view, not a template.** One specific design direction, executed without flinching. It must fit *this* doctor (an Amol internist and pulmonologist, three decades of practice, diabetes centre history, interventional pulmonology) and must not be generic "medical blue with a stethoscope". Run the competitor test: put another doctor's name on it, and it should no longer fit.
2. **Typography that does work.** A paired display face and body face, neither of them Inter or Roboto.
   - Both need excellent Persian/Arabic-script support. Check how they render Persian, including embedded Latin (COPD, ERS) and Persian digits, not just Latin.
   - Self-host the fonts (woff2, subset, `font-display: swap`).
   - Scale and weight carry the hierarchy, and headlines feel chosen.
   - Body text sits at 18px or more on phones.
3. **A restrained color system.** Three to five colours, defined as tokens and used consistently. Premium comes from restraint, not decoration.
4. **Hierarchy that breathes.** Whitespace, scale and contrast give every page a clear primary, secondary and tertiary level.
   - The long bio (six paragraphs) and the 20 conditions and procedures must never become flat walls of content.
5. **Imagery with intent.** Today there is no photography at all: the doctor photo is a placeholder, and there are no clinic photos.
   - Design so the site is complete and premium without photos (type, colour, layout and any illustration that matches the art direction), and gets better when real photos arrive.
   - No stock-photo defaults, and no stock people standing in for the doctor.
   - Any anatomical or medical illustration must be accurate or abstract, never wrong.
   - List the photos I should ask the doctor for (portrait, clinic interior, building exterior), with the framing and aspect ratio the design needs.
6. **Motion that whispers.** Hand-crafted micro-interactions and scroll behaviour, not AOS fade-up everywhere. The credential flip card is the one signature moment. Everything else stays quiet. A designer shouldn't roll their eyes at any of it.
7. **Mobile that's designed, not shrunk.** The phone layouts are their own decisions:
   - the navigation,
   - tap-to-call as the primary action,
   - the conditions list (20 items),
   - the credential cards,
   - the location block with its map link,
   - the contact form.
8. **The invisible expensive stuff.**
   - Under 2s load (LCP), WCAG AA contrast, full keyboard navigation with visible focus.
   - Semantic HTML landmarks and a correct `lang`/`dir`.
   - Real meta tags (title, description, Open Graph, canonical) for every page, including each condition page.
   - `schema.org` structured data (`Physician` / `MedicalClinic` with address, phone and hours; `MedicalCondition` on condition pages).
   - Accessible forms with clear Persian error messages, and no console errors.

## The verification loop (used by Stages 3–8)

Run this on every page you build or change, before calling it done.

Use the Playwright MCP tools against the running dev server:

- Screenshot at **1440×900, 768×1024 and 390×844**, then look at the screenshots critically and fix what's off. Repeat until it's right. Also use taste-skill's inspector.
- Check `browser_console_messages` for zero errors, and `browser_network_requests` for no 404s and sensible asset sizes.
- **Keyboard:** Tab through the whole page.
  - The focus order makes sense in RTL, and focus is always visible.
  - Menus open and close with the keyboard, and Escape closes overlays.
  - The credential cards turn on focus.
- **Motion:** check `prefers-reduced-motion` with `browser_emulate_media`, and check that nothing animates in a way that blocks content.
- **Accessibility:** WCAG AA contrast, a heading hierarchy, landmarks, alt text, and labelled form fields.
- **Worst cases:** test the worst-case content from Stage 1 with `break-ui`, including two and three Clinic Locations.
- **After the motion pass:** run `review-animations` and `animation-performance`, and fix what they flag.
- **Tests:** run `venv/bin/python manage.py test apps` and keep it passing.
- **Before the final report:** run `code-review` on the branch against `main`, and fix what it finds.

## Stage 1: Inspection (read-only)

**Reads:** everything in "What the site is for", plus `docs/design/references/` (the README and every screenshot).

**Work:**
- Run `/impeccable init` to capture the product and design context.
- **Backend:** every app under `apps/`. Cover:
  - models and their fields (what's optional or blank), the default `ordering`, and `DoctorProfile.photo_url`,
  - the admin (the singleton profile, inline credentials, read-only inquiries),
  - the seed migrations and the real seeded content,
  - settings (dev and prod: static, media, email),
  - the existing tests.

  Write down every piece of content the frontend can show and where it comes from.
  - Note that `ConditionTreated` holds both Conditions Treated and Procedures Performed, split by `category`, and that the site shows them as two labelled groups. Only `is_published=True` rows are public.
- **Frontend:** there is none. Record that, and what the admin looks like today.
- **References:** visit the live sites for the motion with the Playwright MCP tools (`mcp__playwright__*`), and name each motion with `animation-vocabulary`.
- **Edge cases:** the content extremes the design must survive:
  - **Long text:**
    - a long condition title with embedded Latin («Ablation تومورهای برونکیال ریه»),
    - a credential with no institution and no year (several seeded ones),
    - the full six-paragraph bio, which uses `\n\n` breaks,
    - an empty `intro_tagline`.
  - **Missing pieces:**
    - no photo (the placeholder),
    - a location with no mobile number and no map link,
    - zero published procedures,
    - a condition with a one-sentence body,
    - an unpublished condition reached directly by URL (it must 404).
  - **Several locations and the contact form:**
    - two or three Clinic Locations,
    - a phone number typed with Persian digits («۰۹۱۱…»), or with spaces or dashes, in the contact form.

**Done when:** `docs/design/00-inspection.md` exists with the content inventory, the edge-case list and the named reference motions. `PROGRESS.md` is updated, and the commit message is written in chat.

**Gate:** none. End the stage and send me to Stage 2.

## Stage 2: Direction and mockups

**Reads:** `docs/design/00-inspection.md`.

**Work:** write `docs/design/01-direction.md`, containing:

- 2–3 **genuinely different** directions from `design-taste-frontend` and `impeccable shape`, all inside the references' brief (Parsley-warm, not clinical). For each one, give:
  - the concept in one line, and which references it draws on,
  - the type pairing, with a Persian sample including Latin terms and Persian digits,
  - the palette as tokens, and the imagery treatment without photos,
  - the motion character, including how the credential flip card looks in it,
  - a sketch of the home page structure.
- Your recommendation and why it fits this doctor.
- **The page and section inventory** for every URL, mapped to the real model fields from Stage 1. Make sure every model has a place to appear.
- **The proposals that need my approval**, each optional and each with its cost:
  - backend gaps (the medical council number, a Paziresh24 link, `Credential.detail`, condition↔procedure links, a structured condition body),
  - the frontend stack (Tailwind vs plain CSS; either way, the output CSS goes in `static_dev/`),
  - image processing for the uploaded photo.
- The open content questions, restated for me to answer.

Use `prototype` to build one static HTML mockup per direction in `docs/design/mockups/`, covering the home hero with the founder card and the credential flip section, using the real Persian content. Screenshot them with Playwright at 1440 and 390 widths.

**Done when:** the direction document and the mockups with screenshots exist, `PROGRESS.md` is updated, and the commit message is written in chat.

**Gate (required):** I choose a direction and answer each proposal and each content question. Record every answer in `PROGRESS.md`. Stage 3 must not start without them.

## Stage 3: Foundation

**Reads:** `01-direction.md`, and the decisions in `PROGRESS.md`.

**Work:**
1. Create the `frontend-design` branch from `main`.
2. Make the approved backend changes only, test-first, with migrations, and with `CONTEXT.md` updated through `domain-modeling`. Update the seeds if I corrected content (for example the surname spelling or the hours).
3. Put the new CSS, JS and font sources in `static_dev/`, and run `collectstatic` (see "Static and media files").
4. Add the design tokens:
   - fonts (self-hosted woff2, subset), colour, type scale, spacing, radii and motion tokens,
   - a reset and layout primitives,
   - the Persian-digits template filter, test-first.
5. Build `base.html` and the shared parts:
   - the header with the name and degrees lockup and the navigation, for desktop and mobile,
   - the always-reachable contact path (tap-to-call on mobile),
   - the footer with every Clinic Location's address, phones, hours and map link,
   - the default meta tags and structured data.
6. Add a temporary home view that renders only the shell, so it can be verified.
7. Run the verification loop on the shell.

**Done when:** the shell passes the verification loop at all three widths, the tests pass, the commit message is written in chat, and `PROGRESS.md` lists the tokens and the template structure (blocks and partials) the page stages must use.

**Gate (required):** I review the shell screenshots (header, footer, mobile navigation) and approve the look before any page is built.

## Stage 4: Home and About

**Reads:** `PROGRESS.md` (tokens, template structure), `01-direction.md`.

**Work:** each view and URL is built test-first, then put through the verification loop.
- **Home:** the founder card, the tagline, the top conditions and the locations summary.
- **About:** the bio and the **credential flip cards**, built with `animate` to the `apple-design` standard. They must work on tap and on keyboard focus, be readable to screen readers, become a crossfade under reduced motion, and turn in mirror for RTL.

**Done when:** both pages pass the verification loop and `break-ui`, the tests pass, `PROGRESS.md` is updated, and the commit message is written in chat.

**Gate (required):** I review Home and About. These are the first real pages, so this is the check that the direction holds up. My notes go into `PROGRESS.md` for Stage 5.

## Stage 5: Conditions and Locations

**Reads:** `PROGRESS.md`, especially my Stage 4 notes.

**Work:** each view and URL is built test-first, then put through the verification loop.
- **Conditions list:** two labelled groups (Conditions Treated, Procedures Performed), published rows only.
- **Condition detail:** Mayo-style, built for today's short bodies, with a "when to see a doctor" block that leads to the clinic phone, its own meta tags and `MedicalCondition` structured data. An unpublished slug returns 404.
- **Locations:** 1 to N. Verify with one, two and three locations.

**Done when:** all three pages pass the verification loop and `break-ui`, the tests pass, `PROGRESS.md` is updated, and the commit message is written in chat.

**Gate:** none. End the stage and send me to Stage 6. Include the screenshots in your message so I can comment.

## Stage 6: Contact and error pages

**Reads:** `PROGRESS.md`.

**Work:**
- **Contact:** the Inquiry form, its validation, the honeypot, and the success and validation-error states, all test-first.
  - Normalise phone numbers typed with Persian digits.
  - Send the optional email only when `INQUIRY_NOTIFICATION_EMAIL` is set.
- **404 and 500 pages.**

**Done when:** the pages pass the verification loop (including the form's keyboard and error states), the tests pass, `PROGRESS.md` is updated, and the commit message is written in chat.

**Gate:** none. End the stage and send me to Stage 7.

## Stage 7: Motion, mobile and cleanup

**Reads:** `PROGRESS.md`.

**Work:**
1. Run `find-animation-opportunities` on the finished site, and build what it approves with `animate`. The flip card stays the one signature moment; everything else stays quiet.
2. Apply `emil-design-eng` and `mobile-native` across the site.
3. Run `review-animations` and `animation-performance`, and fix what they flag.
4. Remove anything unused, remove the temporary bits from Stage 3, and run `simplify`.

**Done when:** every page passes the verification loop again, the tests pass, `PROGRESS.md` is updated, and the commit message is written in chat.

**Gate:** none. End the stage and send me to Stage 8.

## Stage 8: Final review and report

**Reads:** `PROGRESS.md`, `01-direction.md`, and the checklist above.

**Work:**
1. Run `impeccable critique` and `audit`, then `harden` and `polish`. Run `break-ui` across the whole site.
2. Run `code-review` on the branch against `main`, and fix what it finds.
3. Write `DESIGN.md` with `impeccable document`.
4. Write `docs/design/report.md`:
   - each checklist item with screenshots at all three widths,
   - Playwright-measured LCP and transfer size,
   - the known gaps,
   - the photo shot list for the doctor,
   - anything I need to do in the admin.

**Done when:** everything above exists on `frontend-design`, the tests pass, `PROGRESS.md` marks the design work complete, and the commit message is written in chat.

**Gate (required):** I review the report and decide whether to merge `frontend-design` into `main`. Don't merge or push yourself.
