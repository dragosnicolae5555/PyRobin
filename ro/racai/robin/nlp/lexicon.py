from abc import ABCMeta, abstractmethod


class Lexicon(metaclass=ABCMeta):
    """
    <p>An interface to build a "verb" inventory
    with meanings given by the method name. Implement
    this for your language. Also add other meaning-related
    methods or word-related methods.</p>
    """

    @abstractmethod
    def is_command_verb(self, verb_lemma):
        """
        Checks a verb lemma for a "command" verb.
        :param verb_lemma: the verb lemma to check
        :return: {@code true} if lemma is a command verb
        """
        pass

    @abstractmethod
    def is_functional_pos(self, pos):
        """
        Checks if the POS belongs to a functional word.
        :param pos: the POS to check
        :return:{@code true} if {@code pos} belongs to a functional word.
        """
        pass

    @abstractmethod
    def is_functional_word(self, word):
        """
        Checks to see if {@code word} is a functional word.
        :param word: the word to be checked.
        :return: {@code true} if {@code word} is a functional word.
        """
        pass

    @abstractmethod
    def is_noun_pos(self, pos):
        """
        Checks if POS is a noun POS, with friends such as pronouns.
        :param pos: the POS to check
        :return: {@code true} if {@code pos} is a noun
        """
        pass

    @abstractmethod
    def is_pure_noun_pos(self, pos):
        """
        Checks if POS is a noun POS, only.
        :param pos: the POS to check
        :return: {@code true} if {@code pos} is a noun
        """
        pass

    @abstractmethod
    def is_skippable_pos(self, pos):
        """
        Checks if POS can be skipped at the beginning of the sentence.
        :param pos: the POS to check
        :return: {@code true} if {@code pos} is a preposition
        """
        pass
