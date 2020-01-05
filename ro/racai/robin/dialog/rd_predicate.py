from ro.racai.robin.nlp.string_utils import StringUtils


class RDPredicate:
    """
    <p>This is the principal information unit that the
    dialogue system tries to determine if it is {@code true}
    or {@code false} within the {@link RDUniverse} we are reasoning with.<p>
    <p>A predicate is composed of:</p>
    <ul>
    <li>a predicate name along with its synonyms, e.g. "afla"
    "costa" or special predicates such as "locationOf", "timeOf",
    "whoIs", etc.</li>
    <li>a list of predicate arguments, all of type {@link RDConcept}</li>
    </ul>
    <p>Each question/query is transformed automatically in such a predicate such that:
    <ol>
    <li>if the predicate has all arguments bound, it is a "yes/no" question and the
    universe of discourse is used to see if predicate is {@code true} or {@code false};</li>
    <li>if the predicate has some of the arguments unbound, the universe of discourse is
    used to find the value for the remaining arguments such that the predicate is {@code true};</li>
    <li>if more than one predicate match, the dialogue manager asks new questions
    that can provide the data for disambiguation.</li>
    </ol>
    """

    def __init__(self, u_intent_type, verb):
        if StringUtils.is_none_empty_or_blank(verb):
            raise RuntimeError("Action verb cannot be null, empty or blank!")

        """
        The main "name" for this predicate.
        It is a lemma, usually extracted from
        the question (first informative verb). 
        """
        self.__action_verb = verb.strip().lower()
        """
        Type of user intention.
        """
        self.__user_intention = u_intent_type
        """
        Alternate names for the {@link #actionVerb}.
        """
        self.__synonyms_of_action_verb = []
        """
        The arguments of this predicate, in no special order.
        """
        self.__predicate_arguments = []

    def add_synonym(self, syn):
        """
        Adds a new "synonym" to this {@link #actionVerb}.
        :param syn: the synonym to add
        :return:
        """
        if StringUtils.is_none_empty_or_blank(syn):
            raise RuntimeError("Synonym may not be null, empty or blank!")
        self.__synonyms_of_action_verb.append(syn.strip().lower())

    def add_argument(self, rd_concept):
        self.__predicate_arguments.append(rd_concept)

    def get_arguments(self):
        """
        <p>Get the bound arguments of this predicate.</p>
        :return: a list with the predicate arguments.
        """
        return self.__predicate_arguments

    def get_action_verb(self):
        """
        <p>Get the action verb of this predicate.</p>
        :return: the {@link #actionVerb} member field.
        """
        return self.__action_verb

    def get_user_intent(self):
        """
        <p>Get the user intent associated with this predicate.</p>
        :return: the {@link #userIntention} member field.
        """
        return self.__user_intention

    @staticmethod
    def builder(u_intent_type, pform, syns, rd_concepts):
        """
        <p>Convenience static method for building a predicate.</p>
        :param u_intent_type: user intent defined in {@link UIntentType};
        :param pform: canonical form (lemma) for this predicate, e.g. <i>duce</i>;
        :param syns: synonyms for the canonical form (may be null or empty);
        :param rd_concepts: the list of fully instantiated {@link RDConcept}s which
                            are bound already, e.g. <i>laboratorul de informatică</i>.

        :return: an {@link RDPredicate}.
        """
        predicate = RDPredicate(u_intent_type, pform)
        if syns is not None:
            for syn in syns:
                predicate.add_synonym(syn)

        if rd_concepts is not None:
            for rd_concept in rd_concepts:
                predicate.add_argument(rd_concept)

        return predicate

    def deep_copy(self):
        """
        <p>Convenience method for returning a deep copy of this object.</p>
        :return: an exact duplicate of this object.
        """
        predicate = RDPredicate(self.__user_intention, self.__action_verb)
        if self.__synonyms_of_action_verb is not None:
            for syn in self.__synonyms_of_action_verb:
                predicate.add_synonym(syn)

        for rd_concept in self.__predicate_arguments:
            predicate.add_argument(rd_concept)

        return predicate

    def is_this_predicate(self, word, word_net):
        """
        <p>Tests if an arbitrary word refers to this predicate (name).</p>
        :param word: the word to be tested;
        :param word_net: the interface to WordNet; if {@code null}, it is not used;
        :return: {@code true} if the word signals the presence of this predicate.
        """
        word = word.strip().lower()
        if word == self.__action_verb:
            return True

        for syn in self.__synonyms_of_action_verb:
            if word == syn:
                return True

        if word_net is not None:
            return word_net.word_net_equals(word, self.__action_verb)

        return False

    def __str__(self):
        str_value = self.__action_verb + "("
        i = 0
        while i < len(self.__predicate_arguments) - 1:
            str_value = str_value + str(self.__predicate_arguments[i]) + ", "
            i += 1

        if len(self.__predicate_arguments) >= 1:
            str_value = str_value + str(self.__predicate_arguments[-1])

        str_value = str_value + ")"
        return str_value

    class PMatch:
        """
        <p>A predicate match object with the overall match score
        and individual arguments match scores.</p>
        """

        def __init__(self, predicate):
            self.matched_predicate = predicate
            self.arg_match_scores = float(len(predicate.get_arguments()))
            self.match_score = 0.0
            self.said_argument_index = -1
            self.is_valid_match = False
