from django.db import migrations

# Starter copy only — brief and factual on purpose. Dr. Safanavaei (or her
# daughter, under her guidance) should review/edit every one of these
# through the admin before the site goes live; none of this is meant to
# stand as final clinical copy written without her review.

CONDITIONS = [
    {"slug": "asthma", "title": "آسم", "short_description": "تشخیص و درمان آسم در کودکان و بزرگسالان", "body": "آسم یک بیماری التهابی مزمن راه‌های هوایی ریه است که با تنگی نفس، خس‌خس سینه و سرفه همراه می‌شود. تشخیص و کنترل آسم در مطب دکتر صفانوایی ارائه می‌شود."},
    {"slug": "copd", "title": "COPD (بیماری انسدادی مزمن ریه)", "short_description": "تشخیص و درمان بیماری انسدادی مزمن ریه", "body": "COPD گروهی از بیماری‌های ریوی است که باعث محدودیت در عبور هوا می‌شود و معمولاً با سابقه مصرف سیگار یا مواجهه شغلی مرتبط است. مدیریت و درمان دارویی آن در این مطب انجام می‌شود."},
    {"slug": "occupational-lung-disease", "title": "بیماری‌های شغلی ریه", "short_description": "بیماری‌های ریوی ناشی از مواجهه شغلی", "body": "برخی مشاغل با مواجهه با گرد و غبار، مواد شیمیایی یا آلاینده‌ها می‌توانند به بیماری‌های ریوی منجر شوند. ارزیابی و پیگیری این بیماری‌ها در این مطب صورت می‌گیرد."},
    {"slug": "smoking-related-lung-disease", "title": "بیماری‌های ریوی ناشی از سیگار", "short_description": "بیماری‌های ریوی ناشی از مصرف سیگار", "body": "مصرف سیگار یکی از مهم‌ترین عوامل خطر بیماری‌های ریوی از جمله COPD و کانسر ریه است. ارزیابی و درمان این بیماری‌ها در این مطب انجام می‌شود."},
    {"slug": "lung-infections", "title": "بیماری‌های عفونی ریه", "short_description": "تشخیص و درمان بیماری‌های عفونی ریه", "body": "عفونت‌های ریوی مانند پنومونی و برونشیت حاد می‌توانند علل مختلفی داشته باشند. تشخیص و درمان این عفونت‌ها در این مطب ارائه می‌شود."},
    {"slug": "bronchitis", "title": "برونشیت", "short_description": "تشخیص و درمان برونشیت حاد و مزمن", "body": "برونشیت التهاب راه‌های هوایی ریه است که می‌تواند حاد یا مزمن باشد. درمان دارویی و پیگیری آن در این مطب انجام می‌شود."},
    {"slug": "lung-allergies", "title": "حساسیت‌های ریوی", "short_description": "تشخیص و درمان حساسیت‌های ریوی", "body": "حساسیت‌های تنفسی می‌توانند باعث سرفه، تنگی نفس و خس‌خس سینه شوند. بررسی و درمان این حساسیت‌ها در این مطب انجام می‌شود."},
    {"slug": "pulmonary-fibrosis", "title": "فیبروز ریه", "short_description": "تشخیص و پیگیری فیبروز ریه", "body": "فیبروز ریه به سخت و ضخیم شدن بافت ریه گفته می‌شود که تنفس را دشوار می‌کند. ارزیابی و پیگیری درمانی آن در این مطب ارائه می‌شود."},
    {"slug": "rheumatologic-lung-disease", "title": "بیماری‌های روماتیسمی ریه", "short_description": "بیماری‌های ریوی مرتبط با بیماری‌های روماتیسمی", "body": "برخی بیماری‌های روماتیسمی می‌توانند ریه را نیز درگیر کنند. ارزیابی و پیگیری درگیری ریوی این بیماری‌ها در این مطب انجام می‌شود."},
    {"slug": "lung-cancer", "title": "کانسرهای ریه", "short_description": "تشخیص و پیگیری کانسرهای ریه", "body": "تشخیص زودهنگام و پیگیری درمانی کانسرهای ریه، از جمله با کمک اقدامات تشخیصی تخصصی مانند برونکوسکوپی، در این مطب ارائه می‌شود."},
    {"slug": "pleural-disease", "title": "بیماری‌های پرده پلور", "short_description": "تشخیص و درمان بیماری‌های پرده پلور", "body": "بیماری‌های پرده پلور از جمله تجمع مایع یا هوا در فضای پلور می‌توانند باعث تنگی نفس شوند. تشخیص و درمان این بیماری‌ها، در صورت نیاز با تعبیه کاتتر پلور، در این مطب انجام می‌شود."},
    {"slug": "shortness-of-breath", "title": "تنگی نفس", "short_description": "بررسی علت تنگی نفس", "body": "تنگی نفس می‌تواند علل مختلف ریوی یا قلبی داشته باشد. بررسی و تشخیص علت تنگی نفس در این مطب ارائه می‌شود."},
    {"slug": "chronic-cough", "title": "سرفه مزمن", "short_description": "بررسی علت سرفه مزمن", "body": "سرفه مزمن می‌تواند نشانه بیماری‌های مختلف ریوی، گوارشی یا آلرژیک باشد. بررسی و درمان آن در این مطب انجام می‌شود."},
    {"slug": "diabetes", "title": "دیابت", "short_description": "تشخیص و پیگیری دیابت", "body": "دکتر صفانوایی با سابقه ۸ ساله مسئولیت بخش دیابت آمل، تشخیص و پیگیری درمانی بیماران دیابتی را در این مطب ارائه می‌دهد."},
    {"slug": "gi-disorders", "title": "بیماری‌های گوارشی", "short_description": "بررسی و درمان بیماری‌های گوارشی", "body": "ارزیابی و درمان علائم و بیماری‌های گوارشی نیز در کنار سایر بیماری‌های داخلی در این مطب ارائه می‌شود."},
]

PROCEDURES = [
    {"slug": "bronchoscopy", "title": "برونکوسکوپی", "short_description": "برونکوسکوپی تشخیصی و درمانی", "body": "برونکوسکوپی روشی برای مشاهده مستقیم راه‌های هوایی ریه و انجام اقدامات تشخیصی یا درمانی است."},
    {"slug": "pleuroscopy", "title": "پلوروسکوپی", "short_description": "پلوروسکوپی تشخیصی", "body": "پلوروسکوپی روشی برای بررسی فضای پرده پلور و تشخیص علت بیماری‌های آن است."},
    {"slug": "airway-stent", "title": "استنت راه هوایی ریه", "short_description": "تعبیه استنت راه هوایی ریه", "body": "در موارد تنگی راه هوایی، تعبیه استنت ریه می‌تواند به باز نگه‌داشتن راه هوایی کمک کند."},
    {"slug": "bronchial-tumor-ablation", "title": "Ablation تومورهای برونکیال ریه", "short_description": "Ablation تومورهای داخل راه هوایی", "body": "در برخی تومورهای داخل راه هوایی، روش‌های ablation برای کوچک کردن یا از بین بردن تومور به کار می‌روند."},
    {"slug": "pleural-catheter", "title": "تعبیه کاتتر پلور", "short_description": "تعبیه کاتتر پلور برای تجمع مزمن مایع پلور", "body": "در موارد تجمع مزمن مایع پلور، تعبیه کاتتر پلور می‌تواند تنفس بیمار را تسکین دهد."},
]


def seed(apps, schema_editor):
    ConditionTreated = apps.get_model("conditions", "ConditionTreated")
    for order, item in enumerate(CONDITIONS, start=1):
        ConditionTreated.objects.get_or_create(
            slug=item["slug"],
            defaults={
                "category": "condition",
                "title": item["title"],
                "short_description": item["short_description"],
                "body": item["body"],
                "order": order,
            },
        )
    for order, item in enumerate(PROCEDURES, start=1):
        ConditionTreated.objects.get_or_create(
            slug=item["slug"],
            defaults={
                "category": "procedure",
                "title": item["title"],
                "short_description": item["short_description"],
                "body": item["body"],
                "order": order,
            },
        )


def unseed(apps, schema_editor):
    ConditionTreated = apps.get_model("conditions", "ConditionTreated")
    slugs = [item["slug"] for item in CONDITIONS + PROCEDURES]
    ConditionTreated.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("conditions", "0002_conditiontreated_category_and_more"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
