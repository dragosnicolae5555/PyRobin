from ro.racai.robin.dialog.rd_sayings import RDSayings
import re


def init_closing_lines(opening_set):
    # Everything is lower-cased here!
    opening_set.add("mulțumesc")
    opening_set.add("mulțam")
    opening_set.add("mersi")
    opening_set.add("pa")
    opening_set.add("la revedere")


def init_opening_lines(closing_set):
    # Everything is lower-cased here!
    closing_set.add("salut")
    closing_set.add("noroc")
    closing_set.add("bună")
    closing_set.add("servus")
    closing_set.add("pepper")
    closing_set.add("pepăr")
    closing_set.add("salut pepper")
    closing_set.add("salut pepăr")
    closing_set.add("bună ziua")
    closing_set.add("bună ziua pepper")
    closing_set.add("bună ziua pepăr")
    closing_set.add("bună pepper")
    closing_set.add("bună pepăr")
    closing_set.add("noroc pepăr")
    closing_set.add("noroc pepper")
    closing_set.add("servus pepăr")
    closing_set.add("servus pepper")


class RoSayings(RDSayings):
    """
    <p>Romanian version.</p>
    """

    OPENING_LINES = set()
    CLOSING_LINES = set()

    init_opening_lines(OPENING_LINES)
    init_closing_lines(CLOSING_LINES)

    def user_opening_statement(self, words):
        return RoSayings.filter_words(words) in RoSayings.OPENING_LINES

    def user_closing_statement(self, words):
        return RoSayings.filter_words(words) in RoSayings.CLOSING_LINES

    def robot_opening_lines(self):
        return ["Bună ziua!", "Cu ce vă pot ajuta?"]

    def robot_closing_lines(self):
        return ["La revedere."]

    def robot_dont_know_lines(self):
        return ["Nu știu.", "Această informație nu îmi este disponibilă."]

    def robot_didnt_understand_lines(self):
        return ["Nu am înțeles ce ați întrebat.", "Vă rog să reformulați."]

    @staticmethod
    def filter_words(words):
        matched_words = []
        for word in words:
            if not re.match(r'^\W+$', word):
                matched_words.append(word.strip().lower())
        return " ".join(matched_words)
