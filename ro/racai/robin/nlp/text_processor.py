import logging
import os
import re
from abc import ABCMeta, abstractmethod


class TextProcessor(metaclass=ABCMeta):
    """
    <p>This class will take a bare text String and it will
    add POS tagging, lemmatization and dependency parsing.</p>
    """

    def __init__(self, lexicon, word_net, sayings=None,
                 universe_concepts=None,
                 processed_text_cache_file=os.path.abspath(os.path.split(
                     os.path.abspath(os.path.realpath(__file__)))[0] + "/../../../../processed-text-cache.txt"),
                 processed_text_cache={}):
        """
        :param universe_concepts:  This is the list of instantiated concepts constructed
                    during the creation of the micro-world. The text processor
                    must know about them to properly set the query type.
                    If {@code null}, it will NOT be used.
        :param lexicon: Lexicon to use for text processing.
        :param word_net: WordNet to use in text processing.
        :param sayings: Fixed expressions to be recognized.
        :param processed_text_cache_file: Save expensive text processing calls
                    to the TEPROLIN web service.
        :param processed_text_cache:
        """
        self._lexicon = lexicon
        self._sayings = sayings
        self._universe_concepts = universe_concepts
        self._word_net = word_net
        self.__processed_text_cache_file = processed_text_cache_file
        self._processed_text_cache = processed_text_cache
        self.populate_processed_text_cache()

    class Token:
        """
        <p>Represents an annotated token of the input text.
        The member field names are self explanatory.</p>
        """

        def __init__(self, wform, lemma, pos, head, drel, avd):
            """
            :param wform:
            :param lemma:
            :param pos:
            :param head: Head of this token in the dependency tree.
            :param drel: The name of the dependency relation that holds between this token and its
                        head.
            :param avd: True if this token is directly linked
                        to the action verb of the query.
            """
            self.wform = wform
            self.lemma = lemma
            self.POS = pos
            self.head = head
            self.drel = drel
            self.is_action_verb_dependent = avd

        def text_record(self):
            return self.wform + "\t" + self.lemma + "\t" + \
                   self.POS + "\t" + self.drel + "\t" + str(self.head) + \
                   "\t" + str(self.is_action_verb_dependent)

        def __str__(self):
         
            return self.wform + "/" + self.lemma \
                   + "/" + self.POS + " " + self.drel + "<-" + str(self.head)

    class Argument:
        """
        <p>This is the ``argument'' of a predicate, as
        seen in the syntactic parsing of the sentence.</p>
        """

        def __init__(self, toks, isvar):
            """
            :param toks:
            :param isvar: <p>{@code true} if this argument represents
            the missing information that the user requires.</p>
            <p>For example:</p>
            <p><i>În ce sală se desfășoară cursul de informatică?</i></p>
            <p>Here, ``În ce sală'' is the query variable.</p>
            """
            self.arg_tokens = toks
            self.is_query_variable = isvar

    class Query:
        """
         <p>This is the query object that has been extracted
         from the user's request in written Romanian.</p>
        """

        def __init__(self, query_type=None, action_verb=None, predicate_arguments=[]):
            """
            :param query_type: What the query asks for,e.g. a person, a location, etc.
            :param action_verb: What is the main verb (lemma) of the query/question.
                                It can be a command-type verb, e.g. "duce", "conduce",
                                "arată", etc. or some informative verb such as "costa",
                                "fi", "afla", etc.
            :param predicate_arguments: Arguments of the {@link #actionVerb}.
                                        An instantiation of an {@link RDConcept} -- to be matched
                                        against a concept, e.g. "laboratorul de robotică".
            """
            self.query_type = query_type
            self.action_verb = action_verb
            self.predicate_arguments = predicate_arguments

    def text_processor(self, text):
        """
        <p>Give it a text (from the ASR engine) and get back
        a list of {@link Token}s that are annotated.</p>
        :param text: the text to be analyzed
        :return: the list of tokens to work with
        """
        text = self._normalize_text(text)
        text = self.text_correction(text)
        if text in self._processed_text_cache:
            return self._processed_text_cache[text]

        proc_text = self.process_text(text)
        self._processed_text_cache[text] = proc_text
        return proc_text

    def no_functional_words_length(self, sentence):
        """
        <p>Returns the length of a sentence disregarding functional words.</p>
        :param sentence: the sentence to compute length for;
        :return: the number of content words in the sentence.
        """
        length = 0
        if sentence is None:
            return length
        for token in sentence:
            if not self._lexicon.is_functional_pos(token.POS):
                length += 1
        return length

    def populate_processed_text_cache(self):
        """
        :return:
        """
        if not os.path.exists(self.__processed_text_cache_file):
            return
        try:
            rdr = open(self.__processed_text_cache_file, encoding="UTF-8")
            line = rdr.readline()
            while line != '':
                line = line.rstrip("\n")
                text = line
                text_proc = []
                line = rdr.readline()
                while len(line) > 0 and line != "\n":
                    line = line.rstrip("\n")
                    parts = line.split()
                    wform = parts[0]
                    lemma = parts[1]
                    POS = parts[2]
                    drel = parts[3]
                    head = int(parts[4])
                    avd = True if parts[5].lower() == "true" else False

                    text_proc.append(self.Token(wform, lemma, POS, head, drel, avd))
                    line = rdr.readline()
                self._processed_text_cache[text] = text_proc
                line = rdr.readline()
        except IOError as ioe:
            logging.warning("Could not open or read " + self.__processed_text_cache_file)
            logging.exception(ioe)
        finally:
            rdr.close()

    def dump_text_cache(self):
        try:
            wrt = open(self.__processed_text_cache_file, "w", encoding="UTF-8")
            for key in self._processed_text_cache:
                wrt.write(key + "\n")
                for token in self._processed_text_cache[key]:
                    wrt.write(token.text_record() + "\n")
                wrt.write("\n")
        except IOError as ioe:
            logging.warning("Could not open or write to " + self.__processed_text_cache_file)
            logging.exception(ioe)
        finally:
            wrt.close()

    @abstractmethod
    def process_text(self, text):
        """
        <p>Implement this to get the annotations inside a {@link Token}.</p>
        :param text: text to be processed
        :return: the list of tokens
        """
        pass

    @abstractmethod
    def text_correction(self, text):
        """
        <p>If the text comes from an ASR engine, it may have
         errors, so use this method to correct it if possible.</p>
        :param text: text to be corrected
        :return: the fixed text
        """
        pass

    @abstractmethod
    def query_analyzer(self, query):
        """
        <p>Main method of query analysis. This method will
         construct a "parse" of the text query received,
         in the instance of a {@link Query} object.</p>
        :param query: the text query to be mined for the
        action verb and its arguments.
        :return: the {@link Query} object or {@code null}
        if something went wrong.
        """
        pass

    def _normalize_text(self, text):
        """
        <p>Optional call before calling {@link #processText(String)}.</p>
        :param text: the text to be normalized
        :return: normalized text
        """
        text = text.strip()
        text = re.sub(' +', ' ', text)
        return text

    @abstractmethod
    def is_query_variable(self, argument):
        """
        <p>Checks to see if list of tokens could represent
        a ``variable'', e.g. ``cine'', ``unde'', ``ce sală'', etc.</p>
        :param argument: the list of tokens to check for a variable;
        :return: {@code true} if this list of tokens represents a variable.
        """
        pass

    def set_concept_list(self, con_list):
        """
        <p>Used to the the concept list to be used in this processor.</p>
        :param con_list: the concept list to be set.
        :return:
        """
        self._universe_concepts = con_list