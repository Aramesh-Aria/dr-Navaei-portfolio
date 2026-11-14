# Plan: Dr. Sepideh Safanavaei Portfolio

This is the working plan for the Django app/model structure and the phased build order. It assumes the shared understanding captured in [`CONTEXT.md`](../CONTEXT.md) and the three ADRs in [`docs/adr/`](./adr/) — read those first for *why*; this document is the *what* and *in what order*.

## App structure (modules)

Four Django apps, each owning one cohesive concept — kept separate because each earns its place under the deletion test (delete it, and real behavior/content disappears, not just a pass-through):

```
config/            # project settings, root urls.py
apps/
├── doctor/         # Doctor Profile + Credentials — the "About" content
├── conditions/     # Condition Treated + Procedure Performed — one per item, own detail page
├── locations/      # Clinic Location — one or more practice addresses/hours
└── inquiries/      # Inquiry — the contact-form submissions
```

Each app's **interface** is two things: the Django admin (the seam the Content Editor uses) and its models/template context (the seam the public templates render from). No app needs a REST API — there's no separate frontend consuming one (ADR-0001's sibling decision, Q8).

### `doctor`

```python
class DoctorProfile(models.Model):        # singleton — see "Singleton pattern" below
    full_name = models.CharField(...)
    bio = models.TextField()               # Farsi, may contain embedded LTR terms
    photo = models.ImageField(upload_to="public/media/doctor/")
    intro_tagline = models.CharField(...)  # short line used on Home

class Credential(models.Model):
    profile = models.ForeignKey(DoctorProfile, related_name="credentials", ...)
    title = models.CharField(...)          # e.g. "Board Certification in Pulmonology"
    institution = models.CharField(...)
    year = models.PositiveIntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)  # manual sort in admin
```

`Credential` is a separate model (not a text blob) so the daughter can add one via an inline admin form when a new one comes up, without touching a template or asking you to edit code — this is the "content should be admin-editable, not hardcoded" decision from Q3, applied concretely.

### `conditions`

```python
class ConditionTreated(models.Model):
    category = models.CharField(choices=[("condition", ...), ("procedure", ...)])
    # Holds both Condition Treated and Procedure Performed (CONTEXT.md) in one
    # table — `category` is the only real variation between them, so a second
    # model/app would be a seam with nothing behind it.
    title = models.CharField(...)                 # Farsi name, e.g. "آسم" or "برونکوسکوپی"
    slug = models.SlugField(unique=True)           # Latin, e.g. "asthma" — see URL note below
    short_description = models.CharField(...)      # for list/card view
    body = models.TextField()                      # full detail-page content
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
```

Each gets its own URL (`/conditions/<slug>/`) per Q10 — the SEO surface for "پزشک ریه برای <condition>" (or internal-medicine/diabetes equivalent, per the broadened scope) searches. The public template groups the list by `category` into two labeled sections rather than exposing it as a technical field.

### `locations`

```python
class ClinicLocation(models.Model):
    name = models.CharField(...)           # e.g. "مطب اصلی" / "بیمارستان ..."
    address = models.TextField()
    phone = models.CharField(...)          # landline
    mobile_phone = models.CharField(blank=True)  # for calls/SMS — not WhatsApp-specific
    map_url = models.URLField(blank=True)  # link to a maps service, not an embed — keep it simple
    hours = models.TextField()             # free text; structured per-day hours is v2 if it turns out to matter
```

Plain list page, no per-location detail pages — unlike Conditions, locations aren't a search-driving surface, just practical info alongside Contact.

### `inquiries`

```python
class Inquiry(models.Model):
    name = models.CharField(...)
    phone = models.CharField(...)
    preferred_contact_time = models.CharField(blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    # honeypot field, not shown to real users via CSS; if filled, silently drop the submission
    website = models.CharField(blank=True)
```

No medical-detail field, by design (Q11). On save, the view sends an email notification in addition to storing the row — both, per your answer.

### Singleton pattern for `DoctorProfile`

There's only ever one. Rather than pull in a package for this, override the admin's `has_add_permission` to return `False` once a row exists, and `changelist_view` to redirect straight to the single instance's edit page. About five lines; no new dependency for a problem this small.

## URL structure

Latin ASCII slugs for URLs even though page content is Farsi (`/conditions/asthma/`, not a percent-encoded Farsi slug) — cleaner when shared as a link, and Farsi search ranking comes from the page's rendered title/content, not the URL slug. Flag if you'd rather have Farsi URLs; easy to change now, harder once patients start bookmarking/sharing links.

```
/                       Home (pulls DoctorProfile.intro_tagline, top Conditions, Locations summary)
/about/                 Doctor Profile + Credentials
/conditions/            List
/conditions/<slug>/     Detail
/locations/             List (all ClinicLocations)
/contact/               Inquiry form
/admin/                 Django admin (Content Editor login)
```

## Phased roadmap

**Phase 0 — Project setup**
Django project (`config/`) + the four apps, split settings (`base.py`/`dev.py`/`prod.py`), env vars via `python-dotenv` or `django-environ` for `SECRET_KEY`/`DEBUG`/DB path, `requirements.txt`.

**Phase 1 — Models & admin**
Models above, migrations, admin registration (inlines for `Credential` under `DoctorProfile`), the `DoctorProfile` singleton guard. No templates beyond admin yet. This is the natural point to reach for the `tdd` skill if you want model/admin behavior (e.g. the singleton guard, the honeypot logic) built test-first.

**Phase 2 — Content population**
Once the asset checklist comes back from your aunt, populate real data through the admin. This validates the field choices against real content (a bio that's too long for `intro_tagline`, a condition description that needs more structure, etc.) before any template is built around assumed shapes.

**Phase 3 — Frontend design & build**
Reference-hunting (Pinterest etc.) → Claude Design mockup with the *real* Farsi content from Phase 2 → Tailwind + Vazirmatn templates (`base.html` + blocks), RTL by default with explicit LTR spans for embedded English/Latin terms, htmx only if a specific interaction needs it.

**Phase 4 — Inquiry flow**
Contact form view + validation, honeypot check, email notification (needs an SMTP/email provider reachable from Iran — open item, see below).

**Phase 5 — Deploy to Runflare**
Per ADR-0002/0003: `DATABASES['default']['NAME']` under a disk-mounted folder (e.g. `/app/database/db.sqlite3`), `STATIC_ROOT`/`MEDIA_ROOT` under `public/` (static is committed and served by WhiteNoise; a disk is mounted at `/app/public/media` only, for uploads), `DEBUG=False`, `ALLOWED_HOSTS` set once the domain is picked, `collectstatic` is never run on Runflare: it runs locally and `public/static/` is committed (decided 2026-11-14, same as ArameshMusicAcademy-website); after a deploy, run only `migrate`.

## Explicitly out of scope for v1 (backlog)

Blog/announcements, testimonials, FAQ, real booking/calendar system, analytics, bilingual (Farsi/English) support, structured per-day opening hours. Don't build toward these speculatively; revisit if a real need shows up.

## Open external items (not blocking the build)

- Photo(s) — not yet provided; `DoctorProfile.photo` stays blank until they arrive, and templates use `DoctorProfile.photo_url`, which falls back to a neutral placeholder (`apps/doctor/static/doctor/doctor-placeholder.svg`).
- Domain name — resolved: `dr.safanavaiee.ir`.
- Email provider for Inquiry notifications, reachable from Iran — needs picking before Phase 4. Until then `EMAIL_*` env vars stay empty and prod uses the dummy email backend (inquiries are still saved in the admin).
- Second clinic location — Q9 assumed multiple locations, but the asset text only gives one concrete address (the Amol private clinic). Her morning academic affiliation (Mazandaran University of Medical Sciences) may or may not be a second patient-facing location — confirm before adding a second `ClinicLocation` row. No code change needed to add one: it's a new row in the admin.
