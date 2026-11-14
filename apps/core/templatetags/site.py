"""Template filters every public page uses.

Persian digits, phone numbers and Latin isolation go through these filters
only, never by hand in a template (DESIGN_PROMPT ground rules).
"""

import json
import re
from datetime import date

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

_TO_PERSIAN = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
_TO_ASCII = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")

# A run of Latin letters, digits stuck to them, and the spaces/punctuation
# between Latin words ("Lung Cancer", "COVID-19"), but never a trailing space.
_LATIN_RUN = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:[ .\-/&+][A-Za-z0-9]+)*")


@register.filter
def fa_digits(value):
    """1378 → ۱۳۷۸. None and "" render as nothing."""
    if value is None:
        return ""
    return str(value).translate(_TO_PERSIAN)


def ascii_digits(value):
    """Keep only the digits of a phone number, as ASCII: «۰۹۱۱ ۹۹۷-۰۸۲۸» → 09119970828."""
    return re.sub(r"\D", "", str(value or "").translate(_TO_ASCII))


@register.filter
def tel_href(value):
    """A `tel:` link in international form with ASCII digits."""
    digits = ascii_digits(value)
    if digits.startswith("0") and len(digits) == 11:
        digits = "+98" + digits[1:]
    return "tel:" + digits


@register.filter
def phone_display(value):
    """Iranian numbers grouped the way they're read aloud, in Persian digits:
    landline ۰۱۱-۴۴۲۲۹۲۷۰, mobile ۰۹۱۱ ۹۹۷ ۰۸۲۸. Anything else as typed."""
    digits = ascii_digits(value)
    if len(digits) == 11 and digits.startswith("09"):
        shown = f"{digits[:4]} {digits[4:7]} {digits[7:]}"
    elif len(digits) == 11 and digits.startswith("0"):
        shown = f"{digits[:3]}-{digits[3:]}"
    else:
        shown = str(value or "")
    return fa_digits(shown)


@register.filter(needs_autoescape=True)
def isolate_latin(value, autoescape=True):
    """Wrap each Latin run in <bdi> so mixed sentences stay readable in RTL."""
    text = conditional_escape(value) if autoescape else str(value)
    # Entities such as &lt; must not be split, so skip them while wrapping.
    parts = re.split(r"(&[#\w]+;)", str(text))
    out = []
    for part in parts:
        if part.startswith("&") and part.endswith(";"):
            out.append(part)
        else:
            out.append(_LATIN_RUN.sub(lambda m: f"<bdi>{m.group(0)}</bdi>", part))
    return mark_safe("".join(out))


def solar_hijri_year(day):
    """The Solar Hijri (Jalali) year a Gregorian date falls in.

    The arithmetic calendar (jdf.scr.ir's conversion), exact for 1300–1500.
    """
    g_days_before = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    gy = day.year - 1600
    days = (
        365 * gy + (gy + 3) // 4 - (gy + 99) // 100 + (gy + 399) // 400
        + g_days_before[day.month - 1] + day.day - 1
    )
    if day.month > 2 and (day.year % 4 == 0 and (day.year % 100 != 0 or day.year % 400 == 0)):
        days += 1
    days -= 79
    j_np = days // 12053
    days %= 12053
    jy = 979 + 33 * j_np + 4 * (days // 1461)
    days %= 1461
    if days >= 366:
        jy += (days - 1) // 365
    return jy


@register.filter
def years_since(year, today=None):
    """Whole Solar Hijri years since `year` (practising_since → experience)."""
    if not year:
        return None
    return solar_hijri_year(today or date.today()) - int(year)


@register.filter
def paragraphs(value):
    """Split free text on blank lines into its paragraphs."""
    text = str(value or "").replace("\r\n", "\n")
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


_SENTENCE_END = re.compile(r"(.+?[.؟!])\s+(.+)", re.S)
_YEAR = re.compile(r"(?<![0-9۰-۹])(1[34][0-9]{2}|۱[۳۴][۰-۹]{2})(?![0-9۰-۹])")


@register.filter
def lead_sentence(value):
    """{lead, rest}: the opening sentence of a paragraph, and what follows."""
    text = str(value or "").strip()
    match = _SENTENCE_END.match(text)
    if not match:
        return {"lead": text, "rest": ""}
    return {"lead": match.group(1), "rest": match.group(2)}


@register.filter
def first_year(value):
    """The first Solar Hijri year (13xx/14xx) in a text, in Persian digits, or ""."""
    match = _YEAR.search(str(value or "").translate(_TO_ASCII))
    return fa_digits(match.group(1)) if match else ""


@register.filter
def body_sections(value):
    """Split a condition body into sections at lines starting with `## `.

    Text before the first heading is an untitled section. Each section is a
    dict: `id` (an anchor for the "on this page" index, "" when untitled),
    `heading` (None when untitled) and `paragraphs`.
    """
    text = str(value or "").replace("\r\n", "\n")
    sections = []
    heading, lines = None, []

    def close():
        body = paragraphs("\n".join(lines))
        if heading is not None or body:
            n = sum(1 for s in sections if s["heading"] is not None)
            sections.append({
                "id": f"section-{n + 1}" if heading is not None else "",
                "heading": heading,
                "paragraphs": body,
            })

    for line in text.split("\n"):
        if line.startswith("## "):
            close()
            heading, lines = line[3:].strip(), []
        else:
            lines.append(line)
    close()
    return sections


def _json_ld_script(data):
    payload = json.dumps(data, ensure_ascii=False, indent=None)
    # Never let content close the script element early.
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return mark_safe(f'<script type="application/ld+json">{payload}</script>')


def _absolute(site_url, url):
    return url if url.startswith("http") else site_url + url


@register.simple_tag
def physician_json_ld(profile, locations, site_url):
    """`Physician` with one `MedicalClinic` per Clinic Location, as a JSON-LD
    script. Optional facts (council number, Paziresh24) appear once entered."""
    if not profile:
        return ""
    data = {
        "@context": "https://schema.org",
        "@type": "Physician",
        "name": profile.full_name,
        "url": site_url + "/",
        "image": _absolute(site_url, profile.photo_url),
        "medicalSpecialty": "Pulmonary",
    }
    if profile.intro_tagline:
        data["description"] = profile.intro_tagline
    if profile.medical_council_number:
        data["identifier"] = {
            "@type": "PropertyValue",
            "propertyID": "شماره نظام پزشکی",
            "value": profile.medical_council_number,
        }
    if profile.paziresh24_url:
        data["sameAs"] = [profile.paziresh24_url]
    if locations:
        data["telephone"] = tel_href(locations[0].phone).removeprefix("tel:")
    clinics = []
    for location in locations:
        clinic = {
            "@type": "MedicalClinic",
            "name": location.name,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": location.address,
                "addressCountry": "IR",
            },
            "telephone": tel_href(location.phone).removeprefix("tel:"),
            "openingHours": location.hours,
        }
        if location.map_url:
            clinic["hasMap"] = location.map_url
        clinics.append(clinic)
    data["location"] = clinics
    return _json_ld_script(data)


@register.simple_tag
def medical_entity_json_ld(item, site_url):
    """`MedicalCondition` for a Condition Treated, `MedicalProcedure` for a
    Procedure Performed, as a JSON-LD script."""
    kind = "MedicalProcedure" if item.category == "procedure" else "MedicalCondition"
    return _json_ld_script({
        "@context": "https://schema.org",
        "@type": kind,
        "name": item.title,
        "description": item.short_description,
        "url": f"{site_url}/conditions/{item.slug}/",
    })
