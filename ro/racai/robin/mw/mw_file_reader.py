import logging
import os
import re

from ro.racai.robin.dialog.ctype import CType
from ro.racai.robin.dialog.ctype import get_member_regex
from ro.racai.robin.dialog.rd_concept import RDConcept
from ro.racai.robin.dialog.rd_constant import RDConstant
from ro.racai.robin.dialog.rd_predicate import RDPredicate
from ro.racai.robin.dialog.rd_universe import RDUniverse
from ro.racai.robin.dialog.u_intent_type import UIntentType
from ro.racai.robin.mw.rd_microworld import RDMicroworld
from ro.racai.robin.nlp.string_utils import StringUtils


class MWFileReader(RDMicroworld):
    """
    <p>Builds an {@link RDUniverse} from a text {@code .mw} file.
    For an example file, please check the {@code src/main/resources/precis.mw} file.
    Instructions on how to create a new micro-world are in this file, as comments.</p>
    """
    # CONCEPT sală, laborator, cameră -> LOCATION
    CONCEPT_PATT = "^CONCEPT\\s+(.+)\\s*->\\s*([A-Z_]+)$"

    # REFERENCE curs laboratorul de informatică = C1
    REFERENCE_PATT = "^REFERENCE\\s+([^ \\t]+)\\s+([^=]+?)\\s*=\\s*([a-zA-Z0-9]+)$"

    # TIME marți, 8:00 = T1
    # PERSON Adriana Vlad = P1
    CTYPE_PATT = "^" + get_member_regex() + "\\s+([^=]+?)\\s*=\\s*([a-zA-Z0-9]+)$"

    # PREDICATE ține, desfășura -> EXPLAIN_SOMETHING
    PREDICATE_PATT = "^PREDICATE\\s+(.+)\\s*->\\s*([A-Z_]+)$"

    def __init__(self, file):
        """
        <p>Constructs a {@code .mw} file reader from a given file.</p>
        :param file: the file containing the micro-world definition.
        """
        self.mw_file_path = file

    def construct_universe(self, word_net, lexicon, text_processor):
        rdr = open(self.mw_file_path, encoding="UTF-8")
        line = rdr.readline()
        defined_concepts = []
        defined_predicates = []
        referenced_concepts = {}
        true_predicates = []

        line_count = 1

        while line != '':
            line = line.strip()
            if line.startswith("#"):
                # Skip comment lines
                line = rdr.readline()
                line_count += 1
                continue

            if line.startswith("CONCEPT") or line.startswith("CONCEPT\t"):
                cm = re.match(MWFileReader.CONCEPT_PATT, line)
                if cm is not None:
                    csyn = cm.group(1)
                    ctyp = cm.group(2)
                    try:
                        concept_type = CType[ctyp]
                    except KeyError as ke:
                        logging.error("'" + ctyp + "' " +
                                      "is not a recognized ro.racai.robin.dialog.CType " +
                                      "member at line " + str(line_count) + "!")
                        logging.exception(ke)
                        rdr.close()
                        return None
                    if "," in csyn:
                        syn_parts = re.split(",\\s+", csyn)
                        canon_name = syn_parts.pop(0)
                        defined_concepts.append(RDConcept.builder(concept_type, canon_name, syn_parts, None))
                    else:
                        defined_concepts.append(RDConcept.builder(concept_type, csyn, [], None))
                else:
                    logging.warning("CONCEPT line is not well-formed at line " + str(line_count) + "...")
            # end CONCEPT keyword
            elif line.startswith("REFERENCE ") or line.startswith("REFERENCE\t"):
                if len(defined_concepts) <= 0:
                    logging.error("Found references for missing concepts. " +
                                  "Please start with CONCEPT definitions.")
                    rdr.close()
                    return None
                rm = re.match(MWFileReader.REFERENCE_PATT, line)
                if rm is not None:
                    canon_name = rm.group(1)
                    reference = rm.group(2)
                    ref_code = rm.group(3)
                    concept_found = False

                    for c in defined_concepts:
                        if c.get_canonical_name() == canon_name:
                            nc = c.deep_copy()
                            nc.set_reference(reference, text_processor)
                            if ref_code not in referenced_concepts:
                                referenced_concepts[ref_code] = nc
                                concept_found = True
                                break
                            else:
                                logging.error("Reference code '" + ref_code +
                                              "' is duplicated at line " + str(line_count) + "!")
                                rdr.close()
                                return None
                    if not concept_found:
                        logging.error("Found reference for a missing concept '" + canon_name +
                                      "' at line " + str(line_count) + ". " +
                                      "Please add a CONCEPT definition above.")
                        rdr.close()
                        return None
                else:
                    logging.warning("REFERENCE line is not well-formed at line " + str(line_count) + "...")
            # end REFERENCE keyword
            elif re.match(MWFileReader.CTYPE_PATT, line) is not None:
                ctm = re.match(MWFileReader.CTYPE_PATT, line)
                const_type = CType[ctm.group(1)]
                const_value = ctm.group(2)
                constant = RDConstant(const_type, const_value)
                const_code = ctm.group(3)

                if const_code not in referenced_concepts:
                    referenced_concepts[const_code] = constant
                else:
                    logging.error("Constant concept code '" + const_code +
                                  "' is duplicated at line " + str(line_count) + "!")
                    rdr.close()
                    return None
            # end CType keyword
            elif line.startswith("PREDICATE ") or line.startswith("PREDICATE\t"):
                pm = re.match(MWFileReader.PREDICATE_PATT, line)
                if pm is not None:
                    psyn = pm.group(1)
                    usri = pm.group(2)
                    user_intent = None

                    try:
                        user_intent = UIntentType[usri]
                    except KeyError as ke:
                        logging.error("'" + usri + "' " +
                                      "is not a recognized ro.racai.robin.dialog.UIntentType " +
                                      "member at line " + str(line_count) + "!")
                        logging.exception(ke)
                        rdr.close()
                        return None

                    if "," in psyn:
                        syn_parts = re.split(",\\s+", psyn)
                        canon_name = syn_parts.pop(0)
                        defined_predicates.append(RDPredicate.builder(user_intent, canon_name, syn_parts, None))
                    else:
                        defined_predicates.append(RDPredicate.builder(user_intent, psyn, [], None))
                else:
                    logging.warning("PREDICATE line is not well-formed at line " + str(line_count) + "...")
            # end PREDICATE keyword
            elif line.startswith("TRUE ") or line.startswith("TRUE\t"):
                true_parts = line.split()
                action_verb = true_parts[1]
                predicate_found = False

                for p in defined_predicates:
                    if p.get_action_verb().lower() == action_verb.lower():
                        np = p.deep_copy()
                        # Add arguments to the predicate
                        index = 2
                        while index < len(true_parts):
                            ref_code = true_parts[index]
                            if ref_code in referenced_concepts:
                                np.add_argument(referenced_concepts[ref_code])
                            else:
                                logging.error("Reference code '" + ref_code +
                                              "' was not declared before at " + str(line_count) + "!")
                                rdr.close()
                                return None
                            index += 1
                            # end all arguments
                        predicate_found = True
                        true_predicates.append(np)
                        break
                    # end predicate found
                # end all defined predicates
                if not predicate_found:
                    logging.error("Predicate '" + action_verb +
                                  "' was not declared before with a PREDICATE line, at " + str(line_count) + "!")
                    rdr.close()
                    return None
            # end TRUE keyword
            line = rdr.readline()
            line_count += 1
        # end all .mw file
        rdr.close()
        universe = RDUniverse(word_net, lexicon, text_processor)
        universe.add_predicates(true_predicates)
        for ref in referenced_concepts:
            universe.add_concept(referenced_concepts[ref])

        return universe

    def get_microworld_name(self):
        file_name = os.path.basename(self.mw_file_path)
        file_name = re.sub("\\.mw$", "", file_name)
        file_name = file_name.upper()
        return file_name
