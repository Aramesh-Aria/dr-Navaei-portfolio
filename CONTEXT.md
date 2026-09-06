# Dr. Navaei Portfolio

A professional website for Dr. Navaei, a pulmonologist (lung specialist). Its primary job is credibility: a patient who already has her name (via referral or word of mouth) confirms her credentials and finds contact info. Secondary job: light organic reach for patients searching for a pulmonologist who don't know her name yet.

## Language

**Site content**: Farsi (Persian), rendered right-to-left (RTL). Embedded English/Latin terms (drug names, medical terminology, measurements) are wrapped so they render left-to-right within the surrounding RTL flow, keeping mixed sentences readable.
_Avoid_: bilingual, multi-locale — the site is Farsi-only; no `/fa/`/`/en/` locale switching or translated duplicate content.

## Roles

**Content Editor**: someone who updates site content after launch through Django admin. Currently: the site's builder (technical) and the doctor's daughter (non-technical). Drives the decision to make content admin-editable rather than hardcoded in templates, since a non-technical editor needs to change it without touching code.
_Avoid_: admin user, staff (Django's own auth terms — kept distinct from this project-level role)

## Domain terms

**Doctor Profile**: the singleton record describing Dr. Navaei herself — bio, credentials, education, photo.
_Avoid_: About page (that's the template that renders this record, not the record itself)

**Condition Treated**: a specific lung condition/disease she treats, listed for patients and for SEO.
_Avoid_: Service, Specialty

**Clinic Location**: a physical address and hours at which she practices.
_Avoid_: Branch, Office

**Inquiry**: a message a prospective patient submits through the contact form.
_Avoid_: Lead, Submission, Contact request
