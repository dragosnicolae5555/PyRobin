import unittest

from ro.racai.robin.nlp.string_utils import StringUtils


class TestStringUtils(unittest.TestCase):
    def test_none_empty_blank(self):
        self.assertTrue(StringUtils.is_none_empty_or_blank(None))
        self.assertTrue(StringUtils.is_none_empty_or_blank(""))
        self.assertTrue(StringUtils.is_none_empty_or_blank(" "))
        self.assertFalse(StringUtils.is_none_empty_or_blank("abc "))


if __name__ == "__main__":
    unittest.main()
