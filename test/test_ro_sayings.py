import unittest

from ro.racai.robin.dialog.ro_sayings import RoSayings


class TestROSayings(unittest.TestCase):
    def setUp(self) -> None:
        self.rosayings = RoSayings()

    def test_user_opening_statement(self):
        words = ['abc', 'b', 'c', 'd']
        self.assertFalse(self.rosayings.user_opening_statement(words))
        self.assertFalse(self.rosayings.user_closing_statement(words))


if __name__ == "__main__":
    unittest.main()
