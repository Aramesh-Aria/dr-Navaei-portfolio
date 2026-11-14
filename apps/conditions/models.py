from django.db import models


class ConditionTreated(models.Model):
    """Holds two domain concepts (see CONTEXT.md: Condition Treated vs.
    Procedure Performed) in one table — `category` is the only real
    variation between them, so a second model would be a seam with
    nothing behind it."""

    CATEGORY_CONDITION = "condition"
    CATEGORY_PROCEDURE = "procedure"
    CATEGORY_CHOICES = [
        (CATEGORY_CONDITION, "بیماری"),
        (CATEGORY_PROCEDURE, "اقدام درمانی"),
    ]

    category = models.CharField(
        "دسته", max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_CONDITION
    )
    title = models.CharField("نام", max_length=200)
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
