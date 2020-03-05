import logging
import os
from abc import ABCMeta, abstractmethod


class WordNet(metaclass=ABCMeta):
    """
    <p>An interface to a WordNet-like semantic network.
    Currently used to retrieve words that form different
    semantic relations.</p>
    """

    def __init__(self, wn_equals_cache={},
                 wn_equals_cache_file=os.path.abspath(os.path.split(
                     os.path.abspath(os.path.realpath(__file__)))[0] + "/../../../../wordnet-cache.txt")):
        """
        :param wn_equals_cache: The equals cache map, to avoid
                                expensive calls to the RELATE platform.
        :param wn_equals_cache_file: Where to save the WordNet equals cache.
        """
        self._wn_equals_cache = wn_equals_cache
        self._wn_equals_cache_file = wn_equals_cache_file
        self.populate_word_net_equals_cache()

    def populate_word_net_equals_cache(self):
        if not os.path.exists(self._wn_equals_cache_file):
            # On first run this file does not exist yet.
            return
        rdr = open(self._wn_equals_cache_file, encoding="UTF-8")
        try:
            while True:
                line = rdr.readline()
                if line == '':
                    break
                parts = line.split()
                self._wn_equals_cache[parts[0]] = True if parts[1] == "true" else False
        except IOError as ioe:
            logging.warning("Could not open or read " + self._wn_equals_cache_file)
            logging.exception(ioe)
        finally:
            rdr.close()

    def dump_word_net_cache(self):
        try:
            wrt = open(self._wn_equals_cache_file, 'w', encoding="UTF-8")
            for eqk in self._wn_equals_cache:
                wrt.write(eqk + "\t" + self._wn_equals_cache[eqk] + "\n")
        except IOError as ioe:
            logging.warning("Could not open or write to " + self._wn_equals_cache_file)
            logging.exception(ioe)
        finally:
            wrt.close()

    @abstractmethod
    def get_hypernyms(self, word):
        """
        <p>Get a list of hypernyms a given {@code word}.</p>
        regardless of their senses.</p>
        :param word: the word to get hyponyms for;
        :return: {@link java.util.List} with the hypernyms of word, regardless of the meaning.
        """
        pass

    @abstractmethod
    def get_hyponyms(self, word):
        """
        <p>Get a list of hyponyms a given {@code word}.</p>
        regardless of their senses.</p>
        :param word: the word to get hyponyms for;
        :return: {@link java.util.List} with the hyponyms of word, regardless of the meaning.
        """
        pass

    @abstractmethod
    def get_synonyms(self, word):
        """
        <p>Get the list of synonyms for a given {@code word}.</p>
        :param word: the word to get synonyms for;
        :return: {@link java.util.List} with the synonyms of w,
                regardless of the meaning.
        """
        pass

    def word_net_equals(self, w1, w2):
        """
        <p>Does a WordNet first order neighborhood search to
        see if the two parameters can be made equal.</p>
        :param w1: first word parameter
        :param w2: second word parameter
        :return: {@code true} if {@code w1} and {@code w2}
                are synonyms, first order hyponyms/hypernyms
        """
        key12 = w1 + "#" + w2
        key21 = w2 + "#" + w1

        if key12 in self._wn_equals_cache:
            return self._wn_equals_cache[key12]
        if key21 in self._wn_equals_cache:
            return self._wn_equals_cache[key21]

        # Synonym check with WordNet
        for syn in self.get_synonyms(w1):
            if w2 == syn:
                self._wn_equals_cache[key12] = True
                self._wn_equals_cache[key21] = True
                return True

        # Use hypernyms from WordNet (only direct hypernyms)
        for hyper in self.get_hypernyms(w1):
            if w2 == hyper:
                self._wn_equals_cache[key12] = True
                self._wn_equals_cache[key21] = True
                return True

        # Use hyponyms from WordNet (only direct hyponyms)
        for hypo in self.get_hyponyms(w1):
            if w2 == hypo:
                self._wn_equals_cache[key12] = True
                self._wn_equals_cache[key21] = True
                return True

        self._wn_equals_cache[key12] = False
        self._wn_equals_cache[key21] = False
        return False