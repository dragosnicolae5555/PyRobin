from abc import ABCMeta, abstractmethod


class RDMicroworld(metaclass=ABCMeta):
    """
    <p>All micro-world builders have to implement this interface.</p>
    """

    @abstractmethod
    def construct_universe(self, word_net, lexicon, text_processor):
        """
        <p>Construct a universe from your source of choice.
        You can even write Java code to construct the universe.</p>
        :param word_net: the WordNet object to be used in the creation
                        of the {@link RDUniverse} object;
        :param lexicon:  the lexicon object to be used in the creation
                        of the {@link RDUniverse} object;
        :param text_processor: the text processor to be used in the creation
                        of the {@link RDUniverse} object.
        :return:    the constructed universe, populated with bound
                     {@link RDConcept}s and {@link RDPredicate}s.
        """
        pass

    @abstractmethod
    def get_microworld_name(self):
        """
        <p>To pretty-print this micro-world, get its name.</p>
        :return: the name of this micro-world.
        """
        pass
