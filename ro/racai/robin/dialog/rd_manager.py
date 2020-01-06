import getopt
import sys

from ro.racai.robin.dialog.rd_robot_behaviour import RDRobotBehaviour
from ro.racai.robin.dialog.ro_sayings import RoSayings
from ro.racai.robin.mw.mw_file_reader import MWFileReader
from ro.racai.robin.nlp.q_type import QType
from ro.racai.robin.nlp.ro_lexicon import RoLexicon
from ro.racai.robin.nlp.ro_text_processor import RoTextProcessor
from ro.racai.robin.nlp.ro_word_net import RoWordNet


class RDManager:
    """
    <p>This is the main entry point for the ROBIN Dialogue manager.</p>
    """

    def __init__(self, word_net, lexicon, text_processor, say):
        self.__resource_word_net = word_net
        self.__resource_lexicon = lexicon
        self.__resource_text_proc = text_processor
        self.__current_d_state = self.DialogueState()
        self.__resource_sayings = say

        self.__discourse_universe = None
        self.__microworld_name = None

    class DialogueState:
        """
        <p>This is the current state of the dialogue
        to be used by the client of this class.</p>
        """

        def __init__(self):
            # If this is not-null, the dialogue had ended
            # and the robot behaviour is defined and
            # ready to be used by the client;
            self.inferred_behaviour = None
            # This predicate was matched as being
            # the closest one to the user's input
            # from the universe of discourse.
            self.inferred_predicate = None
            # This field should be populated
            # with the response of the robot: either requesting
            # more information or providing the information for
            # saying it. Each string is to be sent separately
            # to the TTS engine.
            self.robot_reply = []
            # What was the type of the previous query.
            self.previous_query_type = None

        def is_dialogue_done(self):
            return self.inferred_behaviour is not None

        def get_reply(self):
            return self.robot_reply

        def get_behaviour(self):
            return self.inferred_behaviour

        @staticmethod
        def robot_says_something(qtyp, lines):
            """
            <p>Canned response when the robot says fixed things.</p>
            :param qtyp: query type to set on the state;
            :param lines:
            :return: a new {@link DialogueState} object.
            """
            state = RDManager.DialogueState()
            state.robot_reply = lines
            state.previous_query_type = qtyp
            return state

        @staticmethod
        def robot_informed_response(qtyp, pm):
            """
            <p>Canned response when the robot responds with
            the argument that checks the type of the query.</p>
            :param qtyp: query type;
            :param pm: predicate match object;
            :return: a new {@link DialogueState} object with
                    {@link RDRobotBehaviour} set.
            """
            state = RDManager.DialogueState()
            state.inferred_predicate = pm.matched_predicate
            state.robot_reply = []
            state.robot_reply.append(state.inferred_predicate.get_arguments()[pm.said_argument_index].get_reference())
            state.inferred_behaviour = RDRobotBehaviour(state.inferred_predicate.get_user_intent(),
                                                        state.inferred_predicate.get_arguments()[
                                                            pm.said_argument_index].get_reference())
            state.previous_query_type = qtyp
            return state

    def load_microworld(self, mw_file):
        """
        <p>Initialize the {@link #discourseUniverse} member field
        from the given {@code .mw} file.</p>
        :param mw_file:
        :return:
        """
        mwr = MWFileReader(mw_file)
        self.__discourse_universe = mwr.construct_universe(self.__resource_word_net,
                                                           self.__resource_lexicon,
                                                           self.__resource_text_proc)
        self.__microworld_name = mwr.get_microworld_name()
        # Set concepts on the text processor...
        self.__resource_text_proc.set_concept_list(self.__discourse_universe.get_universe_concepts())

    def get_microworld_name(self):
        return self.__microworld_name

    def get_concepts_as_string(self):
        concepts = []
        for concept in self.__discourse_universe.get_universe_concepts():
            concepts.append(str(concept))
        return "\n".join(concepts)

    def get_predicates_as_string(self):
        predicates = []
        for predicate in self.__discourse_universe.get_universe_predicates():
            predicates.append(str(predicate))
        return "\n".join(predicates)

    def do_conversation(self, user_input):
        """
        <p>This is the main method of the {@link RDManager}:
        it processes a textual user input are returns a
        {@link DialogueState} object.
        :param user_input: user input to operate with, comes
                    from the ASR module;
        :return: a current state of the dialogue.
        """
        q = self.__resource_text_proc.query_analyzer(self.__resource_text_proc.text_processor(user_input))
        if q.query_type == QType.HELLO:
            self.__current_d_state = self.DialogueState.robot_says_something(
                q.query_type,
                self.__resource_sayings.robot_opening_lines())
            return self.__current_d_state

        if q.query_type == QType.GOODBYE:
            self.__current_d_state = None
            return self.DialogueState.robot_says_something(q.query_type,
                                                           self.__resource_sayings.robot_closing_lines())

        # 1. Try and match the query first...
        pm = self.__discourse_universe.resolve_query(q)
        if pm.matched_predicate is None:
            # No predicate found, this means no
            # predicate was found in KB. Return this
            # and say we do not know about it.
            self.__current_d_state = self.DialogueState.robot_says_something(
                        q.query_type,
                        self.__resource_sayings.robot_dont_know_lines())
            return self.__current_d_state

        if pm.said_argument_index >= 0 and pm.is_valid_match:
            # 2. Some predicate matched. If we have an
            # argument that we could return, that's
            # a success.
            self.__current_d_state = self.DialogueState.robot_informed_response(q.query_type, pm)
        elif self.__current_d_state.inferred_predicate is not None:
            # 3. Some predicate matched but we don't have
            # enough information specified. Try to do a
            # match in the context of the previously
            # matched predicate.
            pm = self.__discourse_universe.resolve_query_in_context(q, self.__current_d_state.inferred_predicate)
            if pm.said_argument_index >= 0:
                self.__current_d_state = self.DialogueState.robot_informed_response(q.query_type, pm)
            else:
                self.__current_d_state = self.DialogueState.robot_says_something(
                    q.query_type,
                    self.__resource_sayings.robot_dont_know_lines)
        else:
            # No predicate found, this means no
            # predicate was found in KB. Return this
            # and say we do not know about it.
            self.__current_d_state = self.DialogueState.robot_says_something(
                        q.query_type,
                        self.__resource_sayings.robot_dont_know_lines)

        return self.__current_d_state

    def dump_resource_caches(self):
        """
        Method to dump the resource caches so that
        we avoid expensive calls the text processing
        or resource querying web services.
        :return:
        """
        # Make sure you save expensive calls
        # to local hard disk...
        self.__resource_text_proc.dump_text_cache()
        self.__resource_word_net.dump_word_net_cache()

    @staticmethod
    def romanian_diacritics(prompt):
        prompt = prompt.replace("a^", "â")
        prompt = prompt.replace("i^", "î")
        prompt = prompt.replace("a@", "ă")
        prompt = prompt.replace("s@", "ș")
        prompt = prompt.replace("t@", "ț")
        prompt = prompt.replace("A^", "Â")
        prompt = prompt.replace("I^", "Î")
        prompt = prompt.replace("A@", "Ă")
        prompt = prompt.replace("S@", "Ș")
        prompt = prompt.replace("T@", "Ț")

        return prompt


