from unittest import mock

from captcha.models import CaptchaStore
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Inquiry


def solved_captcha():
    """A real captcha with its right answer, as the form's POST fields."""
    key = CaptchaStore.generate_key()
    return {"captcha_0": key, "captcha_1": CaptchaStore.objects.get(hashkey=key).response}


class InquiryAdminTests(TestCase):
    """Inquiries only come from patients via the contact form (Phase 4);
    the Content Editor reads them and marks them read, nothing more."""

    def setUp(self):
        user = get_user_model().objects.create_superuser("editor", "", "pw")
        self.client.force_login(user)
        self.inquiry = Inquiry.objects.create(
            name="بیمار", phone="09120000000", message="سلام"
        )

    def test_inquiry_cannot_be_created_from_admin(self):
        response = self.client.get(reverse("admin:inquiries_inquiry_add"))
        self.assertEqual(response.status_code, 403)

    def test_patient_message_cannot_be_altered_from_admin(self):
        url = reverse("admin:inquiries_inquiry_change", args=[self.inquiry.pk])
        self.client.post(url, {"name": "تغییر", "phone": "0", "is_read": "on"})
        self.inquiry.refresh_from_db()
        self.assertEqual(self.inquiry.name, "بیمار")
        self.assertTrue(self.inquiry.is_read)

    def test_honeypot_field_is_hidden_from_admin_form(self):
        url = reverse("admin:inquiries_inquiry_change", args=[self.inquiry.pk])
        response = self.client.get(url)
        self.assertNotContains(response, 'name="website"')

    def test_newest_inquiries_come_first(self):
        newer = Inquiry.objects.create(name="دوم", phone="1")
        self.assertEqual(Inquiry.objects.first(), newer)


class ContactPageTests(TestCase):
    """`/contact/`: the clinic's phones first, then the Inquiry form."""

    def test_contact_page_shows_the_form_with_labelled_fields(self):
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        for field in ("name", "phone", "preferred_contact_time", "message"):
            self.assertRegex(html, rf'<label[^>]+for="id_{field}"')
        self.assertIn('autocomplete="tel"', html)
        self.assertIn('inputmode="tel"', html)

    def post(self, **fields):
        data = {"name": "مریم احمدی", "phone": "09121234567", "preferred_contact_time": "", "message": ""}
        data.update(solved_captcha(), **fields)
        return self.client.post("/contact/", data, follow=True)

    def test_a_sent_inquiry_is_saved_and_confirmed_once(self):
        response = self.post(preferred_contact_time="عصرها", message="برای نوبت")
        self.assertRedirects(response, "/contact/")
        inquiry = Inquiry.objects.get()
        self.assertEqual(
            (inquiry.name, inquiry.phone, inquiry.preferred_contact_time, inquiry.message, inquiry.is_read),
            ("مریم احمدی", "09121234567", "عصرها", "برای نوبت", False),
        )
        self.assertContains(response, "پیام شما رسید")
        self.assertNotContains(self.client.get("/contact/"), "پیام شما رسید")

    def test_a_phone_typed_with_persian_digits_spaces_or_dashes_is_saved_as_ascii_digits(self):
        for typed, saved in (
            ("۰۹۱۱ ۹۹۷-۰۸۲۸", "09119970828"),
            ("+98 911 997 0828", "09119970828"),
            ("011-44229270", "01144229270"),
            ("٠٩١١٩٩٧٠٨٢٨", "09119970828"),  # Arabic-Indic digits, from some keyboards
        ):
            with self.subTest(typed=typed):
                Inquiry.objects.all().delete()
                self.post(phone=typed)
                self.assertEqual(Inquiry.objects.get().phone, saved)

    def test_missing_name_and_phone_are_reported_in_persian_beside_their_fields(self):
        response = self.client.post("/contact/", {"name": " ", "phone": ""})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Inquiry.objects.exists())
        html = response.content.decode()
        self.assertIn("لطفاً نام خود را بنویسید.", html)
        self.assertIn("لطفاً یک شماره تلفن بنویسید", html)
        self.assertRegex(html, r'id="id_phone"[^>]*aria-invalid="true"|aria-invalid="true"[^>]*id="id_phone"')
        self.assertRegex(html, r'aria-describedby="[^"]*id_phone_error')

    def test_a_phone_that_is_not_a_number_is_refused_and_kept_as_typed(self):
        for typed in ("۱۲۳", "abc", "0912123456789"):
            with self.subTest(typed=typed):
                response = self.client.post("/contact/", {"name": "مریم", "phone": typed})
                self.assertContains(response, "شماره تلفن درست نیست")
                self.assertContains(response, f'value="{typed}"')
        self.assertFalse(Inquiry.objects.exists())

    def test_a_filled_honeypot_is_dropped_silently(self):
        response = self.post(website="http://spam.example")
        self.assertFalse(Inquiry.objects.exists())
        self.assertContains(response, "پیام شما رسید")  # a bot learns nothing

    def test_a_filled_honeypot_with_invalid_fields_still_gets_the_confirmation(self):
        # A bot that also fails validation (or the captcha) learns nothing either.
        response = self.client.post(
            "/contact/", {"name": "", "phone": "spam", "website": "http://spam.example"}, follow=True
        )
        self.assertFalse(Inquiry.objects.exists())
        self.assertContains(response, "پیام شما رسید")
        self.assertNotContains(response, "شماره تلفن درست نیست")

    def test_the_honeypot_is_hidden_from_people_and_screen_readers(self):
        html = self.client.get("/contact/").content.decode()
        self.assertRegex(html, r'<div class="form__trap" aria-hidden="true">')
        self.assertRegex(html, r'name="website"[^>]*tabindex="-1"')


class ContactCaptchaTests(TestCase):
    """The contact form asks for the letters of a server-drawn image."""

    def test_the_form_shows_a_labelled_captcha_with_a_new_image_button(self):
        html = self.client.get("/contact/").content.decode()
        self.assertRegex(html, r'<label for="id_captcha_1">کد امنیتی')
        self.assertRegex(html, r'<img src="/captcha/image/[0-9a-f]+/"[^>]*alt="تصویر کد امنیتی"')
        self.assertIn('data-captcha-refresh="/captcha/refresh/"', html)
        self.assertRegex(html, r'id="id_captcha_1"[^>]*aria-describedby="id_captcha_1_hint"|aria-describedby="id_captcha_1_hint"[^>]*id="id_captcha_1"')

    def test_the_captcha_image_is_served(self):
        key = CaptchaStore.generate_key()
        response = self.client.get(f"/captcha/image/{key}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")

    def test_a_wrong_code_is_refused_and_tied_to_the_captcha_box(self):
        key = CaptchaStore.generate_key()
        response = self.client.post(
            "/contact/", {"name": "مریم", "phone": "09121234567", "captcha_0": key, "captcha_1": "wrong"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Inquiry.objects.exists())
        html = response.content.decode()
        self.assertIn("کد امنیتی درست نیست", html)
        self.assertIn('id="id_captcha_1_error"', html)
        self.assertIn('href="#id_captcha_1"', html)  # the summary links to the box
        self.assertRegex(html, r'aria-describedby="id_captcha_1_hint id_captcha_1_error"')

    def test_a_missing_code_is_refused_with_a_message_that_names_it(self):
        response = self.client.post("/contact/", {"name": "مریم", "phone": "09121234567"})
        self.assertFalse(Inquiry.objects.exists())
        self.assertContains(response, "لطفاً کد امنیتی تصویر را بنویسید.")

    def test_anyone_who_cannot_read_the_image_is_offered_the_clinic_phone(self):
        # The image has no audio version: the phone is its alternative (WCAG 1.1.1).
        html = self.client.get("/contact/").content.decode()
        self.assertRegex(html, r'<p class="field__alt">اگر خواندن تصویر برایتان دشوار است[^<]*<a[^>]*href="tel:\+981144229270"')

    def test_the_image_is_drawn_at_twice_its_shown_size_for_sharp_phone_screens(self):
        from django.conf import settings

        self.assertEqual(settings.CAPTCHA_IMAGE_SIZE, (400, 140))
        self.assertRegex(self.client.get("/contact/").content.decode(), r'class="captcha__image" width="200" height="70"')

    def test_the_contact_form_carries_a_csrf_token(self):
        self.assertContains(self.client.get("/contact/"), 'name="csrfmiddlewaretoken"')

@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class InquiryEmailTests(TestCase):
    """An email goes out only when INQUIRY_NOTIFICATION_EMAIL is set, and
    email never stops an Inquiry from being saved."""

    def post(self):
        return self.client.post(
            "/contact/", {"name": "مریم", "phone": "۰۹۱۲۱۲۳۴۵۶۷", "message": "سلام", **solved_captcha()}
        )

    @override_settings(INQUIRY_NOTIFICATION_EMAIL="")
    def test_no_email_without_a_notification_address(self):
        self.post()
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(Inquiry.objects.count(), 1)

    @override_settings(INQUIRY_NOTIFICATION_EMAIL="clinic@example.com")
    def test_an_email_with_name_and_phone_goes_to_the_notification_address(self):
        self.post()
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, ["clinic@example.com"])
        self.assertIn("مریم", email.subject)
        self.assertIn("09121234567", email.body)
        self.assertIn("/admin/inquiries/inquiry/", email.body)

    @override_settings(INQUIRY_NOTIFICATION_EMAIL="clinic@example.com")
    def test_a_failing_email_still_saves_and_confirms(self):
        with mock.patch("apps.inquiries.views.send_mail", side_effect=OSError("smtp down")), \
                self.assertLogs("apps.inquiries.views", "ERROR"):
            response = self.client.post(
                "/contact/", {"name": "مریم", "phone": "09121234567", **solved_captcha()}, follow=True
            )
        self.assertEqual(Inquiry.objects.count(), 1)
        self.assertContains(response, "پیام شما رسید")

    @override_settings(INQUIRY_NOTIFICATION_EMAIL="clinic@example.com")
    def test_a_honeypot_submission_sends_no_email(self):
        self.client.post("/contact/", {"name": "x", "phone": "09121234567", "website": "x", **solved_captcha()})
        self.assertEqual(len(mail.outbox), 0)


class UnreadInquiryCountTests(TestCase):
    """The admin sidebar shows how many Inquiries are still unread."""

    def setUp(self):
        user = get_user_model().objects.create_superuser("editor", "", "pw")
        self.client.force_login(user)

    def test_the_unread_count_follows_the_inquiries_name(self):
        Inquiry.objects.create(name="الف", phone="1")
        Inquiry.objects.create(name="ب", phone="2")
        Inquiry.objects.create(name="ج", phone="3", is_read=True)
        self.assertContains(self.client.get(reverse("admin:index")), "پیام‌های بیماران (۲)")

    def test_no_count_when_everything_is_read(self):
        Inquiry.objects.create(name="الف", phone="1", is_read=True)
        response = self.client.get(reverse("admin:index"))
        self.assertContains(response, "پیام‌های بیماران")
        self.assertNotContains(response, "پیام‌های بیماران (")
