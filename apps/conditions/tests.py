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

    def test_bronchoscopy_is_seeded_as_a_procedure(self):
        self.assertEqual(
            ConditionTreated.objects.get(slug="bronchoscopy").category, "procedure"
        )
