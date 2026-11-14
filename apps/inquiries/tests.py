from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Inquiry


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
