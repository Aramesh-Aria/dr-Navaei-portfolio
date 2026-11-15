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


class LocationsPageTests(TestCase):
    """`/locations/`: every Clinic Location, all fields, 1 to N."""

    def get(self):
        return self.client.get("/locations/")

    def add(self, name, **kwargs):
        fields = {"address": "ساری", "phone": "01133344455", "hours": "صبح‌ها", "order": 5}
        fields.update(kwargs)
        return ClinicLocation.objects.create(name=name, **fields)

    def test_the_amol_clinic_is_shown_with_every_field(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertRegex(html, r"<h1[^>]*>مطب</h1>")
        main = html[html.index("<main"):html.index("</main>")]
        self.assertIn("ساختمان پزشکان آنیتا", main)
        self.assertIn('href="tel:+981144229270"', main)
        self.assertIn('href="tel:+989119970828"', main)
        self.assertIn("پذیرش بیماران: روزانه، شیفت عصر", main)

    def test_one_location_is_a_single_wide_block(self):
        html = self.get().content.decode()
        self.assertIn('class="places places--1"', html)
        self.assertNotIn("places--many", html)

    def test_two_and_three_locations_become_columns_under_a_plural_heading(self):
        self.add("بیمارستان امام ساری")
        html = self.get().content.decode()
        self.assertIn("places--2 places--many", html)
        self.assertRegex(html, r"<h1[^>]*>مطب‌ها</h1>")
        self.add("درمانگاه سوم", order=6)
        html = self.get().content.decode()
        self.assertIn("places--3 places--many", html)
        self.assertEqual(html.count('class="place"'), 3)

    def test_route_button_only_with_a_map_link(self):
        self.assertNotContains(self.get(), "مسیر روی نقشه")
        ClinicLocation.objects.update(map_url="https://nshn.ir/abc")
        main = self.get().content.decode().split("<main")[1].split("</main>")[0]
        self.assertIn('href="https://nshn.ir/abc"', main)

    def test_a_location_without_a_mobile_shows_only_its_landline(self):
        self.add("بیمارستان امام ساری", mobile_phone="")
        main = self.get().content.decode().split("<main")[1].split("</main>")[0]
        self.assertEqual(main.count("<dt>همراه</dt>"), 1)  # the Amol clinic's, not Sari's

    def test_the_first_clinic_phone_hides_the_floating_tab(self):
        self.assertRegex(self.get().content.decode(), r'href="tel:\+981144229270" data-call-anchor')

    def test_nav_marks_the_locations_link_current(self):
        self.assertContains(self.get(), 'href="/locations/" aria-current="page"')

    def test_page_renders_with_no_locations(self):
        ClinicLocation.objects.all().delete()
        self.assertEqual(self.get().status_code, 200)
