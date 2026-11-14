from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ClinicLocation


class MultipleLocationsTests(TestCase):
    """The site starts with one clinic, but a second must be addable later
    from the admin alone, with no code change."""

    def setUp(self):
        user = get_user_model().objects.create_superuser("editor", "", "pw")
        self.client.force_login(user)

    def test_second_location_can_be_added_from_admin(self):
        response = self.client.post(
            reverse("admin:locations_cliniclocation_add"),
            {
                "name": "مطب دوم",
                "address": "ساری",
                "phone": "01100000000",
                "mobile_phone": "",
                "map_url": "",
                "hours": "صبح‌ها",
                "order": 1,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ClinicLocation.objects.count(), 2)

    def test_locations_follow_manual_order(self):
        ClinicLocation.objects.all().delete()
        ClinicLocation.objects.create(name="ب", address="-", phone="1", hours="-", order=2)
        ClinicLocation.objects.create(name="الف", address="-", phone="1", hours="-", order=1)
        self.assertEqual(
            [l.name for l in ClinicLocation.objects.all()], ["الف", "ب"]
        )

    def test_mobile_phone_and_map_link_are_optional(self):
        response = self.client.post(
            reverse("admin:locations_cliniclocation_add"),
            {"name": "مطب سوم", "address": "-", "phone": "1", "hours": "-", "order": 2},
        )
        self.assertEqual(response.status_code, 302)


class SeededLocationTests(TestCase):
    def test_amol_clinic_is_seeded_with_landline_and_mobile(self):
        clinic = ClinicLocation.objects.get(name="مطب آمل")
        self.assertEqual(clinic.phone, "01144229270")
        self.assertEqual(clinic.mobile_phone, "09119970828")
