from ro.racai.robin.dialog.rd_concept import RDConcept


class RDConstant(RDConcept):
    """
    <p>A "constant" is an instance of a concept for which
    we don't care about the name of the variable. For instance,
    <i>8:00</i> is an instance of the "hour" concept but we only
    keep the instance. Useful when we want to talk about these constants.</p>
    """

    def __init__(self, ctype, ref):
        super().__init__(ctype, ref)
        if not ref or not ref.strip():
            raise RuntimeError("Reference cannot be None, empty or blank!")

    def deep_copy(self):
        return RDConstant(self._concept_type, self._assigned_reference)

    def add_synonym(self, syn):
        """
        <p>Do nothing as constants do not have synonyms.</p>
        :param syn:
        :return:
        """
        print("do nothing")

    def __eq__(self, other):
        """
        <p>A constant can be equal to an instantiated concept
        having the same instance value and type.</p>
        :param other:
        :return:
        """
        if isinstance(other, RDConcept):
            if self._concept_type != other._concept_type:
                return False
            if other._assigned_reference is None and self._assigned_reference is None:
                return True
            elif other._assigned_reference is not None and self._assigned_reference is not None \
                    and other._assigned_reference.lower() == self._assigned_reference.lower():
                return True

        return False

    def __hash__(self):
        return hash(self._canonical_form)
