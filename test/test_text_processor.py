import unittest

from ro.racai.robin.dialog.ro_sayings import RoSayings
from ro.racai.robin.nlp.ro_lexicon import RoLexicon
from ro.racai.robin.nlp.ro_text_processor import RoTextProcessor
from ro.racai.robin.nlp.ro_word_net import RoWordNet


class RoTextProcessorTest(unittest.TestCase):

    def test_TEPROLIN(self):
        tp = RoTextProcessor(RoLexicon(), RoWordNet(), RoSayings())
        tokens = tp.text_processor("Unde se află laboratorul de SDA?")
        self.assertTrue(len(tokens) == 7)
        self.assertTrue(tokens[0].wform == "Unde")
        self.assertTrue(tokens[0].drel == "advmod")
        self.assertTrue(tokens[0].head == 3)


if __name__ == "__main__":
    unittest.main()
