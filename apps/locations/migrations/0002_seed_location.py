from django.db import migrations

NAME = "مطب آمل"
ADDRESS = "آمل، سبزه میدان، روبروی مخابرات مرکزی، ساختمان پزشکان آنیتا، طبقه اول، واحد ۳"
PHONE = "01144229270"
# The asset text calls this a mobile number ("همراه"), not explicitly WhatsApp —
# stored here as the closest fit; confirm with the doctor before relying on it
# as an actual WhatsApp contact channel for the Phase 4 contact-form link.
WHATSAPP_NUMBER = "09119970828"
HOURS = "پذیرش بیماران: روزانه، شیفت عصر"


def seed(apps, schema_editor):
    ClinicLocation = apps.get_model("locations", "ClinicLocation")
    ClinicLocation.objects.get_or_create(
        name=NAME,
        defaults={
            "address": ADDRESS,
            "phone": PHONE,
            "whatsapp_number": WHATSAPP_NUMBER,
            "hours": HOURS,
            "order": 0,
        },
    )


def unseed(apps, schema_editor):
    ClinicLocation = apps.get_model("locations", "ClinicLocation")
    ClinicLocation.objects.filter(name=NAME).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
