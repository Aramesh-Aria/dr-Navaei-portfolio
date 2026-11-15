import re

from django import forms

from apps.core.templatetags.site import ascii_digits

from .models import Inquiry

# One example, written without spaces or dashes: a grouped number beside
# Persian text is reordered by bidi in a plain-text message.
PHONE_INVALID = "این شماره تلفن درست نیست. شماره را ۱۱ رقمی و با صفر اول بنویسید؛ مثلاً ۰۹۱۱۱۲۳۴۵۶۷."


def normalise_phone(value):
    """«۰۹۱۱ ۹۹۷-۰۸۲۸», «+98 911 997 0828» → "09119970828"; None if it isn't
    an 11-digit Iranian number (mobile or landline with its area code)."""
    if re.search(r"[^\d\s\-+()٠-٩۰-۹]", value):
        return None
    digits = ascii_digits(value)
    if digits.startswith("0098"):
        digits = "0" + digits[4:]
    elif digits.startswith("98") and len(digits) == 12:
        digits = "0" + digits[2:]
    return digits if re.fullmatch(r"0\d{10}", digits) else None


class InquiryForm(forms.ModelForm):
    """The contact form. No medical-detail field, by design."""

    message = forms.CharField(
        label="پیام", required=False, max_length=2000,
        help_text="لطفاً شرح بیماری را این‌جا ننویسید؛ آن را در ویزیت بگویید.",
        widget=forms.Textarea(attrs={"rows": 4}),
    )

    class Meta:
        model = Inquiry
        fields = ["name", "phone", "preferred_contact_time", "message"]
        labels = {"name": "نام و نام خانوادگی", "phone": "شماره تلفن"}
        # Shown above each field and announced with it (aria-describedby).
        help_texts = {
            "phone": "همراه یا ثابت، با پیش‌شماره. رقم فارسی یا انگلیسی، هر دو درست است.",
            "preferred_contact_time": "مثلاً «عصرها» یا «شنبه صبح».",
        }
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "phone": forms.TextInput(
                attrs={"autocomplete": "tel", "inputmode": "tel", "dir": "ltr"}
            ),
            "preferred_contact_time": forms.TextInput(attrs={"autocomplete": "off"}),
        }
        error_messages = {
            "name": {"required": "لطفاً نام خود را بنویسید."},
            "phone": {"required": "لطفاً یک شماره تلفن بنویسید تا مطب بتواند با شما تماس بگیرد."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.help_text:
                field.widget.attrs["aria-describedby"] = f"id_{name}_hint"
            if field.required:
                field.widget.attrs["aria-required"] = "true"

    def full_clean(self):
        super().full_clean()
        # Point each invalid field at its error, after its hint.
        for name in self.errors:
            if name not in self.fields:
                continue
            attrs = self.fields[name].widget.attrs
            attrs["aria-invalid"] = "true"
            attrs["aria-describedby"] = " ".join(
                filter(None, [attrs.get("aria-describedby"), f"id_{name}_error"])
            )

    def clean_phone(self):
        phone = normalise_phone(self.cleaned_data["phone"])
        if phone is None:
            raise forms.ValidationError(PHONE_INVALID, code="invalid")
        return phone
