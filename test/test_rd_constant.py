import unittest

from ro.racai.robin.dialog.ctype import CType
from ro.racai.robin.dialog.rd_constant import RDConstant


class TestRDConstant(unittest.TestCase):

    def setUp(self) -> None:
        self.rd_constant1 = RDConstant(CType.WORD, "ref")

    def test_create_rd_constant(self):
        self.assertRaises(RuntimeError, RDConstant, CType.PERSON, " ")

    def test_deep_copy(self):
        copyed_rd_constant = self.rd_constant1.deep_copy()
        self.assertEqual(self.rd_constant1, copyed_rd_constant)
        self.assertIsNot(self.rd_constant1, copyed_rd_constant)
        arr = [self.rd_constant1]
        self.assertIn(copyed_rd_constant, arr)

    def test_equals(self):
        other1_rd_constants = RDConstant(CType.PERSON, "ref")
        self.assertNotEqual(other1_rd_constants, self.rd_constant1)
        other2_rd_constants = RDConstant(CType.WORD, "REF")
        self.assertEqual(self.rd_constant1, other2_rd_constants)


if __name__ == "__main__":
    unittest.main()
