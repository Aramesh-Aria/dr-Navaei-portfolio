from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0002_seed_location"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cliniclocation",
            old_name="whatsapp_number",
            new_name="mobile_phone",
        ),
        migrations.AlterField(
            model_name="cliniclocation",
            name="phone",
            field=models.CharField(max_length=50, verbose_name="تلفن ثابت"),
        ),
        migrations.AlterField(
            model_name="cliniclocation",
            name="mobile_phone",
            field=models.CharField(blank=True, max_length=50, verbose_name="تلفن همراه"),
        ),
    ]
