from enum import Enum

"""
<p>An enumeration describing possible query types.</p>

CONDU-mă te rog la camera 1222.
COMMAND:

UNDE e sala 209?
LOCATION:

CINE ține cursul din sala 1254?
PERSON:

CÂND se ține cursul de fotografie?
TIME:

CUM ajung în laboratorul de robotică?
HOW:

În ce SALĂ se ține cursul de informatică?
WHAT:

Nu e așa că d-na Laura Florescu ține cursul de SDA în sala 113?
YESNO:

End of conversation
GOODBYE:

Start of conversation
HELLO:
"""

QType = Enum("QType", ("COMMAND",
                       "LOCATION",
                       "PERSON",
                       "TIME",
                       "HOW",
                       "WHAT",
                       "YESNO",
                       "GOODBYE",
                       "HELLO"))
