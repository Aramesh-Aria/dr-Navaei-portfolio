from django.db import models


class ClinicLocation(models.Model):
    name = models.CharField("نام مطب یا محل", max_length=200)
    address = models.TextField("آدرس")
    phone = models.CharField("تلفن ثابت", max_length=50)
    mobile_phone = models.CharField("تلفن همراه", max_length=50, blank=True)
    map_url = models.URLField("لینک نقشه", blank=True)
    hours = models.TextField("ساعات کاری")
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "مطب"
        verbose_name_plural = "مطب‌ها"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
