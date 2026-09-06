from django.db import models


class ConditionTreated(models.Model):
    title = models.CharField("نام بیماری", max_length=200)
    slug = models.SlugField(
        "اسلاگ (بخش انگلیسی آدرس صفحه)",
        unique=True,
        help_text="فقط حروف انگلیسی کوچک، عدد و خط تیره — مثلا asthma",
    )
    short_description = models.CharField("توضیح کوتاه (برای لیست)", max_length=300)
    body = models.TextField("توضیح کامل")
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)
    is_published = models.BooleanField("نمایش داده شود", default=True)

    class Meta:
        verbose_name = "بیماری"
        verbose_name_plural = "بیماری‌های تحت درمان"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title
