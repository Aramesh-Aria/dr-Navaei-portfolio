from django.db import models


class DoctorProfile(models.Model):
    """Singleton — see the admin's singleton guard in admin.py."""

    full_name = models.CharField("نام و نام خانوادگی", max_length=200)
    intro_tagline = models.CharField(
        "جمله کوتاه معرفی (صفحه اصلی)", max_length=200, blank=True
    )
    bio = models.TextField("بیوگرافی")
    photo = models.ImageField("عکس", upload_to="doctor/", blank=True, null=True)

    class Meta:
        verbose_name = "پروفایل پزشک"
        verbose_name_plural = "پروفایل پزشک"

    def __str__(self):
        return self.full_name


class Credential(models.Model):
    profile = models.ForeignKey(
        DoctorProfile, related_name="credentials", on_delete=models.CASCADE,
        verbose_name="پروفایل پزشک",
    )
    title = models.CharField("عنوان", max_length=200)
    institution = models.CharField("موسسه یا دانشگاه", max_length=200, blank=True)
    year = models.PositiveIntegerField("سال", null=True, blank=True)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "مدرک یا سابقه"
        verbose_name_plural = "مدارک و سوابق"
        ordering = ["order", "-year"]

    def __str__(self):
        return self.title
