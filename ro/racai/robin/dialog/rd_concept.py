from ro.racai.robin.nlp.string_utils import StringUtils


class RDConcept:
    """
    <p>This class models a concept in the ROBIN Dialogue micro-world (e.g. universe of discourse).
    For instance, in our familiar PRECIS orientation scenario, a concept is the room where something
    happens. A concept can be expressed through a <i>canonical form</i>, e.g. Romanian <i>cameră</i>,
    through synonyms e.g. <i>sală</i> or through a noun phrase e.g. <i>sala de la parter</i>.
    <p>A concept is a typed variable <b>X</b> which has to be bound to a value at runtime. For instance,
    we could speak of <i>sala 209</i> or of <i>laboratorul de robotică</i>.
    """

    def __init__(self, concept_type, ref, cform=None):
        """
        this one is for creating a RDConstant
        :param concept_type: the type of the concept constant
        :param ref:
        """

        # Keeps the canonical form of the concept
        # For instance, Romanian <i>cameră</i>
        # TODO: No multiple meanings support yet.
        # <b>Important: no two concepts can have the
        # same canonical form! It is a limitation
        # for now.</b>
        if cform is not None and cform.strip():
            self._canonical_form = cform.strip().lower()
        else:
            self._canonical_form = None

        # This is the type of the concept, to be checked
        # and enforced when this concept is a predicate argument
        self._concept_type = concept_type

        # Alternate words for the {@link #canonicalForm}.
        # For instance, Romanian <i>sală</i> and <i>laborator</i>.
        self._synonyms_of_canonical_form = []

        # This is the reference of the concept from the micro-world.
        # If no reference has been assigned yet, leave this to null.
        self._assigned_reference = ref

        # The processed version of the {@link #assignedReference}.
        # To be filled in at the first request.
        self.assigned_reference_tokens = []

    @staticmethod
    def builder(ctyp, cform, syns, ref):
        """
        <p>Convenience static method for building a concept.</p>
        :param ctyp  type of the concept defined in {@link CType};
        :param cform canonical form (lemma) for this concept, e.g. <i>sală</i>
        :param syns  synonyms for the canonical form (may be null or empty);
        :param ref   the assigned (reference) value to this concept:
        """
        new_concept = RDConcept(ctyp, ref, cform)
        if syns:
            for s in syns:
                new_concept.add_synonym(s)
        return new_concept

    def deep_copy(self):
        """
        <p>Create a deep copy of this concept.
        All internal data structure are allocated on the heap
        for the new object.</p>
        :return: a deep copy of this object.
        """
        new_concept = RDConcept(self._concept_type, self._assigned_reference, self._canonical_form)
        if self._synonyms_of_canonical_form:
            for s in self._synonyms_of_canonical_form:
                new_concept.add_synonym(s)

        return new_concept

    def add_synonym(self, syn):
        """
        <p>Adds a synonym to this concept, by which the
        concept can be identified in text.</p>
        :param syn: the synonym string to be added.
        :return:
        """
        if syn in (None, '') or not syn.strip():
            raise RuntimeError('Synonym may not be null, empty or blank!')
        self._synonyms_of_canonical_form.append(syn.strip().lower())

    def set_reference(self, value, text_processor):
        """
        <p>Sets the reference for this concept.</p>
        :param value: the reference to be set
        :param text_processor:
        :return:
        """
        if value is not None:
            if self._assigned_reference is None \
                    or (self._assigned_reference is not None and value != self._assigned_reference):
                self._assigned_reference = value
                self.assigned_reference_tokens = text_processor.text_processor(self._assigned_reference)

    def get_reference(self):
        """
        <p>Returns the textual description (reference) for this
        concept in the given {@link RDUniverse}.</p>
        :return: the textual description (or reference) of
        this concept or {@code null} if there isn't one.
        """
        return self._assigned_reference

    def get_tokenized_reference(self):
        """
        <p>Gets the tokenized version of the reference
        for matching with user's sayings.</p>
        :return: the processed version of the
        {@link #assignedReference} member field.
        """
        return self.assigned_reference_tokens

    def get_canonical_name(self):
        """
        <p>Returns the "standard" name for this concept.</p>
        :return: the {@link #canonicalForm} member field.
        """
        return self._canonical_form

    def get_type(self):
        """
        <p>Returns the type of this concept.</p>
        :return: the {@link #conceptType} member field.
        """
        return self._concept_type

    def is_this_concept(self, word, word_net):
        """
        <p>Tests if an arbitrary word refers to this concept.</p>
        :param word: the word to be tested;
        :param word_net: the interface to WordNet; if {@code null}, it is not used;
        :return: {@code true} if the word signals the presence of this concept.
        """
        if self._canonical_form is None:
            return False
        word = word.strip().lower()
        if word == self._canonical_form:
            return True
        for syn in self._synonyms_of_canonical_form:
            if word == syn:
                return True

        if word_net is not None:
            return word_net.word_net_equals(word, self._canonical_form)

        return False

    def __str__(self):
        if not StringUtils.is_none_empty_or_blank(self._assigned_reference):
            return "'" + self._assigned_reference + "'" + "/" + self._concept_type.name

        return "'" + self._canonical_form + "'" + "/" + self._concept_type.name

    def __eq__(self, other):
        if isinstance(other, RDConcept):
            if self._concept_type != other._concept_type:
                return False
            if self._canonical_form == other._canonical_form:
                if self._assigned_reference is None and other._assigned_reference is None:
                    return True
                elif self._assigned_reference is not None and other._assigned_reference is not None \
                        and self._assigned_reference.lower() == other._assigned_reference.lower():
                    return True
        return False

    def __hash__(self):
        return hash(self._canonical_form)
