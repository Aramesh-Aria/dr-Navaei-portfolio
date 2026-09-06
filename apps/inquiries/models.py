from django.db import models


class Inquiry(models.Model):
    name = models.CharField("نام", max_length=200)
    phone = models.CharField("تلفن", max_length=50)
    preferred_contact_time = models.CharField(
        "زمان مناسب برای تماس", max_length=200, blank=True
    )
    message = models.TextField("پیام", blank=True)
    created_at = models.DateTimeField("تاریخ ارسال", auto_now_add=True)
    is_read = models.BooleanField("خوانده شده", default=False)

    # Honeypot (Q11 / docs/plan.md): hidden via CSS on the real form (Phase 4).
    # A filled value means a bot submitted it, not a patient — `editable=False`
    # also keeps it off the admin form, since staff never need to see it.
    website = models.CharField(max_length=200, blank=True, editable=False)

    class Meta:
        verbose_name = "پیام بیمار"
        verbose_name_plural = "پیام‌های بیماران"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.created_at:%Y-%m-%d}"
