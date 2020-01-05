from abc import ABCMeta, abstractmethod


class RDSayings(metaclass=ABCMeta):
    """
    <p>Interface to check for fixed expressions,
    to be extended in each new language.</p>
    """

    @abstractmethod
    def user_opening_statement(self, words):
        """
        User has started the dialogue with a "Hello" or
        "Hello Pepper" or similar.

        :param words: a list of words to check if
        they mark the start of the conversation (SOC)
        :return: {@code true} if words mark the SOC
        """
        pass

    @abstractmethod
    def user_closing_statement(self, words):
        """
         User has ended the dialogue with a "Thank you" or "Goodbye".

        :param words: a list of words to check if
        they mark the end of the conversation (EOC)
        :return: {@code true} if words mark the EOC
        """
        pass

    @abstractmethod
    def robot_opening_lines(self):
        """
        What the robot says to start the conversation.

        :return: the list of string to be said;
        each string is sent separately
        to the TTS module.
        """
        pass

    @abstractmethod
    def robot_closing_lines(self):
        """
        What the robot says to end the conversation.

        :return: the list of string to be said;
        each string is sent separately
        to the TTS module.
        """
        pass

    @abstractmethod
    def robot_dont_know_lines(self):
        """
        What the robot says for "I don't know."
        the list of string to be said;
        each string is sent separately
        to the TTS module.

        :return:
        """
        pass

    @abstractmethod
    def robot_didnt_understand_lines(self):
        """
        What the robot says for "I didn't understand."
        the list of string to be said;

        :return: the list of string to be said;
        each string is sent separately
        to the TTS module.
        """
        pass
