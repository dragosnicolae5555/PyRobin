import getopt
import sys
from collections.abc import Iterable 

from ro.racai.robin.dialog.rd_robot_behaviour import RDRobotBehaviour
from ro.racai.robin.dialog.rd_manager import RDManager
from ro.racai.robin.dialog.ro_sayings import RoSayings
from ro.racai.robin.mw.mw_file_reader import MWFileReader
from ro.racai.robin.nlp.q_type import QType
from ro.racai.robin.nlp.ro_lexicon import RoLexicon
from ro.racai.robin.nlp.ro_text_processor import RoTextProcessor
from ro.racai.robin.nlp.ro_word_net import RoWordNet

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], None)
    if len(args) != 1:
        print("python main.py <.mw file>")

    mw_file = args[0]
    rown = RoWordNet()
    rolex = RoLexicon()
    say = RoSayings()
    rotp = RoTextProcessor(rolex, rown, say)
    dman = RDManager(rown, rolex, rotp, say)

    dman.load_microworld(mw_file)

    print("Default charset: UTF-8\n")
    print("\n")
    print("Use the following convention:\n")
    print("(replace lower with upper-case for upper-case diacritics)\n")
    print("  a^ for â\n")
    print("  i^ for î\n")
    print("  a@ for ă\n")
    print("  s@ for ș\n")
    print("  t@ for ț\n")
    print("\n")
    print("Dialogue manager commands:\n")
    print("  'exit' or 'quit' to terminate this dialogue;\n")
    print("  'dump predicates' to print the list of ``known'' predicates in the KB;\n")
    print("  'dump concepts' to print the list of ``known'' bound concepts in the KB.\n")
    print("\n")

    # A text-based dialogue loop.
    # Type 'exit' or 'quit' to end it.
    print("Running with the " + dman.get_microworld_name() + " microworld")
    prompt = RDManager.romanian_diacritics(input("User> "))

    while len(prompt) > 0 and prompt.lower() != "exit" and prompt.lower() != "quit":
        prompt = prompt.strip()
        if prompt.startswith("dump"):
            parts = prompt.split()
            if parts[1] == "concepts":
                print(dman.get_concepts_as_string())
                print("\n")
            elif parts[1] == "predicates":
                print(dman.get_predicates_as_string())
                print("\n")
            else:
                print("Dialogue Manager> Unknown 'dump' command.")
                print("\n")
            prompt = RDManager.romanian_diacritics(input("User> "))
            continue
        dstat = dman.do_conversation(prompt)
        print("Pepper> ")
        if isinstance(dstat.get_reply()(), Iterable):
            print(" ".join(dstat.get_reply()()))
        else :      
            print(" ".join(dstat.get_reply()))
        print("\n")

        if dstat.is_dialogue_done():
            print(dstat.get_behaviour())

        prompt = RDManager.romanian_diacritics(input("User> "))

    dman.dump_resource_caches()