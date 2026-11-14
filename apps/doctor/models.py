from django.db import models
from django.templatetags.static import static

from . import images


class DoctorProfile(models.Model):
    """Singleton — see the admin's singleton guard in admin.py."""

    full_name = models.CharField("نام و نام خانوادگی", max_length=200)
    intro_tagline = models.CharField(
        "جمله کوتاه معرفی (صفحه اصلی)", max_length=200, blank=True
    )
    bio = models.TextField("بیوگرافی")
    photo = models.ImageField("عکس", upload_to="doctor/", blank=True, null=True)
    medical_council_number = models.CharField(
        "شماره نظام پزشکی", max_length=20, blank=True,
        help_text="همان شماره‌ای که بیماران با آن پزشک را استعلام می‌کنند",
    )
    practising_since = models.PositiveIntegerField(
        "سال شروع طبابت (شمسی)", null=True, blank=True,
        help_text="مثلا ۱۳۷۸ — سال‌های تجربه از روی همین سال حساب می‌شود",
    )
    paziresh24_url = models.URLField(
        "لینک پروفایل پذیرش۲۴", blank=True,
        help_text="فقط برای لینک بیرونی؛ نظرها در سایت کپی نمی‌شوند",
    )

    class Meta:
        verbose_name = "پروفایل پزشک"
        verbose_name_plural = "پروفایل پزشک"

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # A new upload has no resized copies yet; make them once.
        if self.photo and not images.variant_url(self.photo, images.WIDTHS[-1]):
            images.make_variants(self.photo)

    @property
    def photo_url(self):
        """The photo every template renders: the 1200px WebP copy, the
        original if no copy exists, or the lungs-mark placeholder."""
        if self.photo:
            return images.variant_url(self.photo, images.WIDTHS[-1]) or self.photo.url
        return static("doctor/doctor-placeholder.svg")

    @property
    def photo_srcset(self):
        """`srcset` for the resized copies, or "" (placeholder, unprocessed photo)."""
        if not self.photo:
            return ""
        urls = [(images.variant_url(self.photo, w), w) for w in images.WIDTHS]
        if not all(url for url, _ in urls):
            return ""
        return ", ".join(f"{url} {w}w" for url, w in urls)


class Credential(models.Model):
    profile = models.ForeignKey(
        DoctorProfile, related_name="credentials", on_delete=models.CASCADE,
        verbose_name="پروفایل پزشک",
    )
    title = models.CharField("عنوان", max_length=200)
    institution = models.CharField("موسسه یا دانشگاه", max_length=200, blank=True)
    year = models.PositiveIntegerField("سال", null=True, blank=True)
    detail = models.TextField(
        "توضیح بیشتر (پشت کارت)", blank=True,
        help_text="اختیاری؛ در پشت کارت سوابق، زیر نام موسسه نمایش داده می‌شود",
    )
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "مدرک یا سابقه"
        verbose_name_plural = "مدارک و سوابق"
        ordering = ["order", "-year"]

    def __str__(self):
        return self.title
