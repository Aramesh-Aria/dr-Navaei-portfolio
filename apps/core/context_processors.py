from django.conf import settings

from apps.core.templatetags.site import lead_sentence
from apps.doctor.models import DoctorProfile
from apps.locations.models import ClinicLocation


def site(request):
    """What every public page needs: the Doctor Profile, every Clinic Location
    (the first one is the primary phone), and the defaults for meta tags."""
    if request.path.startswith("/admin/"):
        return {"clinic_word": "مطب"}  # a 404 under /admin/ still renders the public nav
    profile = DoctorProfile.objects.first()
    locations = list(ClinicLocation.objects.all())
    description = ""
    if profile:
        description = profile.intro_tagline or lead_sentence(profile.bio)["lead"]
        if locations:
            description += "؛ " + "، ".join(l.name for l in locations)
    return {
        "profile": profile,
        "locations": locations,
        "primary_location": locations[0] if locations else None,
        # «مطب» or «مطب‌ها»: every label that names the clinics follows the count.
        "clinic_word": "مطب‌ها" if len(locations) > 1 else "مطب",
        # Links to /locations/ promise «و مسیر» only when a map link exists.
        "has_route": any(l.map_url for l in locations),
        "site_url": settings.SITE_URL,
        "default_description": description[:200],
    }
