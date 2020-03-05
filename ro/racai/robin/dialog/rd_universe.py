from ro.racai.robin.dialog.ctype import CType
from ro.racai.robin.dialog.rd_predicate import RDPredicate
from ro.racai.robin.nlp.levenshtein import Levenshtein
from ro.racai.robin.nlp.q_type import QType


class RDUniverse:
    """
    <p>This class describes the universe of discourse for a given
    micro-word. That is, it maps {@link ro.racai.robin.dialog.RDConcept}s
    to actual, textual descriptions of existing objects, being an <b>inventory</b>
    of ``known'' values for all concepts. For instance,
    in our PRECIS scenario, for the <i>sală</i> concept, we could have
    values such as <i>209</i>, <i>laboratorul de SDA</i>, etc.</p>
    <p>This class has to be sub-classed so that the correspondence
    is made by database interrogation, XML files, etc.</p>
    """

    def __init__(self, word_net, lexicon, text_processor):
        """
        <p>Universe of discourse constructor.</p>
        :param word_net: a WordNet instance for your language;
        :param lexicon: a lexicon instance for your language.
        :param text_processor:
        """
        # Bound concepts in this universe of discourse.
        # Fill in this list using {@link #addConcept(RDConcept)}.
        self.concepts = []
        # Predicates that are true in this universe.
        # Use {@link #addPredicate()} method to fill in this list.
        self.predicates = []
        # The word distance object used to compute
        # Levenshtein distances.
        self.word_distance = Levenshtein()
        # The WordNet object that is used to find
        # "similar" words.
        self.word_net = word_net
        # Lexicon to test for functional words
        # when matching descriptions.
        self.lexicon = lexicon
        # The TextProcessor to use to compute
        # a special type of sentence length.
        self.text_processor = text_processor

    def get_universe_concepts(self):
        """
        <p>Get the universe instantiated concepts to pass on
        to the text processor or to print.</p>
        :return:  the list of bound concepts that exist in this universe.
        """
        return self.concepts

    def get_universe_predicates(self):
        """
        <p>Get the universe instantiated predicates to print.</p>
        :return: the list of bound predicates that exist in this universe.
        """
        return self.predicates

    def add_concept(self, conc):
        """
        <p>Adds a concept built with {@link RDConcept#Builder(CType, String, List, String)} to
        this universe of discourse. Note that the textual description {@link RDConcept#getReference()}
        must not be null!
        :param conc: the bound (instantiated) concept to be added to this universe
        :return: void
        """
        self.concepts.append(conc)

    def add_predicate(self, pred):
        """
        <p>Adds a ``true'' predicate to this universe of discourse.
        :param pred: the predicate to add to this universe
        :return:
        """
        self.predicates.append(pred)

    def add_predicates(self, preds):
        self.predicates.clear()
        self.predicates.extend(preds)

    def resolve_query(self, query):
        """
        <p>Checks each predicate from this universe of discourse
        and assigns a match score.</p>
        :param query: the parsed {@link Query} object from the
                    user utterance;
        :return: the predicate match object which best matches the query;
                {@code null} if no predicate matched. It's safe to say that
                the information is not in the Knowledge Base in this case.
        """
        result = None
        max_score = 0.0
        for pred in self.predicates:
            pm = self.score_query_against_predicate(query, pred)
            if pm is not None and pm.match_score > max_score:
                result = pm
                max_score = pm.match_score
        return result

    def resolve_query_in_context(self, query, pred):
        """
        <p>If user asks something else, in the context of the first utterance,
        try and find some other argument of the previously matched predicate
        which could be the answer...</p>
        :param query: the parsed {@link Query} object from the user's utterance
        :param pred: the previously matched predicate which could
                    hold information that the user wants with
                    its current, incomplete query.
        :return: {@code null} if no information could be extracted or
                a new predicate match if new information could be extracted.
        """
        # 1. Match the action verb of the query with the one of the predicate
        if not pred.is_this_predicate(query.action_verb, self.word_net):
            return None
        # Predicate bound arguments
        pred_args = pred.get_arguments()
        # User query tokens making up syntactic arguments of the verb
        query_args = query.predicate_arguments
        result = RDPredicate.PMatch(pred)

        for q_arg in query_args:
            if q_arg.is_query_variable:
                i = 0
                while i < len(pred_args):
                    p_arg = pred_args[i]
                    if q_arg.is_query_variable and\
                            self.is_of_same_type(p_arg, q_arg, query.query_type):
                        result.said_argument_index = i
                        break
                    i += 1
                break
        if result.said_argument_index >= 0:
            result.is_valid_match = True
            return result
        return None

    def is_concept_instance(self, user_tokens, bound_concept):
        """
        <p>Verifies if the user description of a concept matches
        the given bound concept.</p>
        :param user_tokens: the user description of the concept;
        :param bound_concept: the target bound concept to do the matching against.
        :return: {@code true} if description matches the concept.
        """
        for tok in user_tokens:
            if tok.is_action_verb_dependent and not self.lexicon.is_functional_pos(tok.POS):
                if bound_concept.is_this_concept(tok.lemma, self.word_net) \
                        or bound_concept.is_this_concept(tok.wform, self.word_net):
                    return True
        return False

    def score_query_against_predicate(self, query, pred):
        # 1. Match the action verb of the query with the one of the predicate
        if not pred.is_this_predicate(query.action_verb, self.word_net):
            return None

        # Match the syntactic arguments with logical (bound) arguments
        # Predicate bound arguments
        pred_args = pred.get_arguments()
        # User query tokens making up syntactic arguments of the verb
        query_args = query.predicate_arguments
        """
        Find the maximal sum assignment of query arguments
        to predicate arguments
        Matrix is symmetrical
        """
        match_scores = [[0]*len(query_args) for i in range(len(pred_args))]
        ij_pairs = set()
        i = 0
        while i < len(pred_args):
            p_arg = pred_args[i]
            j = 0
            while j < len(query_args):
                q_arg = query_args[j]
                q_arg_toks = query_args[j].arg_tokens
                match_scores[i][j] = 0.0
                if (str(j) + "#" + str(i)) in ij_pairs:
                    # Matrix is symmetrical, where it can.
                    match_scores[i][j] = match_scores[j][i]
                elif q_arg.is_query_variable and self.is_of_same_type(p_arg, q_arg, query.query_type):
                    """
                    A query type that matches argument
                    is counted as a argument match.
                    """
                    match_scores[i][j] = float(1.0)
                    ij_pairs.add(str(i) + "#" + str(j))
                elif self.is_concept_instance(q_arg_toks, p_arg):
                    # Else, the argument is fuzzy scored against user's description.
                    match_scores[i][j] = self.description_similarity(p_arg.get_tokenized_reference(), q_arg_toks)
                    ij_pairs.add(str(i) + "#" + str(j))
                j += 1
            i += 1
        result = RDPredicate.PMatch(pred)
        # Predicate has matched, at least with its name.
        result.match_score = 1.0
        i = 0
        while i < len(pred_args):
            p_arg = pred_args[i]
            max_score = 0.0
            j = 0
            while j < len(query_args):
                q_arg = query_args[j]
                if match_scores[i][j] > max_score:
                    max_score = match_scores[i][j]
                if q_arg.is_query_variable and\
                        self.is_of_same_type(p_arg, q_arg, query.query_type) and\
                        result.said_argument_index == -1:
                    result.said_argument_index = i
                j += 1
            result.match_score += max_score
            result.arg_match_scores[i] = max_score
            i += 1
        # 1.0 for the predicate name and 1.0 of the query variable.
        result.is_valid_match = (result.match_score > 2.0)
        return result

    def is_of_same_type(self, con, arg, qtyp):
        """
        <p>Will say {@code true} if this concept is of the same type
        as the query, that is if query could be asking for this concept.
        :param con: the concept to be matched against...
        :param arg: the argument that was extracted from the user's query;
        :param qtyp:
        :return: {@code true} if query is asking for this.
        """
        if con.get_type() == CType.WORD and qtyp == QType.WHAT:
            for t in arg.arg_tokens:
                if self.lexicon.is_noun_pos(t.POS):
                    if t.lemma.lower() == con.get_canonical_name().lower():
                        return True
        elif qtyp == QType.PERSON and con.get_type() == CType.PERSON:
            return True
        elif qtyp == QType.LOCATION and con.get_type() == CType.LOCATION:
            return True
        elif qtyp == QType.TIME and con.get_type() == CType.TIME:
            return True

        return False

    def description_similarity(self, description, reference):
        """
        <p>Detects if two lists of words are ``similar''. Word matching
        is done in a lower-case manner, using string equality, WordNet and
        Levenshtein distances.</p>
        <p>If {@code i, j} are the indexes of the words aligning with
        the lowest Levenshtein distance L, we output
        sum((|i - j| + 1) * (L + 1)) / (length(description) + length(reference)).</p>
        :param description: list of description tokens that is to be matched;
        :param reference: list of reference tokens that is to be matched;
        :return: a real number that is 1.0f if the two entities
        are exactly equal and less than 1 for a degree of
        similarity.
        """
        sum = 0
        d_len = self.text_processor.no_functional_words_length(description)
        r_len = self.text_processor.no_functional_words_length(reference)

        i = 0
        while i < len(description):
            L = 1000
            j = len(reference)
            li = description[i].lemma
            wi = description[i].wform

            if self.lexicon.is_functional_pos(description[i].POS):
                i += 1
                continue
            jj = 0
            while jj < len(reference):
                if self.lexicon.is_functional_pos(reference[jj].POS):
                    # Skip functional words from match.
                    jj += 1
                    continue
                wjj = reference[jj].wform
                ljj = reference[jj].lemma

                if li.lower() == ljj.lower() or self.word_net.word_net_equals(li, ljj):
                    L = 0
                    j = jj
                    jj += 1
                    break
                else:
                    d = self.word_distance.distance(wi.lower(), wjj.lower(), 5)
                    if d < L:
                        L = d
                        j = jj
                jj += 1
            # end jj
            sum += (abs(i - j) + 1) * (L + 1)
            i += 1
        # end i
        d_score = float(sum) / float(d_len)
        r_score = float(sum) / float(r_len)

        return 2.0/(d_score + r_score)