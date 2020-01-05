from enum import Enum

"""
<p>Concept type: if not a word such as <i>sală</i>, it can
be a TIME unit or a PERSON (for now; more to be added as needed).</p>


Any noun here.
This is the general category, the default category.
WORD

e.g. Angela Gheorghiu
PERSON,

e.g. 8:15
TIME

e.g. sala 209
LOCATION

"""

CType = Enum("CType", (
                "WORD",
                "PERSON",
                "TIME",
                "LOCATION"))


def get_member_regex():
    options = []
    for name, member in CType.__members__.items():
        options.append(name)

    return "(" + "|".join(options) + ")"



