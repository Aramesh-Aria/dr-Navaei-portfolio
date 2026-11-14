import re

from django.conf import settings

from apps.doctor.models import DoctorProfile
from apps.locations.models import ClinicLocation


def _first_sentence(text):
    match = re.match(r"(.+?[.؟!])(\s|$)", text or "", re.S)
    return (match.group(1) if match else text or "").strip()


def site(request):
    """What every public page needs: the Doctor Profile, every Clinic Location
    (the first one is the primary phone), and the defaults for meta tags."""
    if request.path.startswith("/admin/"):
        return {}
    profile = DoctorProfile.objects.first()
    locations = list(ClinicLocation.objects.all())
    description = ""
    if profile:
        description = profile.intro_tagline or _first_sentence(profile.bio)
        if locations:
            description += "؛ " + "، ".join(l.name for l in locations)
    return {
        "profile": profile,
        "locations": locations,
        "primary_location": locations[0] if locations else None,
        "site_url": settings.SITE_URL,
        "default_description": description[:200],
    }
