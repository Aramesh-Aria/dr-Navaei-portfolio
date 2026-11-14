from django.template import Context, Template
from django.test import SimpleTestCase


def render(source, **context):
    return Template("{% load site %}" + source).render(Context(context))


class PersianDigitsFilterTests(SimpleTestCase):
    def test_ascii_digits_become_persian(self):
        self.assertEqual(render("{{ y|fa_digits }}", y=1378), "۱۳۷۸")

    def test_text_around_digits_is_kept(self):
        self.assertEqual(render("{{ s|fa_digits }}", s="بیش از 30 مقاله"), "بیش از ۳۰ مقاله")

    def test_empty_value_renders_nothing(self):
        self.assertEqual(render("{{ y|fa_digits }}", y=None), "")


class PhoneFilterTests(SimpleTestCase):
    def test_tel_href_is_international_ascii(self):
        self.assertEqual(render("{{ p|tel_href }}", p="01144229270"), "tel:+981144229270")

    def test_tel_href_accepts_persian_digits_spaces_and_dashes(self):
        self.assertEqual(render("{{ p|tel_href }}", p="۰۹۱۱ ۹۹۷-۰۸۲۸"), "tel:+989119970828")

    def test_landline_is_shown_with_its_area_code_split_off(self):
        self.assertEqual(render("{{ p|phone_display }}", p="01144229270"), "۰۱۱-۴۴۲۲۹۲۷۰")

    def test_mobile_is_shown_in_three_groups(self):
        self.assertEqual(render("{{ p|phone_display }}", p="09119970828"), "۰۹۱۱ ۹۹۷ ۰۸۲۸")

    def test_unrecognised_number_is_shown_as_typed_in_persian_digits(self):
        self.assertEqual(render("{{ p|phone_display }}", p="123"), "۱۲۳")


class IsolateLatinFilterTests(SimpleTestCase):
    def test_latin_runs_are_wrapped_in_bdi(self):
        self.assertEqual(
            render("{{ t|isolate_latin }}", t="COPD (بیماری انسدادی مزمن ریه)"),
            "<bdi>COPD</bdi> (بیماری انسدادی مزمن ریه)",
        )

    def test_multi_word_latin_stays_one_run(self):
        self.assertEqual(
            render("{{ t|isolate_latin }}", t="عضو ERS و Lung Cancer"),
            "عضو <bdi>ERS</bdi> و <bdi>Lung Cancer</bdi>",
        )

    def test_html_is_escaped_before_wrapping(self):
        self.assertEqual(
            render("{{ t|isolate_latin }}", t="<b>x</b>"),
            "&lt;<bdi>b</bdi>&gt;<bdi>x</bdi>&lt;/<bdi>b</bdi>&gt;",
        )


class ParagraphsFilterTests(SimpleTestCase):
    def test_text_is_split_on_blank_lines(self):
        source = "{% for p in t|paragraphs %}[{{ p }}]{% endfor %}"
        self.assertEqual(render(source, t="یک\n\nدو\r\n\r\nسه\n"), "[یک][دو][سه]")


class BodySectionsFilterTests(SimpleTestCase):
    """Stage 2 gate 7.1f: an editor starts a section with a line `## heading`."""

    source = (
        "{% for s in t|body_sections %}"
        "<{{ s.id }}|{{ s.heading }}|{% for p in s.paragraphs %}({{ p }}){% endfor %}>"
        "{% endfor %}"
    )

    def test_short_body_without_headings_is_one_untitled_section(self):
        self.assertEqual(render(self.source, t="یک جمله."), "<|None|(یک جمله.)>")

    def test_headed_sections_are_split_with_their_paragraphs(self):
        body = "مقدمه.\n\n## علائم\nسرفه.\n\nتنگی نفس.\n## درمان\nدارو."
        self.assertEqual(
            render(self.source, t=body),
            "<|None|(مقدمه.)>"
            "<section-1|علائم|(سرفه.)(تنگی نفس.)>"
            "<section-2|درمان|(دارو.)>",
        )


import json
import re

from django.conf import settings
from django.test import TestCase

from apps.doctor.models import DoctorProfile
from apps.locations.models import ClinicLocation


class ShellTests(TestCase):
    """The shared page shell, rendered by the temporary home view (Stage 3)."""

    def get(self):
        return self.client.get("/")

    def test_home_is_a_persian_rtl_page(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="fa" dir="rtl">')

    def test_html_is_revalidated_on_every_load(self):
        # Owner decision: a CSS/JS change must never need a hard refresh.
        self.assertIn("no-cache", self.get()["Cache-Control"])

    def test_stylesheet_and_script_links_carry_a_content_hash(self):
        html = self.get().content.decode()
        self.assertRegex(html, r'href="/public/static/assets/css/site\.[0-9a-f]{12}\.css"')
        self.assertRegex(html, r'src="/public/static/assets/js/site\.[0-9a-f]{12}\.js"')

    def test_header_shows_the_name_and_the_first_clinic_phone(self):
        response = self.get()
        self.assertContains(response, "دکتر سپیده صفانوایی")
        self.assertContains(response, 'href="tel:+981144229270"')
        self.assertContains(response, "۰۱۱-۴۴۲۲۹۲۷۰")

    def test_footer_lists_every_clinic_location(self):
        ClinicLocation.objects.create(
            name="بیمارستان امام ساری", address="ساری", phone="01133344455",
            hours="صبح‌ها", order=5,
        )
        response = self.get()
        self.assertContains(response, "مطب آمل")
        self.assertContains(response, "بیمارستان امام ساری")
        self.assertContains(response, 'href="tel:+981133344455"')

    def test_location_without_map_link_shows_no_route_button(self):
        ClinicLocation.objects.update(map_url="")
        self.assertNotContains(self.get(), "مسیر روی نقشه")

    def test_location_with_map_link_shows_the_route_button(self):
        ClinicLocation.objects.update(map_url="https://nshn.ir/abc")
        self.assertContains(self.get(), 'href="https://nshn.ir/abc"')

    def test_page_has_meta_description_canonical_and_open_graph(self):
        html = self.get().content.decode()
        self.assertIn('<link rel="canonical" href="https://dr.safanavaiee.ir/">', html)
        self.assertRegex(html, r'<meta name="description" content="[^"]+">')
        self.assertIn('<meta property="og:title"', html)
        self.assertIn('<meta property="og:locale" content="fa_IR">', html)

    def structured_data(self):
        html = self.get().content.decode()
        block = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        return json.loads(block.group(1))

    def test_structured_data_describes_the_physician_and_her_clinics(self):
        data = self.structured_data()
        self.assertEqual(data["@type"], "Physician")
        self.assertEqual(data["name"], "دکتر سپیده صفانوایی")
        clinic = data["location"][0]
        self.assertEqual(clinic["@type"], "MedicalClinic")
        self.assertEqual(clinic["telephone"], "+981144229270")
        self.assertIn("سبزه میدان", clinic["address"]["streetAddress"])
        self.assertEqual(clinic["address"]["addressCountry"], "IR")
        self.assertEqual(clinic["openingHours"], "پذیرش بیماران: روزانه، شیفت عصر")

    def test_council_number_appears_only_once_entered(self):
        self.assertNotIn("identifier", self.structured_data())
        DoctorProfile.objects.update(medical_council_number="51510")
        self.assertEqual(self.structured_data()["identifier"]["value"], "51510")

    def test_shell_still_renders_with_no_locations(self):
        ClinicLocation.objects.all().delete()
        self.assertEqual(self.get().status_code, 200)


class DevStaticTests(SimpleTestCase):
    def test_dev_server_serves_static_without_caching(self):
        self.assertEqual(settings.WHITENOISE_MAX_AGE, 0)
        self.assertLess(
            settings.INSTALLED_APPS.index("whitenoise.runserver_nostatic"),
            settings.INSTALLED_APPS.index("django.contrib.staticfiles"),
        )


from django.contrib.auth import get_user_model


class AdminThemeTests(TestCase):
    """Owner decision (Stage 2 gate): the admin uses the academy's Jazzmin setup."""

    def setUp(self):
        user = get_user_model().objects.create_superuser("editor", "", "pw")
        self.client.force_login(user)

    def test_admin_uses_the_persian_jazzmin_branding_and_rtl_fixes(self):
        html = self.client.get("/admin/").content.decode()
        self.assertIn("سایت دکتر صفانوایی", html)
        self.assertRegex(html, r"/public/static/assets/css/admin\.[0-9a-f]{12}\.css")

    def test_admin_logo_is_the_site_s_not_adminlte_a(self):
        html = self.client.get("/admin/").content.decode()
        self.assertRegex(html, r"/public/static/assets/img/admin-logo\.[0-9a-f]{12}\.svg")
        self.assertNotIn("AdminLTELogo", html)

    def test_admin_loads_nothing_from_the_internet(self):
        html = self.client.get("/admin/").content.decode()
        self.assertNotIn("fonts.googleapis.com", html)
        self.assertRegex(html, r"/public/static/vendor/bootswatch/flatly/bootstrap\.min[.0-9a-f]*\.css")
