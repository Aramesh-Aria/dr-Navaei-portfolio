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


class ApprovedProfileFieldsTests(AdminTestCase):
    """Stage 2 gate: council number, practising-since year, Paziresh24 link and
    a longer credential detail. All optional, so they can start empty."""

    def test_new_profile_fields_are_saved_from_admin_and_may_be_blank(self):
        profile = DoctorProfile.objects.get()
        url = reverse("admin:doctor_doctorprofile_change", args=[profile.pk])
        data = {
            "full_name": profile.full_name,
            "intro_tagline": profile.intro_tagline,
            "bio": profile.bio,
            "medical_council_number": "51510",
            "practising_since": "1378",
            "paziresh24_url": "",
            "credentials-TOTAL_FORMS": "0",
            "credentials-INITIAL_FORMS": "0",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        profile.refresh_from_db()
        self.assertEqual(profile.medical_council_number, "51510")
        self.assertEqual(profile.practising_since, 1378)
        self.assertEqual(profile.paziresh24_url, "")

    def test_new_fields_start_empty_until_the_doctor_confirms_them(self):
        profile = DoctorProfile.objects.get()
        self.assertEqual(profile.medical_council_number, "")
        self.assertIsNone(profile.practising_since)
        self.assertEqual(profile.paziresh24_url, "")

    def test_credential_detail_is_editable_inline(self):
        profile = DoctorProfile.objects.get()
        response = self.client.get(
            reverse("admin:doctor_doctorprofile_change", args=[profile.pk])
        )
        self.assertContains(response, "credentials-0-detail")


import io
import shutil
import tempfile
from pathlib import Path
from unittest import mock

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image


def jpeg_upload(width, height, name="portrait.jpg"):
    buffer = io.BytesIO()
    Image.new("RGB", (width, height), (200, 160, 120)).save(buffer, "JPEG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")


class ProcessedPhotoTests(TestCase):
    """Stage 2 gate 7.3a: an unedited phone photo must not be the page's LCP
    image, so the upload is resized to WebP and the original is kept."""

    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media)
        override = override_settings(MEDIA_ROOT=self.media)
        override.enable()
        self.addCleanup(override.disable)

    def open_url(self, url):
        return Image.open(self.media + url.removeprefix("/public/media"))

    def test_large_upload_is_served_as_1200px_webp(self):
        profile = DoctorProfile.objects.create(
            full_name="دکتر الف", bio="...", photo=jpeg_upload(3000, 4000)
        )
        self.assertRegex(profile.photo_url, r"^/public/media/doctor/portrait.*-1200\.webp$")
        image = self.open_url(profile.photo_url)
        self.assertEqual((image.format, image.width), ("WEBP", 1200))

    def test_srcset_offers_600_and_1200_widths(self):
        profile = DoctorProfile.objects.create(
            full_name="دکتر الف", bio="...", photo=jpeg_upload(3000, 4000)
        )
        self.assertRegex(profile.photo_srcset, r"-600\.webp 600w, .*-1200\.webp 1200w$")
        self.assertEqual(self.open_url(profile.photo_srcset.split(" ")[0]).width, 600)

    def test_original_upload_is_kept(self):
        profile = DoctorProfile.objects.create(
            full_name="دکتر الف", bio="...", photo=jpeg_upload(3000, 4000)
        )
        self.assertEqual(Image.open(profile.photo.path).width, 3000)

    def test_small_upload_is_never_enlarged(self):
        profile = DoctorProfile.objects.create(
            full_name="دکتر الف", bio="...", photo=jpeg_upload(500, 700)
        )
        self.assertEqual(self.open_url(profile.photo_url).width, 500)

    def test_placeholder_has_no_srcset(self):
        self.assertEqual(DoctorProfile(full_name="دکتر الف", bio="...").photo_srcset, "")

    def copies(self):
        return sorted(p.name for p in Path(self.media, "doctor").glob("*.webp"))

    def test_replacing_the_photo_deletes_the_old_copies(self):
        profile = DoctorProfile.objects.create(
            full_name="دکتر الف", bio="...", photo=jpeg_upload(1600, 2000, "old.jpg")
        )
        profile.photo = jpeg_upload(1600, 2000, "new.jpg")
        profile.save()
        self.assertEqual(self.copies(), ["new-1200.webp", "new-600.webp"])
        self.assertTrue(Path(self.media, "doctor", "old.jpg").exists())  # original kept

    def test_clearing_the_photo_deletes_its_copies(self):
        profile = DoctorProfile.objects.create(
            full_name="دکتر الف", bio="...", photo=jpeg_upload(1600, 2000)
        )
        profile.photo = None
        profile.save()
        self.assertEqual(self.copies(), [])

    def test_saving_other_fields_leaves_the_copies_alone(self):
        profile = DoctorProfile.objects.create(
            full_name="دکتر الف", bio="...", photo=jpeg_upload(1600, 2000)
        )
        with mock.patch("apps.doctor.images.make_variants") as make:
            profile.bio = "تازه"
            profile.save()
        make.assert_not_called()

    def test_copies_are_looked_up_once_not_on_every_render(self):
        profile = DoctorProfile.objects.create(
            full_name="دکتر الف", bio="...", photo=jpeg_upload(1600, 2000)
        )
        profile = DoctorProfile.objects.get(pk=profile.pk)
        with mock.patch.object(FileSystemStorage, "exists", side_effect=AssertionError("stat")):
            for _ in range(3):
                self.assertTrue(profile.photo_url.endswith("-1200.webp"))
                self.assertIn("600w", profile.photo_srcset)


class CorruptPhotoUploadTests(AdminTestCase):
    """A photo Pillow cannot decode is refused with a form error, not a 500."""

    def setUp(self):
        super().setUp()
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media)
        override = override_settings(MEDIA_ROOT=self.media)
        override.enable()
        self.addCleanup(override.disable)

    def test_a_truncated_jpeg_gets_a_persian_error(self):
        whole = jpeg_upload(1600, 2000).read()
        broken = SimpleUploadedFile("broken.jpg", whole[: len(whole) // 3], "image/jpeg")
        profile = DoctorProfile.objects.get()
        response = self.client.post(
            reverse("admin:doctor_doctorprofile_change", args=[profile.pk]),
            {
                "full_name": profile.full_name,
                "intro_tagline": profile.intro_tagline,
                "bio": profile.bio,
                "photo": broken,
                "credentials-TOTAL_FORMS": "0",
                "credentials-INITIAL_FORMS": "0",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "این عکس باز نمی‌شود")
        profile.refresh_from_db()
        self.assertFalse(profile.photo)
