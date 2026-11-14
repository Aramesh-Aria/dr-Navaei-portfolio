from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Credential, DoctorProfile


class AdminTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_superuser("editor", "", "pw")
        self.client.force_login(user)


class DoctorProfileSingletonAdminTests(AdminTestCase):
    """The Content Editor can only ever edit the one Doctor Profile."""

    def setUp(self):
        super().setUp()
        # The seed migration already created the profile; start each test
        # from an explicit, known state instead of relying on it.
        DoctorProfile.objects.all().delete()

    def test_profile_can_be_added_when_none_exists(self):
        response = self.client.get(reverse("admin:doctor_doctorprofile_add"))
        self.assertEqual(response.status_code, 200)

    def test_second_profile_cannot_be_added(self):
        DoctorProfile.objects.create(full_name="دکتر الف", bio="...")
        response = self.client.get(reverse("admin:doctor_doctorprofile_add"))
        self.assertEqual(response.status_code, 403)

    def test_changelist_redirects_to_the_single_profile(self):
        profile = DoctorProfile.objects.create(full_name="دکتر الف", bio="...")
        response = self.client.get(reverse("admin:doctor_doctorprofile_changelist"))
        self.assertRedirects(
            response, reverse("admin:doctor_doctorprofile_change", args=[profile.pk])
        )

    def test_credentials_are_editable_inline_on_the_profile(self):
        profile = DoctorProfile.objects.create(full_name="دکتر الف", bio="...")
        Credential.objects.create(profile=profile, title="فوق تخصص ریه")
        response = self.client.get(
            reverse("admin:doctor_doctorprofile_change", args=[profile.pk])
        )
        self.assertContains(response, "فوق تخصص ریه")


class CredentialOrderingTests(TestCase):
    def test_credentials_follow_manual_order(self):
        profile = DoctorProfile.objects.create(full_name="دکتر الف", bio="...")
        Credential.objects.create(profile=profile, title="سوم", order=30)
        Credential.objects.create(profile=profile, title="اول", order=10)
        Credential.objects.create(profile=profile, title="دوم", order=20)

        titles = [c.title for c in profile.credentials.all()]
        self.assertEqual(titles, ["اول", "دوم", "سوم"])


class SeededProfileTests(TestCase):
    """Real content from the doctor's asset text, loaded by migration."""

    def test_profile_is_seeded_with_name_and_tagline(self):
        profile = DoctorProfile.objects.get()
        self.assertEqual(profile.full_name, "دکتر سپیده صفانوایی")
        self.assertEqual(profile.intro_tagline, "متخصص داخلی و فوق تخصص بیماری‌های ریه")

    def test_internal_medicine_credential_is_from_shahid_beheshti_1378(self):
        credential = Credential.objects.get(title="متخصص داخلی")
        self.assertIn("شهید بهشتی", credential.institution)
        self.assertEqual(credential.year, 1378)

    def test_all_eight_credentials_are_seeded(self):
        self.assertEqual(DoctorProfile.objects.get().credentials.count(), 8)


class ProfilePhotoTests(TestCase):
    """Until the real photo is uploaded, the site shows a neutral placeholder."""

    def test_placeholder_is_used_when_no_photo_uploaded(self):
        profile = DoctorProfile(full_name="دکتر الف", bio="...")
        # With DEBUG off the manifest storage adds a cache-busting hash.
        self.assertRegex(
            profile.photo_url,
            r"^/public/static/doctor/doctor-placeholder(\.[0-9a-f]{12})?\.svg$",
        )

    def test_uploaded_photo_replaces_placeholder(self):
        profile = DoctorProfile(full_name="دکتر الف", bio="...", photo="doctor/real.jpg")
        self.assertEqual(profile.photo_url, "/public/media/doctor/real.jpg")
