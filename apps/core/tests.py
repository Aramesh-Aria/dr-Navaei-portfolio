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

    def test_digits_outside_latin_become_persian(self):
        # An address or a title typed with ASCII digits in the admin.
        self.assertEqual(
            render("{{ t|isolate_latin }}", t="آمل، پلاک 12، طبقه 3"),
            "آمل، پلاک ۱۲، طبقه ۳",
        )

    def test_digits_inside_a_latin_run_stay_in_it(self):
        self.assertEqual(
            render("{{ t|isolate_latin }}", t="عوارض COVID-19 و FEV1"),
            "عوارض <bdi>COVID-19</bdi> و <bdi>FEV1</bdi>",
        )

    def test_a_number_after_a_space_is_persian_text_not_part_of_the_run(self):
        self.assertEqual(render("{{ t|isolate_latin }}", t="بخش ICU 2"), "بخش <bdi>ICU</bdi> ۲")
        self.assertEqual(
            render("{{ t|fa_digits|isolate_latin }}", t="FEV1 80 درصد"),
            "<bdi>FEV۱</bdi> ۸۰ درصد",
        )

    def test_persian_digits_after_fa_digits_stay_in_the_run(self):
        self.assertEqual(
            render("{{ t|fa_digits|isolate_latin }}", t="COVID-19"),
            "<bdi>COVID-۱۹</bdi>",
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
    """The shared page shell (header, footer, call tab, meta), checked on the home page."""

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


from datetime import date

from apps.core.templatetags.site import solar_hijri_year


class SolarHijriYearTests(SimpleTestCase):
    """Years of experience are counted from `practising_since` (a Solar Hijri year)."""

    def test_autumn_2026_is_1405(self):
        self.assertEqual(solar_hijri_year(date(2026, 11, 14)), 1405)

    def test_the_year_turns_at_nowruz(self):
        self.assertEqual(solar_hijri_year(date(2026, 3, 20)), 1404)
        self.assertEqual(solar_hijri_year(date(2026, 3, 21)), 1405)

    def test_nowruz_on_march_20_in_a_leap_year(self):
        # 1 Farvardin 1403 fell on 20 March 2024.
        self.assertEqual(solar_hijri_year(date(2024, 3, 19)), 1402)
        self.assertEqual(solar_hijri_year(date(2024, 3, 20)), 1403)


class YearsSinceFilterTests(SimpleTestCase):
    def test_years_are_counted_from_the_solar_hijri_year(self):
        self.assertEqual(
            render("{{ y|years_since:today }}", y=1378, today=date(2026, 11, 14)), "27"
        )

    def test_no_year_gives_nothing(self):
        self.assertEqual(render("{{ y|years_since|default:'' }}", y=None), "")


from apps.conditions.models import ConditionTreated
from apps.doctor.models import Credential


class HomePageTests(TestCase):
    """`/`: the founder card, credentials preview, top conditions and the clinic."""

    def get(self):
        return self.client.get("/")

    def test_the_name_is_the_page_heading(self):
        html = self.get().content.decode()
        self.assertEqual(len(re.findall(r"<h1[ >]", html)), 1)
        self.assertRegex(html, r"<h1[^>]*>دکتر سپیده صفانوایی</h1>")

    def test_the_hero_call_button_hides_the_floating_tab(self):
        html = self.get().content.decode()
        self.assertRegex(html, r'<a class="pill pill--gold[^"]*" href="tel:\+981144229270" data-call-anchor')

    def test_the_shell_preview_is_gone(self):
        self.assertNotContains(self.get(), "پیش‌نمایش پوسته")

    def test_only_credentials_with_an_institution_flip(self):
        html = self.get().content.decode()
        self.assertEqual(html.count("data-flip"), 4)
        self.assertIn("دانشگاه علوم پزشکی مازندران", html)
        # A title-only credential is a static row.
        self.assertIn("عضو انجمن علمی ریه ایران", html)

    def test_a_credential_detail_goes_on_the_back_of_its_card(self):
        Credential.objects.filter(title="هیات علمی").update(detail="تدریس به دستیاران داخلی")
        self.assertContains(self.get(), "تدریس به دستیاران داخلی")

    def test_top_six_published_conditions_link_to_their_pages(self):
        ConditionTreated.objects.filter(slug="asthma").update(is_published=False)
        html = self.get().content.decode()
        self.assertNotIn('href="/conditions/asthma/"', html)
        self.assertIn('href="/conditions/copd/"', html)
        self.assertIn('href="/conditions/lung-allergies/"', html)  # 7th, now 6th
        self.assertNotIn('href="/conditions/pulmonary-fibrosis/"', html)

    def test_latin_in_condition_titles_is_isolated(self):
        self.assertContains(self.get(), "<bdi>COPD</bdi> (بیماری انسدادی مزمن ریه)")

    def test_procedures_block_disappears_when_none_are_published(self):
        self.assertContains(self.get(), "اقدامات درمانی")
        self.assertContains(self.get(), 'href="/conditions/bronchoscopy/"')
        ConditionTreated.objects.filter(category="procedure").update(is_published=False)
        self.assertNotContains(self.get(), 'id="procedures-title"')

    def test_experience_and_council_number_appear_only_once_entered(self):
        self.assertNotContains(self.get(), "سال تجربه")
        DoctorProfile.objects.update(practising_since=1378, medical_council_number="51510")
        response = self.get()
        self.assertContains(response, "سال تجربه")
        self.assertContains(response, "۵۱۵۱۰")

    def test_route_button_only_with_a_map_link(self):
        self.assertNotContains(self.get(), "مسیر مطب")
        ClinicLocation.objects.update(map_url="https://nshn.ir/abc")
        self.assertContains(self.get(), "مسیر مطب")

    def test_the_portrait_is_the_profile_photo_url(self):
        self.assertRegex(
            self.get().content.decode(),
            r'<img class="portrait__img" src="/public/static/doctor/doctor-placeholder\.[0-9a-f]{12}\.svg"',
        )

    def test_home_renders_without_locations_or_credentials(self):
        ClinicLocation.objects.all().delete()
        Credential.objects.all().delete()
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "data-flip")


class BioFiltersTests(SimpleTestCase):
    """The bio is set as paragraphs whose opening sentence leads, with the
    paragraph's first year in the margin (01-direction.md §6, /about/)."""

    def test_the_opening_sentence_is_split_from_the_rest(self):
        source = "{% with s=t|lead_sentence %}[{{ s.lead }}][{{ s.rest }}]{% endwith %}"
        self.assertEqual(
            render(source, t="جمله‌ی اول است. جمله‌ی دوم."),
            "[جمله‌ی اول است.][جمله‌ی دوم.]",
        )

    def test_a_single_sentence_is_all_lead(self):
        source = "{% with s=t|lead_sentence %}[{{ s.lead }}][{{ s.rest }}]{% endwith %}"
        self.assertEqual(render(source, t="فقط یک جمله"), "[فقط یک جمله][]")

    def test_the_first_year_is_found_in_persian_or_ascii_digits(self):
        self.assertEqual(render("{{ t|first_year }}", t="در سال ۱۳۸۵ وارد و در ۱۳۸۷ بازگشت"), "۱۳۸۵")
        self.assertEqual(render("{{ t|first_year }}", t="since 1378"), "۱۳۷۸")

    def test_counts_are_not_years(self):
        self.assertEqual(render("{{ t|first_year }}", t="به مدت ۸ سال و ۳۰ مقاله"), "")


class AboutPageTests(TestCase):
    def get(self):
        return self.client.get("/about/")

    def test_about_has_its_own_title_and_heading(self):
        html = self.get().content.decode()
        self.assertIn("<title>درباره‌ی دکتر سپیده صفانوایی", html)
        self.assertRegex(html, r"<h1[^>]*>دکتر سپیده صفانوایی</h1>")

    def test_every_bio_paragraph_is_shown(self):
        html = self.get().content.decode()
        self.assertEqual(html.count('class="bio__para"'), 6)
        self.assertIn("<bdi>ERS</bdi>", html)

    def test_every_credential_is_shown(self):
        html = self.get().content.decode()
        self.assertEqual(html.count("data-flip"), 4)
        self.assertIn("بیش از ۳۰ مقاله علمی", html)

    def test_nav_marks_the_about_link_current(self):
        self.assertContains(self.get(), 'href="/about/" aria-current="page"')

    def test_about_renders_without_a_bio_paragraph_break(self):
        DoctorProfile.objects.update(bio="یک جمله.")
        self.assertContains(self.get(), 'class="bio__para"', count=1)

    def test_about_description_is_the_bio_s_opening_sentence(self):
        self.assertContains(
            self.get(),
            '<meta name="description" content="دکتر سپیده صفانوایی فارغ‌التحصیل تخصص داخلی در سال ۱۳۷۸ است.">',
        )


class RouteLabelTests(TestCase):
    """«نشانی مطب و مسیر» promises a route only when a map link exists."""

    def test_without_a_map_link_the_label_names_only_the_address(self):
        ClinicLocation.objects.update(map_url="")
        html = self.client.get("/conditions/asthma/").content.decode()
        self.assertIn("نشانی مطب<svg", html)
        self.assertNotIn("و مسیر", html)

    def test_with_a_map_link_the_label_names_the_route(self):
        ClinicLocation.objects.update(map_url="https://neshan.org/maps/places/x")
        for path in ("/", "/conditions/asthma/", "/contact/"):
            with self.subTest(path=path):
                self.assertContains(self.client.get(path), "نشانی مطب و مسیر")


class CallTabTests(TestCase):
    def test_call_tab_starts_hidden_so_it_never_flashes_on_load(self):
        # site.js shows it once no [data-call-anchor] is on screen; CSS shows it without JS.
        self.assertContains(self.client.get("/"), '<a class="calltab is-hidden"')


from unittest import mock

from django.test import Client, RequestFactory

from apps.core.views import server_error


class NotFoundPageTests(TestCase):
    def test_an_unknown_address_gets_the_site_404_with_ways_back(self):
        response = self.client.get("/no-such-page/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        html = response.content.decode()
        self.assertRegex(html, r"<h1[^>]*>این صفحه پیدا نشد</h1>")
        self.assertIn('<meta name="robots" content="noindex">', html)
        # A missing page must not name itself as the canonical address.
        self.assertNotIn('rel="canonical"', html)
        self.assertNotIn('og:url', html)
        self.assertIn('href="/conditions/"', html)
        self.assertIn('href="/conditions/asthma/"', html)  # the published conditions, as threads
        self.assertIn('href="tel:+981144229270"', html)

    def test_an_unpublished_condition_gets_the_same_page(self):
        ConditionTreated.objects.filter(slug="asthma").update(is_published=False)
        response = self.client.get("/conditions/asthma/")
        self.assertContains(response, "این صفحه پیدا نشد", status_code=404)
        self.assertNotContains(response, 'href="/conditions/asthma/"', status_code=404)


class ServerErrorPageTests(TestCase):
    def test_the_site_500_handler_is_installed(self):
        from config import urls

        self.assertEqual(urls.handler500, "apps.core.views.server_error")

    def test_server_error_page_apologises_and_gives_the_clinic_phone(self):
        response = server_error(RequestFactory().get("/"))
        self.assertEqual(response.status_code, 500)
        self.assertContains(response, "مشکلی پیش آمد", status_code=500)
        self.assertContains(response, 'href="tel:+981144229270"', status_code=500)
        self.assertContains(response, 'lang="fa" dir="rtl"', status_code=500)

    def test_without_the_database_the_page_still_renders_without_the_phone(self):
        with mock.patch("apps.core.views.ClinicLocation.objects.all", side_effect=RuntimeError("db down")):
            response = server_error(RequestFactory().get("/"))
        self.assertContains(response, "مشکلی پیش آمد", status_code=500)
        self.assertNotContains(response, "tel:", status_code=500)

    def test_a_500_page_that_cannot_render_still_answers_500(self):
        with mock.patch("apps.core.views.loader.get_template", side_effect=RuntimeError), \
                self.assertLogs("apps.core.views", "ERROR"):
            response = server_error(RequestFactory().get("/"))
        self.assertEqual(response.status_code, 500)
        self.assertContains(response, "Server Error (500)", status_code=500)


class BadRequestPageTests(TestCase):
    def test_the_site_400_handler_is_installed(self):
        from config import urls

        self.assertEqual(urls.handler400, "apps.core.views.bad_request")

    def test_a_request_for_an_unknown_host_gets_the_persian_400_page(self):
        response = self.client.get("/", HTTP_HOST="evil.example")
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "400.html")
        self.assertContains(response, "درخواست نادرست بود", status_code=400)
        self.assertContains(response, '<meta name="robots" content="noindex">', status_code=400)
        self.assertNotContains(response, 'rel="canonical"', status_code=400)
        self.assertContains(response, 'href="tel:+981144229270"', status_code=400)


class PermissionDeniedPageTests(TestCase):
    def test_the_site_403_handler_is_installed(self):
        from config import urls

        self.assertEqual(urls.handler403, "apps.core.views.permission_denied")

    def test_a_forbidden_page_gets_the_persian_403_page(self):
        from django.contrib.auth import get_user_model

        self.client.force_login(get_user_model().objects.create_superuser("editor", "", "pw"))
        response = self.client.get("/admin/inquiries/inquiry/add/")  # Inquiries come only from patients
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")
        self.assertContains(response, "دسترسی به این صفحه ممکن نیست", status_code=403)
        self.assertNotContains(response, 'rel="canonical"', status_code=403)
        self.assertContains(response, 'href="/"', status_code=403)


class ExpiredFormPageTests(TestCase):
    def test_a_form_sent_without_its_csrf_cookie_gets_a_persian_page_back_to_the_form(self):
        response = Client(enforce_csrf_checks=True).post("/contact/", {"name": "x", "phone": "09120000000"})
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403_csrf.html")
        self.assertContains(response, "فرم منقضی شد", status_code=403)
        self.assertNotContains(response, 'rel="canonical"', status_code=403)
        self.assertContains(response, 'href="/contact/"', status_code=403)
