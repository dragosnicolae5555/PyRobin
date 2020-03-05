import json
import logging
from urllib import parse

import requests

from ro.racai.robin.nlp.word_net import WordNet


class RoWordNet(WordNet):
    """
    <p>The Romanian WordNet class, implementing
    the {@link WordNet} interface.</p>
    """
    WORDNET_QUERY = "https://relate.racai.ro/index.php?path=rownws&word=#WORD#&sid=#ILI#&wn=ro"

    def __init__(self):
        super().__init__()

    def get_hypernyms(self, word):
        return RoWordNet.get_relation_members(word, "hypernym")

    def get_hyponyms(self, word):
        return RoWordNet.get_relation_members(word, "hyponym")

    @staticmethod
    def get_relation_members(word, real_name):
        members = []
        root = RoWordNet.json_word_net_response(word)
        if not bool(root):
            return members
        senses = root["senses"]
        for sense in senses:
            relations = sense["relations"]
            for relation in relations:
                relation_name = relation["rel"]
                if relation_name == real_name:
                    members.append(str(relation["tliteral"]))
        return members

    def get_synonyms(self, word):
        synonyms = []
        root = RoWordNet.json_word_net_response(word)
        if not bool(root):
            # If word is not found in WordNet...
            return synonyms
        senses = root["senses"]
        for sense in senses:
            synset = str(sense["literal"]).split(",")
            for syn in synset:
                if syn != word:
                    synonyms.append(syn)
        return synonyms

    @staticmethod
    def json_word_net_response(word):
        query = RoWordNet.WORDNET_QUERY
        word = parse.quote_plus(word, encoding="UTF-8")
        query = query.replace("#WORD#", word)
        query = query.replace("#ILI#", "")

        headers = {'Content-Type': 'application/json'}
        response = requests.get(url=query, headers=headers)
        status_code = response.status_code
     

        if status_code == 200:
            return json.loads(json.dumps(response.json()))
        else:
            logging.error("RELATE query error for word '" + word + "'; error code " + status_code)

        return None