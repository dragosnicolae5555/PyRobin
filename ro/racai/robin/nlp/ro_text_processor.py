import json
import logging
from urllib import parse

import requests

from ro.racai.robin.dialog.ctype import CType
from ro.racai.robin.nlp.q_type import QType
from ro.racai.robin.nlp.text_processor import TextProcessor


class RoTextProcessor(TextProcessor):
    """
    <p>The Romanian implementation using
    <a href="http://relate.racai.ro:5000">RELATE</a>, the TEPROLIN web service.</p>
    """
    TEPROLIN_QUERY = "http://relate.racai.ro:5000/process"

    def __init__(self, lexicon, word_net, sayings):
        super().__init__(lexicon, word_net, sayings)

    def process_text(self, text):

        content = {}
        arguments = {"text": text}
        data = parse.urlencode(arguments, encoding="UTF-8")
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        response = requests.post(url=RoTextProcessor.TEPROLIN_QUERY, headers=headers, data=data)
        status_code = response.status_code
    

        if status_code == 200:
            content = json.loads(json.dumps(response.json()))
        else:
            logging.error("TEPROLIN query error for text '" + text + "'; error code " + status_code)

        tokens = []
        result = content["teprolin-result"]
        tokenized = result["tokenized"]
        tokenized_data = tokenized[0]

        for tk in tokenized_data:
            word_form = tk["_wordform"]
            lemma = tk["_lemma"]
            msd = tk["_msd"]
            head = int(tk["_head"])
            deprel = str(tk["_deprel"])

            tokens.append(self.Token(word_form, lemma, msd, head, deprel, False))

        return tokens

    def text_correction(self, text):
        # TODO: apply any text correction mechanisms here!
        return text

    def query_analyzer(self, query):
        if query is None:
            return None
        result = self.Query()
        action_verb_id = 0
        query_words = []

        for token in query:
            query_words.append(token.wform)

        # -1. If hello, return quickly.
        if self._sayings.user_opening_statement(query_words):
            result.query_type = QType.HELLO
            return result

        # 0. If goodbye, return quickly.
        if self._sayings.user_closing_statement(query_words):
            result.query_type = QType.GOODBYE
            return result

        # 1. Find the root of the sentence. This has to be a main verb.
        index = 0
        while index < len(query):
            t = query[index]
            if t.head == 0 and t.POS.startswith("Vm"):
                result.action_verb = t.lemma.lower()
                # These are 1-based
                action_verb_id += 1
                break
            index += 1

        if action_verb_id == 0:
            logging.error("Could not find an action verb in the query '" + self.query_to_string() + "'")
            return None

        # 2. Find all arguments (first dependents) of the action verb.
        # We only consider "noun" arguments, e.g. nouns, pronouns, abbreviations, numerals, etc.
        j_index = 0
        while j_index < len(query):
            tk = query[j_index]
            if tk.head == action_verb_id and self._lexicon.is_noun_pos(tk.POS):
                tk.is_action_verb_dependent = True
                below_indexes = []
                noun_phrase_indexes = []

                below_indexes.append(j_index + 1)
                RoTextProcessor.tree_under(query, below_indexes, noun_phrase_indexes)
                noun_phrase_indexes.sort()

                # -1 because all indexes are +1 to match
                # dependency parsing 1-based indexes
                noun_phrase = []
                for index in noun_phrase_indexes:
                    noun_phrase.append(query[index - 1])
                p_arg = self.Argument(noun_phrase, RoTextProcessor.is_query_variable(noun_phrase))
                result.predicate_arguments.append(p_arg)

            j_index += 1
        fti = 0
        # Skip non-interesting words at the beginning
        # of the user's sentence.
        while fti < len(query) and self._lexicon.is_skippable_pos(query[fti].POS):
            fti += 1

        if fti >= len(query) - 1:
            return None

        first_token = query[fti]
        second_token = query[fti + 1]

        # 3. Determine the query type.
        if self._lexicon.is_command_verb(result.action_verb):
            result.query_type = QType.COMMAND
        elif first_token.lemma == "cine":
            result.query_type = QType.PERSON
        elif first_token.lemma == "ce":
            if self._lexicon.is_pure_noun_pos(second_token.POS)\
                    and self._universe_concepts is not None:
                for c in self._universe_concepts:
                    if c.is_this_concept(second_token.lemma, self._word_net)\
                            and c.get_type() != CType.WORD:
                        switcher = {CType.PERSON: QType.PERSON,
                                    CType.LOCATION: QType.LOCATION,
                                    CType.TIME: QType.TIME
                                    }
                        result.query_type = switcher.get(c.get_type, QType.WHAT)
                        if result.query_type is not None:
                            break
            else:
                result.query_type = QType.WHAT
        elif first_token.lemma == "unde":
            result.query_type = QType.LOCATION
        elif first_token.lemma == "când":
            result.query_type = QType.TIME
        elif first_token.lemma == "cum":
            result.query_type = QType.HOW
        else:
            result.query_type = QType.YESNO

        return result

    @staticmethod
    def tree_under(query, check_heads, stored_heads):
        """
        Extracts the portion of the sentence under the
        dependency tree rooted at index.
        :param query: the list of tokens to use
        :param check_heads: list of heads to search for
                            in the dependency tree; initially
                            it only contains the root index
        :param stored_heads: list of heads that are "below"
                            root index
        :return: a list of integers for indexes
                that are "below" the starting index
        """
        added_heads = []
        for h in check_heads:
            index = 0
            while index < len(query):
                t = query[index]
                t_index = index + 1
                if t.head == h:
                    if t_index not in check_heads \
                            and t_index not in stored_heads \
                            and t_index not in added_heads:
                        added_heads.append(t_index)
                index += 1
        stored_heads.extend(check_heads)
        if len(added_heads) > 0:
            RoTextProcessor.tree_under(query, added_heads, stored_heads)

    # Debugging method.
    @staticmethod
    def query_to_string(query):
        wforms = []
        for token in query:
            wforms.append(token.wform)
        return " ".join(wforms)

    @staticmethod
    def is_query_variable(argument):
        if argument is not None and len(argument) > 0:
            first_index = 0
            if argument[0].POS.startswith("S"):
                # Remove first preposition, if it exists.
                first_index = 1

            # Relative pronoun/determiner/adverb
            if len(argument[first_index].POS) >= 2 and argument[first_index].POS[1] == 'w':
                return True

            if len(argument) == 1 and (argument[0].POS[0] in ("N", "Y", "M")):
                # If we have a single noun in the argument
                return True

        return False
