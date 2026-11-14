from django.db import migrations

FULL_NAME = "دکتر سپیده صفانوایی"

BIO = (
    "دکتر سپیده صفانوایی فارغ‌التحصیل تخصص داخلی در سال ۱۳۷۸ است. دوران طرح تخصصی را "
    "به مدت ۲ سال در منطقه محروم کهگیلویه گذراند و پس از آن به دیار اصلی خود، آمل، "
    "بازگشت و به مدت ۸ سال مسئول بخش دیابت آمل در بیمارستان امام رضا مشغول به کار شد.\n\n"
    "در طی این ۸ سال، مرکز دیابت آمل جزو ۵ مرکز برتر و ریفرال کشوری شناخته شد و بارها "
    "توسط ریاست دانشگاه و بازرسین کشوری به علت اجرای استاندارد جهانی دیابت مورد تشویق "
    "قرار گرفت.\n\n"
    "پس از آن، برای ادامه تحصیل در رشته فوق تخصصی ریه، در سال ۱۳۸۵ وارد دانشگاه علوم "
    "پزشکی شهید بهشتی شد و به مدت ۲ سال در بیمارستان مسیح دانشوری مشغول به کار و تحصیل "
    "بود. در سال ۱۳۸۷ با مدرک فوق تخصصی ریه و ICU به شهر آمل بازگشت.\n\n"
    "در سال ۱۳۹۰ مجدداً به مدت ۵ سال برای گذراندن دوره اینترونشن فوق تخصصی ریه به "
    "بیمارستان مسیح دانشوری مراجعه کرد و این دوره را در همان بیمارستان به پایان رساند.\n\n"
    "از سال ۱۳۹۵ به عنوان هیات علمی با دانشگاه علوم پزشکی مازندران در ساعات صبح همکاری "
    "می‌کند و روزانه در شیفت عصر، در مطب شخصی خود در شهر آمل، پذیرای بیماران داخلی، "
    "دیابت و ریوی است.\n\n"
    "ایشان از سال ۱۳۸۷ عضو انجمن علمی ریه اروپا (ERS)، انجمن علمی ریه آمریکا (ATS) و "
    "انجمن علمی ریه ایران است و تاکنون بالغ بر ۳۰ مقاله علمی و ۲ کتاب نوشته است که در "
    "مجلات معتبر خارجی به چاپ رسیده‌اند."
)

INTRO_TAGLINE = "متخصص داخلی و فوق تخصص بیماری‌های ریه"

CREDENTIALS = [
    {"title": "متخصص داخلی", "institution": "دانشگاه علوم پزشکی شهید بهشتی، تهران", "year": 1378, "order": 10},
    {"title": "فوق تخصص بیماری‌های ریه و ICU", "institution": "دانشگاه علوم پزشکی شهید بهشتی - بیمارستان مسیح دانشوری", "year": 1387, "order": 20},
    {"title": "دوره تخصصی اینترونشن ریه", "institution": "بیمارستان مسیح دانشوری", "year": 1395, "order": 30},
    {"title": "هیات علمی", "institution": "دانشگاه علوم پزشکی مازندران", "year": 1395, "order": 40},
    {"title": "عضو انجمن علمی ریه اروپا (ERS)", "institution": "", "year": 1387, "order": 50},
    {"title": "عضو انجمن علمی ریه آمریکا (ATS)", "institution": "", "year": 1387, "order": 60},
    {"title": "عضو انجمن علمی ریه ایران", "institution": "", "year": 1387, "order": 70},
    {"title": "بیش از ۳۰ مقاله علمی و ۲ کتاب در مجلات معتبر خارجی", "institution": "", "year": None, "order": 80},
]


def seed(apps, schema_editor):
    DoctorProfile = apps.get_model("doctor", "DoctorProfile")
    Credential = apps.get_model("doctor", "Credential")

    profile, _ = DoctorProfile.objects.get_or_create(
        full_name=FULL_NAME,
        defaults={"bio": BIO, "intro_tagline": INTRO_TAGLINE},
    )
    profile.bio = BIO
    profile.intro_tagline = INTRO_TAGLINE
    profile.save()

    for item in CREDENTIALS:
        Credential.objects.get_or_create(
            profile=profile,
            title=item["title"],
            defaults={
                "institution": item["institution"],
                "year": item["year"],
                "order": item["order"],
            },
        )


def unseed(apps, schema_editor):
    DoctorProfile = apps.get_model("doctor", "DoctorProfile")
    DoctorProfile.objects.filter(full_name=FULL_NAME).delete()  # cascades to Credential


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
