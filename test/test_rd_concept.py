import unittest
from unittest import TestCase

from ro.racai.robin.dialog.ctype import CType
from ro.racai.robin.dialog.rd_concept import RDConcept


class TestRDConcept(TestCase):

    def setUp(self) -> None:
        self.new_concept1 = RDConcept(CType.WORD, "abc")
        self.new_concept2 = RDConcept(CType.PERSON, "abc", "Def")
        self.new_concept3 = RDConcept(CType.WORD, "abc", " ")
        self.new_concept4 = RDConcept.builder(CType.WORD, "abc", ["a", "B", "c"], "def")

    def test_create_concept(self):
        self.assertIsNone(self.new_concept1._canonical_form)
        self.assertEqual(self.new_concept2._canonical_form, "def")
        self.assertIsNone(self.new_concept3._canonical_form)

    def test_builder(self):
        self.assertListEqual(self.new_concept4._synonyms_of_canonical_form, ['a', 'b', 'c'])

    def test_deep_copy(self):
        copy_concept = self.new_concept4.deep_copy()
        self.assertEqual(self.new_concept4, copy_concept)

    def test_equals(self):
        self.assertNotEqual(self.new_concept1, self.new_concept2)
        canonical_form_none_concept = RDConcept(CType.PERSON, None, "abc")
        new_concept5 = RDConcept(CType.PERSON, None, "ABC")
        self.assertEqual(new_concept5, canonical_form_none_concept)


if __name__ == "__main__":
    unittest.main()
