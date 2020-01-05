import os
import re
import unittest

from ro.racai.robin.dialog.ctype import get_member_regex, CType


class TestCTypeTestCase(unittest.TestCase):

    def test_get_member_regex(self):
        members_regex = get_member_regex()
        self.assertEqual(members_regex, '(WORD|PERSON|TIME|LOCATION)')

    def test_random(self):
        file = open("/home/free/PycharmProjects/robindialog/precis.mw")
        line = file.readline()
        while line != '':
            print(line)
            line = file.readline()



if __name__ == "__main__":
    unittest.main()
