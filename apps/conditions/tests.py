from django.db import IntegrityError
from django.test import TestCase

from .models import ConditionTreated


def make(slug, **kwargs):
    defaults = {"title": slug, "short_description": "...", "body": "..."}
    defaults.update(kwargs)
    return ConditionTreated.objects.create(slug=slug, **defaults)


class ConditionTreatedTests(TestCase):
    def setUp(self):
        ConditionTreated.objects.all().delete()  # drop seeded rows

    def test_new_item_defaults_to_condition_not_procedure(self):
        self.assertEqual(make("asthma").category, ConditionTreated.CATEGORY_CONDITION)

    def test_items_follow_manual_order(self):
        make("c", order=3)
        make("a", order=1)
        make("b", order=2)
        self.assertEqual(
            [c.slug for c in ConditionTreated.objects.all()], ["a", "b", "c"]
        )

    def test_conditions_and_procedures_can_be_listed_separately(self):
        make("asthma")
        make("bronchoscopy", category=ConditionTreated.CATEGORY_PROCEDURE)
        conditions = ConditionTreated.objects.filter(
            category=ConditionTreated.CATEGORY_CONDITION
        )
        self.assertEqual([c.slug for c in conditions], ["asthma"])

    def test_published_leaves_out_hidden_rows(self):
        make("asthma")
        make("hidden", is_published=False)
        self.assertEqual([c.slug for c in ConditionTreated.objects.published()], ["asthma"])

    def test_conditions_and_procedures_are_published_rows_of_each_category(self):
        make("asthma", order=1)
        make("copd", order=2, is_published=False)
        make("bronchoscopy", category=ConditionTreated.CATEGORY_PROCEDURE)
        make("stent", category=ConditionTreated.CATEGORY_PROCEDURE, is_published=False)
        self.assertEqual([c.slug for c in ConditionTreated.objects.conditions()], ["asthma"])
        self.assertEqual([c.slug for c in ConditionTreated.objects.procedures()], ["bronchoscopy"])

    def test_slug_must_be_unique(self):
        make("asthma")
        with self.assertRaises(IntegrityError):
            make("asthma")


class SeededConditionsTests(TestCase):
    def test_fifteen_conditions_and_five_procedures_are_seeded(self):
        self.assertEqual(
            ConditionTreated.objects.filter(category="condition").count(), 15
        )
        self.assertEqual(
            ConditionTreated.objects.filter(category="procedure").count(), 5
        )

    def test_seeded_items_are_published(self):
        self.assertFalse(ConditionTreated.objects.filter(is_published=False).exists())

    def test_every_seeded_body_has_at_least_two_sections(self):
        for item in ConditionTreated.objects.all():
            with self.subTest(item.slug):
                self.assertGreaterEqual(item.body.count("\n## "), 2)

    def test_bronchoscopy_is_seeded_as_a_procedure(self):
        self.assertEqual(
            ConditionTreated.objects.get(slug="bronchoscopy").category, "procedure"
        )


class ConditionsListPageTests(TestCase):
    """`/conditions/`: two labelled groups, published rows only."""

    def get(self):
        return self.client.get("/conditions/")

    def test_both_groups_are_listed_with_links_to_each_page(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn('id="conditions-title"', html)
        self.assertIn('id="procedures-title"', html)
        self.assertEqual(html.count('href="/conditions/asthma/"'), 1)
        self.assertIn('href="/conditions/bronchoscopy/"', html)
        self.assertIn("تشخیص و درمان آسم در کودکان و بزرگسالان", html)

    def test_unpublished_rows_are_not_listed(self):
        ConditionTreated.objects.filter(slug="asthma").update(is_published=False)
        self.assertNotContains(self.get(), 'href="/conditions/asthma/"')

    def test_jump_links_show_each_group_s_count(self):
        html = self.get().content.decode()
        self.assertIn('href="#conditions"', html)
        self.assertIn('href="#procedures"', html)
        self.assertIn("۱۵", html)

    def test_a_group_with_no_rows_disappears_with_its_jump_link(self):
        ConditionTreated.objects.filter(category="procedure").update(is_published=False)
        html = self.get().content.decode()
        self.assertNotIn('id="procedures-title"', html)
        self.assertNotIn('href="#procedures"', html)
        self.assertIn('id="conditions-title"', html)

    def test_nav_marks_the_conditions_link_current(self):
        self.assertContains(self.get(), 'href="/conditions/" aria-current="page"')

    def test_the_page_has_its_own_title(self):
        self.assertContains(self.get(), "<title>بیماری‌ها و اقدامات درمانی · دکتر سپیده صفانوایی</title>")


import json
import re


class ConditionDetailPageTests(TestCase):
    """`/conditions/<slug>/`: Mayo Clinic's order, built for today's short bodies."""

    def get(self, slug="copd"):
        return self.client.get(f"/conditions/{slug}/")

    def test_the_title_is_the_page_heading_with_latin_isolated(self):
        html = self.get().content.decode()
        self.assertEqual(len(re.findall(r"<h1[ >]", html)), 1)
        self.assertRegex(html, r"<h1[^>]*><bdi>COPD</bdi> \(بیماری انسدادی مزمن ریه\)</h1>")
        self.assertIn("تشخیص و درمان بیماری انسدادی مزمن ریه", html)
        self.assertIn("محدودیت در عبور هوا", html)

    def test_an_unpublished_slug_is_a_404(self):
        ConditionTreated.objects.filter(slug="copd").update(is_published=False)
        self.assertEqual(self.get().status_code, 404)

    def test_an_unknown_slug_is_a_404(self):
        self.assertEqual(self.get("no-such-thing").status_code, 404)

    def structured_data(self, slug="copd"):
        html = self.get(slug).content.decode()
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        return {d["@type"]: d for d in map(json.loads, blocks)}

    def test_a_condition_page_carries_medical_condition_data(self):
        data = self.structured_data()["MedicalCondition"]
        self.assertEqual(data["name"], "COPD (بیماری انسدادی مزمن ریه)")
        self.assertEqual(data["description"], "تشخیص و درمان بیماری انسدادی مزمن ریه")
        self.assertEqual(data["url"], "https://dr.safanavaiee.ir/conditions/copd/")

    def test_a_procedure_page_carries_medical_procedure_data(self):
        data = self.structured_data("bronchoscopy")
        self.assertNotIn("MedicalCondition", data)
        self.assertEqual(data["MedicalProcedure"]["name"], "برونکوسکوپی")

    def test_when_to_see_a_doctor_leads_to_the_clinic_phone(self):
        html = self.get().content.decode()
        block = html[html.index('id="see-a-doctor"'):]
        self.assertIn("چه زمانی به پزشک مراجعه کنید", block)
        self.assertIn('href="tel:+981144229270"', block)
        self.assertIn('href="/locations/"', block)

    def test_a_procedure_page_asks_for_a_visit_instead(self):
        html = self.get("bronchoscopy").content.decode()
        self.assertNotIn("چه زمانی به پزشک مراجعه کنید", html)
        self.assertIn("نوبت و مشاوره", html)

    def test_a_short_body_has_no_on_this_page_index(self):
        ConditionTreated.objects.filter(slug="copd").update(body="یک بند کوتاه.")
        self.assertNotContains(self.get(), "در این صفحه")

    def test_seeded_bodies_get_an_on_this_page_index(self):
        self.assertContains(self.get(), "در این صفحه")

    def test_two_headed_sections_get_an_on_this_page_index(self):
        ConditionTreated.objects.filter(slug="copd").update(
            body="مقدمه.\n\n## علائم\nسرفه.\n\n## درمان\nدارو."
        )
        html = self.get().content.decode()
        self.assertIn("در این صفحه", html)
        self.assertIn('href="#section-1"', html)
        self.assertIn('<h2 class="display-3" id="section-2-title">درمان</h2>', html)
        self.assertIn('href="#see-a-doctor"', html)

    def test_meta_tags_are_the_item_s_own(self):
        html = self.get().content.decode()
        self.assertIn("<title>COPD (بیماری انسدادی مزمن ریه) · دکتر سپیده صفانوایی</title>", html)
        self.assertIn('<meta name="description" content="تشخیص و درمان بیماری انسدادی مزمن ریه">', html)
        self.assertIn('<link rel="canonical" href="https://dr.safanavaiee.ir/conditions/copd/">', html)


import importlib

from django.apps import apps as django_apps

sectioned = importlib.import_module("apps.conditions.migrations.0004_sectioned_bodies")


class SectionedBodiesMigrationTests(TestCase):
    """0004 runs on production: it may only replace the untouched seed text."""

    def test_an_edited_body_is_left_alone(self):
        ConditionTreated.objects.filter(slug="asthma").update(body=sectioned.SEED["asthma"])
        ConditionTreated.objects.filter(slug="copd").update(body="متن ویرایش‌شده‌ی دکتر.")
        sectioned.forwards(django_apps, None)
        self.assertEqual(ConditionTreated.objects.get(slug="copd").body, "متن ویرایش‌شده‌ی دکتر.")
        self.assertEqual(ConditionTreated.objects.get(slug="asthma").body, sectioned.BODIES["asthma"])

    def test_backwards_restores_only_untouched_new_text(self):
        ConditionTreated.objects.filter(slug="copd").update(body="متن ویرایش‌شده‌ی دکتر.")
        sectioned.backwards(django_apps, None)
        self.assertEqual(ConditionTreated.objects.get(slug="asthma").body, sectioned.SEED["asthma"])
        self.assertEqual(ConditionTreated.objects.get(slug="copd").body, "متن ویرایش‌شده‌ی دکتر.")

    def test_every_seeded_slug_has_new_text(self):
        self.assertEqual(set(sectioned.BODIES), set(sectioned.SEED))
        self.assertEqual(len(sectioned.BODIES), 20)
