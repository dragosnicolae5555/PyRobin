import re

from ro.racai.robin.nlp.lexicon import Lexicon


class RoLexicon(Lexicon):
    """
    <p>Romanian action verbs to be used in ROBIN Dialog.</p>
    """
    STOP_WORDS = set()

    # Generated automatically from
    # tbl.wordform.ro.v87
    STOP_WORDS.add("a")
    STOP_WORDS.add("acea")
    STOP_WORDS.add("aceasta")
    STOP_WORDS.add("această")
    STOP_WORDS.add("aceea")
    STOP_WORDS.add("aceeași")
    STOP_WORDS.add("acei")
    STOP_WORDS.add("aceia")
    STOP_WORDS.add("aceiași")
    STOP_WORDS.add("acel")
    STOP_WORDS.add("acela")
    STOP_WORDS.add("același")
    STOP_WORDS.add("acele")
    STOP_WORDS.add("acelea")
    STOP_WORDS.add("aceleași")
    STOP_WORDS.add("acelei")
    STOP_WORDS.add("aceleia")
    STOP_WORDS.add("aceleiași")
    STOP_WORDS.add("acelor")
    STOP_WORDS.add("acelora")
    STOP_WORDS.add("acelorași")
    STOP_WORDS.add("acelui")
    STOP_WORDS.add("aceluia")
    STOP_WORDS.add("aceluiași")
    STOP_WORDS.add("acest")
    STOP_WORDS.add("acesta")
    STOP_WORDS.add("aceste")
    STOP_WORDS.add("acestea")
    STOP_WORDS.add("acestei")
    STOP_WORDS.add("acesteia")
    STOP_WORDS.add("acești")
    STOP_WORDS.add("aceștia")
    STOP_WORDS.add("acestor")
    STOP_WORDS.add("acestora")
    STOP_WORDS.add("acestui")
    STOP_WORDS.add("acestuia")
    STOP_WORDS.add("ăi")
    STOP_WORDS.add("aia")
    STOP_WORDS.add("ăia")
    STOP_WORDS.add("aiasta")
    STOP_WORDS.add("aiastă")
    STOP_WORDS.add("aidoma")
    STOP_WORDS.add("ăilalți")
    STOP_WORDS.add("aista")
    STOP_WORDS.add("al")
    STOP_WORDS.add("ăl")
    STOP_WORDS.add("ăla")
    STOP_WORDS.add("ălălalt")
    STOP_WORDS.add("alaltă")
    STOP_WORDS.add("alde")
    STOP_WORDS.add("ale")
    STOP_WORDS.add("alea")
    STOP_WORDS.add("ălei")
    STOP_WORDS.add("ăleia")
    STOP_WORDS.add("alelalte")
    STOP_WORDS.add("alor")
    STOP_WORDS.add("ălor")
    STOP_WORDS.add("ălora")
    STOP_WORDS.add("ălorlalți")
    STOP_WORDS.add("alt")
    STOP_WORDS.add("alta")
    STOP_WORDS.add("altă")
    STOP_WORDS.add("altceva")
    STOP_WORDS.add("altcineva")
    STOP_WORDS.add("altcuiva")
    STOP_WORDS.add("alte")
    STOP_WORDS.add("altei")
    STOP_WORDS.add("alteia")
    STOP_WORDS.add("altele")
    STOP_WORDS.add("alteța-voastră")
    STOP_WORDS.add("alți")
    STOP_WORDS.add("alții")
    STOP_WORDS.add("altor")
    STOP_WORDS.add("altora")
    STOP_WORDS.add("altui")
    STOP_WORDS.add("altuia")
    STOP_WORDS.add("altul")
    STOP_WORDS.add("ălui")
    STOP_WORDS.add("ăluia")
    STOP_WORDS.add("anumit")
    STOP_WORDS.add("anumită")
    STOP_WORDS.add("anumite")
    STOP_WORDS.add("anumiți")
    STOP_WORDS.add("anumitor")
    STOP_WORDS.add("apud")
    STOP_WORDS.add("ar")
    STOP_WORDS.add("aș")
    STOP_WORDS.add("ast")
    STOP_WORDS.add("ăst")
    STOP_WORDS.add("asta")
    STOP_WORDS.add("astă")
    STOP_WORDS.add("ăsta")
    STOP_WORDS.add("aste")
    STOP_WORDS.add("astea")
    STOP_WORDS.add("ăstei")
    STOP_WORDS.add("ăsteia")
    STOP_WORDS.add("ăști")
    STOP_WORDS.add("ăștia")
    STOP_WORDS.add("ăștilalți")
    STOP_WORDS.add("ăstor")
    STOP_WORDS.add("ăstora")
    STOP_WORDS.add("ăstui")
    STOP_WORDS.add("ăstuia")
    STOP_WORDS.add("asupra")
    STOP_WORDS.add("asupră")
    STOP_WORDS.add("atât")
    STOP_WORDS.add("atâta")
    STOP_WORDS.add("atâtea")
    STOP_WORDS.add("atâți")
    STOP_WORDS.add("atâția")
    STOP_WORDS.add("atâtor")
    STOP_WORDS.add("atâtora")
    STOP_WORDS.add("ați")
    STOP_WORDS.add("ăți")
    STOP_WORDS.add("ca")
    STOP_WORDS.add("că")
    STOP_WORDS.add("căci")
    STOP_WORDS.add("cam")
    STOP_WORDS.add("când")
    STOP_WORDS.add("care")
    STOP_WORDS.add("cărei")
    STOP_WORDS.add("căreia")
    STOP_WORDS.add("careva")
    STOP_WORDS.add("carevasăzică")
    STOP_WORDS.add("cari")
    STOP_WORDS.add("căror")
    STOP_WORDS.add("cărora")
    STOP_WORDS.add("cărui")
    STOP_WORDS.add("căruia")
    STOP_WORDS.add("cât")
    STOP_WORDS.add("câta")
    STOP_WORDS.add("câtă")
    STOP_WORDS.add("câtăva")
    STOP_WORDS.add("câte")
    STOP_WORDS.add("câtelea")
    STOP_WORDS.add("câteva")
    STOP_WORDS.add("câți")
    STOP_WORDS.add("câțiva")
    STOP_WORDS.add("câtor")
    STOP_WORDS.add("câtora")
    STOP_WORDS.add("câtorva")
    STOP_WORDS.add("către")
    STOP_WORDS.add("câtva")
    STOP_WORDS.add("ce")
    STOP_WORDS.add("cea")
    STOP_WORDS.add("cealaltă")
    STOP_WORDS.add("ceastălaltă")
    STOP_WORDS.add("ceea")
    STOP_WORDS.add("cei")
    STOP_WORDS.add("ceia")
    STOP_WORDS.add("ceilalți")
    STOP_WORDS.add("cel")
    STOP_WORDS.add("cela")
    STOP_WORDS.add("celălalt")
    STOP_WORDS.add("cele")
    STOP_WORDS.add("celea")
    STOP_WORDS.add("celei")
    STOP_WORDS.add("celeia")
    STOP_WORDS.add("celeilalte")
    STOP_WORDS.add("celelalte")
    STOP_WORDS.add("celor")
    STOP_WORDS.add("celora")
    STOP_WORDS.add("celorlalte")
    STOP_WORDS.add("celorlalți")
    STOP_WORDS.add("celui")
    STOP_WORDS.add("celuia")
    STOP_WORDS.add("celuilalt")
    STOP_WORDS.add("cestălalt")
    STOP_WORDS.add("cesteilalte")
    STOP_WORDS.add("cestelalte")
    STOP_WORDS.add("ceștilalți")
    STOP_WORDS.add("cestorlalte")
    STOP_WORDS.add("cestorlalți")
    STOP_WORDS.add("cestuilalt")
    STOP_WORDS.add("ceva")
    STOP_WORDS.add("chiar")
    STOP_WORDS.add("ci")
    STOP_WORDS.add("cine")
    STOP_WORDS.add("cineva")
    STOP_WORDS.add("ciu-ciu")
    STOP_WORDS.add("conform")
    STOP_WORDS.add("contra")
    STOP_WORDS.add("contrar")
    STOP_WORDS.add("cu")
    STOP_WORDS.add("cui")
    STOP_WORDS.add("cuiva")
    STOP_WORDS.add("cum")
    STOP_WORDS.add("cutare")
    STOP_WORDS.add("cutare-cutare")
    STOP_WORDS.add("cutărei")
    STOP_WORDS.add("cutăreia")
    STOP_WORDS.add("cutărescu")
    STOP_WORDS.add("cutăror")
    STOP_WORDS.add("cutărora")
    STOP_WORDS.add("cutărui")
    STOP_WORDS.add("cutăruia")
    STOP_WORDS.add("dacă")
    STOP_WORDS.add("dăcât")
    STOP_WORDS.add("d-altă")
    STOP_WORDS.add("dâm")
    STOP_WORDS.add("dân")
    STOP_WORDS.add("dânsa")
    STOP_WORDS.add("dânsei")
    STOP_WORDS.add("dânsele")
    STOP_WORDS.add("dânselor")
    STOP_WORDS.add("dânșii")
    STOP_WORDS.add("dânșilor")
    STOP_WORDS.add("dânsul")
    STOP_WORDS.add("dânsului")
    STOP_WORDS.add("dar")
    STOP_WORDS.add("dară")
    STOP_WORDS.add("darămite")
    STOP_WORDS.add("darmite")
    STOP_WORDS.add("datorită")
    STOP_WORDS.add("de")
    STOP_WORDS.add("de-a")
    STOP_WORDS.add("deasupra")
    STOP_WORDS.add("decât")
    STOP_WORDS.add("deci")
    STOP_WORDS.add("dedesubtul")
    STOP_WORDS.add("deoarece")
    STOP_WORDS.add("deși")
    STOP_WORDS.add("despre")
    STOP_WORDS.add("destui")
    STOP_WORDS.add("destul")
    STOP_WORDS.add("destulă")
    STOP_WORDS.add("destule")
    STOP_WORDS.add("dicât")
    STOP_WORDS.add("dimprejurul")
    STOP_WORDS.add("din")
    STOP_WORDS.add("dinafara")
    STOP_WORDS.add("dinaintea")
    STOP_WORDS.add("dinapoia")
    STOP_WORDS.add("dinăuntrul")
    STOP_WORDS.add("dindărătul")
    STOP_WORDS.add("dinlăuntru")
    STOP_WORDS.add("dinlăuntrul")
    STOP_WORDS.add("dinspre")
    STOP_WORDS.add("dintre")
    STOP_WORDS.add("dintru")
    STOP_WORDS.add("dumisale")
    STOP_WORDS.add("dumitale")
    STOP_WORDS.add("dumneaei")
    STOP_WORDS.add("dumnealor")
    STOP_WORDS.add("dumnealui")
    STOP_WORDS.add("dumneasa")
    STOP_WORDS.add("dumneata")
    STOP_WORDS.add("dumneavoastră")
    STOP_WORDS.add("după")
    STOP_WORDS.add("ea")
    STOP_WORDS.add("ei")
    STOP_WORDS.add("el")
    STOP_WORDS.add("ele")
    STOP_WORDS.add("eu")
    STOP_WORDS.add("fără")
    STOP_WORDS.add("fiecare")
    STOP_WORDS.add("fiecărei")
    STOP_WORDS.add("fiecăreia")
    STOP_WORDS.add("fiecărui")
    STOP_WORDS.add("fiecăruia")
    STOP_WORDS.add("fiece")
    STOP_WORDS.add("fiindcă")
    STOP_WORDS.add("fitecine")
    STOP_WORDS.add("foarte")
    STOP_WORDS.add("grație")
    STOP_WORDS.add("iar")
    STOP_WORDS.add("iară")
    STOP_WORDS.add("iaste")
    STOP_WORDS.add("iea")
    STOP_WORDS.add("iei")
    STOP_WORDS.add("iel")
    STOP_WORDS.add("iele")
    STOP_WORDS.add("îi")
    STOP_WORDS.add("îl")
    STOP_WORDS.add("îmi")
    STOP_WORDS.add("împotriva")
    STOP_WORDS.add("împrejurul")
    STOP_WORDS.add("în")
    STOP_WORDS.add("înaintea")
    STOP_WORDS.add("înapoia")
    STOP_WORDS.add("înăuntrul")
    STOP_WORDS.add("încât")
    STOP_WORDS.add("încotro")
    STOP_WORDS.add("îndărătul")
    STOP_WORDS.add("înde")
    STOP_WORDS.add("înlăuntrul")
    STOP_WORDS.add("însa")
    STOP_WORDS.add("însă")
    STOP_WORDS.add("însămi")
    STOP_WORDS.add("însăși")
    STOP_WORDS.add("însăți")
    STOP_WORDS.add("însele")
    STOP_WORDS.add("însemi")
    STOP_WORDS.add("însene")
    STOP_WORDS.add("înseși")
    STOP_WORDS.add("înseți")
    STOP_WORDS.add("însevă")
    STOP_WORDS.add("înșii")
    STOP_WORDS.add("înșine")
    STOP_WORDS.add("înșiși")
    STOP_WORDS.add("înșivă")
    STOP_WORDS.add("înspre")
    STOP_WORDS.add("însul")
    STOP_WORDS.add("însumi")
    STOP_WORDS.add("însuși")
    STOP_WORDS.add("însuți")
    STOP_WORDS.add("întocmai")
    STOP_WORDS.add("intra")
    STOP_WORDS.add("între")
    STOP_WORDS.add("întru")
    STOP_WORDS.add("întrucât")
    STOP_WORDS.add("io")
    STOP_WORDS.add("îs")
    STOP_WORDS.add("își")
    STOP_WORDS.add("ista")
    STOP_WORDS.add("îți")
    STOP_WORDS.add("jur-împrejurul")
    STOP_WORDS.add("jurul")
    STOP_WORDS.add("la")
    STOP_WORDS.add("lângă")
    STOP_WORDS.add("le")
    STOP_WORDS.add("li")
    STOP_WORDS.add("lor")
    STOP_WORDS.add("lui")
    STOP_WORDS.add("mă")
    STOP_WORDS.add("mai")
    STOP_WORDS.add("mata")
    STOP_WORDS.add("matale")
    STOP_WORDS.add("matali")
    STOP_WORDS.add("mea")
    STOP_WORDS.add("mei")
    STOP_WORDS.add("mele")
    STOP_WORDS.add("meu")
    STOP_WORDS.add("mi")
    STOP_WORDS.add("mie")
    STOP_WORDS.add("mine")
    STOP_WORDS.add("mult")
    STOP_WORDS.add("multă")
    STOP_WORDS.add("multe")
    STOP_WORDS.add("mulți")
    STOP_WORDS.add("multor")
    STOP_WORDS.add("multora")
    STOP_WORDS.add("mulțumită")
    STOP_WORDS.add("ne")
    STOP_WORDS.add("necum")
    STOP_WORDS.add("nema")
    STOP_WORDS.add("ni")
    STOP_WORDS.add("nicăierea")
    STOP_WORDS.add("nicăieri")
    STOP_WORDS.add("nici")
    STOP_WORDS.add("nicicând")
    STOP_WORDS.add("nicicum")
    STOP_WORDS.add("nicidecât")
    STOP_WORDS.add("nicidecum")
    STOP_WORDS.add("nicio")
    STOP_WORDS.add("nici-o")
    STOP_WORDS.add("niciodată")
    STOP_WORDS.add("niciun")
    STOP_WORDS.add("nici-un")
    STOP_WORDS.add("niciuna")
    STOP_WORDS.add("nici-una")
    STOP_WORDS.add("niciunde")
    STOP_WORDS.add("niciunei")
    STOP_WORDS.add("nici-unei")
    STOP_WORDS.add("niciuneia")
    STOP_WORDS.add("nici-uneia")
    STOP_WORDS.add("niciunele")
    STOP_WORDS.add("nici-unele")
    STOP_WORDS.add("niciunii")
    STOP_WORDS.add("nici-unii")
    STOP_WORDS.add("niciunor")
    STOP_WORDS.add("nici-unor")
    STOP_WORDS.add("niciunora")
    STOP_WORDS.add("nici-unora")
    STOP_WORDS.add("niciunui")
    STOP_WORDS.add("nici-unui")
    STOP_WORDS.add("niciunuia")
    STOP_WORDS.add("nici-unuia")
    STOP_WORDS.add("niciunul")
    STOP_WORDS.add("nici-unul")
    STOP_WORDS.add("nimănui")
    STOP_WORDS.add("nimănuia")
    STOP_WORDS.add("nime")
    STOP_WORDS.add("nimenea")
    STOP_WORDS.add("nimeni")
    STOP_WORDS.add("nimic")
    STOP_WORDS.add("nimica")
    STOP_WORDS.add("nincs")
    STOP_WORDS.add("niscai")
    STOP_WORDS.add("niscaiva")
    STOP_WORDS.add("niște")
    STOP_WORDS.add("noastră")
    STOP_WORDS.add("noastre")
    STOP_WORDS.add("noi")
    STOP_WORDS.add("noștri")
    STOP_WORDS.add("nostru")
    STOP_WORDS.add("nouă")
    STOP_WORDS.add("nu")
    STOP_WORDS.add("numai-că")
    STOP_WORDS.add("o")
    STOP_WORDS.add("oare")
    STOP_WORDS.add("oarecare")
    STOP_WORDS.add("oarecari")
    STOP_WORDS.add("oarece")
    STOP_WORDS.add("oarecine")
    STOP_WORDS.add("oarecui")
    STOP_WORDS.add("oareșce")
    STOP_WORDS.add("oareșicând")
    STOP_WORDS.add("oareșicare")
    STOP_WORDS.add("oareșicum")
    STOP_WORDS.add("oi")
    STOP_WORDS.add("oiu")
    STOP_WORDS.add("om")
    STOP_WORDS.add("or")
    STOP_WORDS.add("ori")
    STOP_WORDS.add("oricare")
    STOP_WORDS.add("oricărei")
    STOP_WORDS.add("oricăreia")
    STOP_WORDS.add("oricăror")
    STOP_WORDS.add("oricărora")
    STOP_WORDS.add("oricărui")
    STOP_WORDS.add("oricăruia")
    STOP_WORDS.add("oricât")
    STOP_WORDS.add("oricâtă")
    STOP_WORDS.add("oricâte")
    STOP_WORDS.add("oricâți")
    STOP_WORDS.add("oricâtor")
    STOP_WORDS.add("orice")
    STOP_WORDS.add("oricine")
    STOP_WORDS.add("oricui")
    STOP_WORDS.add("orișicare")
    STOP_WORDS.add("orișicărei")
    STOP_WORDS.add("orișicăreia")
    STOP_WORDS.add("orișicărui")
    STOP_WORDS.add("orișicăruia")
    STOP_WORDS.add("orișicât")
    STOP_WORDS.add("orișicâtă")
    STOP_WORDS.add("orișicâte")
    STOP_WORDS.add("orișicâți")
    STOP_WORDS.add("orișicâtor")
    STOP_WORDS.add("orișice")
    STOP_WORDS.add("orișicine")
    STOP_WORDS.add("orișicui")
    STOP_WORDS.add("pă")
    STOP_WORDS.add("pân")
    STOP_WORDS.add("până")
    STOP_WORDS.add("până-n")
    STOP_WORDS.add("pân-la")
    STOP_WORDS.add("paracutare")
    STOP_WORDS.add("pe")
    STOP_WORDS.add("pentru")
    STOP_WORDS.add("per")
    STOP_WORDS.add("peste")
    STOP_WORDS.add("pi")
    STOP_WORDS.add("potrivit")
    STOP_WORDS.add("prea")
    STOP_WORDS.add("precum")
    STOP_WORDS.add("primprejurul")
    STOP_WORDS.add("prin")
    STOP_WORDS.add("printre")
    STOP_WORDS.add("printru")
    STOP_WORDS.add("privind")
    STOP_WORDS.add("pro")
    STOP_WORDS.add("puțin")
    STOP_WORDS.add("puțină")
    STOP_WORDS.add("puține")
    STOP_WORDS.add("puțini")
    STOP_WORDS.add("puținii")
    STOP_WORDS.add("relativ")
    STOP_WORDS.add("sa")
    STOP_WORDS.add("să")
    STOP_WORDS.add("săi")
    STOP_WORDS.add("sale")
    STOP_WORDS.add("sau")
    STOP_WORDS.add("său")
    STOP_WORDS.add("se")
    STOP_WORDS.add("si")
    STOP_WORDS.add("și")
    STOP_WORDS.add("șî")
    STOP_WORDS.add("sie")
    STOP_WORDS.add("sieși")
    STOP_WORDS.add("sii")
    STOP_WORDS.add("sine")
    STOP_WORDS.add("sineși")
    STOP_WORDS.add("spre")
    STOP_WORDS.add("sub")
    STOP_WORDS.add("ta")
    STOP_WORDS.add("tăi")
    STOP_WORDS.add("tale")
    STOP_WORDS.add("taman")
    STOP_WORDS.add("tău")
    STOP_WORDS.add("te")
    STOP_WORDS.add("ți")
    STOP_WORDS.add("ție")
    STOP_WORDS.add("tine")
    STOP_WORDS.add("toată")
    STOP_WORDS.add("toate")
    STOP_WORDS.add("toatele")
    STOP_WORDS.add("tot")
    STOP_WORDS.add("toți")
    STOP_WORDS.add("toții")
    STOP_WORDS.add("totu")
    STOP_WORDS.add("totul")
    STOP_WORDS.add("totului")
    STOP_WORDS.add("tu")
    STOP_WORDS.add("tuturor")
    STOP_WORDS.add("tuturora")
    STOP_WORDS.add("un")
    STOP_WORDS.add("una")
    STOP_WORDS.add("unde")
    STOP_WORDS.add("unei")
    STOP_WORDS.add("uneia")
    STOP_WORDS.add("unele")
    STOP_WORDS.add("unii")
    STOP_WORDS.add("unor")
    STOP_WORDS.add("unora")
    STOP_WORDS.add("unu")
    STOP_WORDS.add("unui")
    STOP_WORDS.add("unuia")
    STOP_WORDS.add("unul")
    STOP_WORDS.add("va")
    STOP_WORDS.add("vă")
    STOP_WORDS.add("vasăzică")
    STOP_WORDS.add("vei")
    STOP_WORDS.add("veți")
    STOP_WORDS.add("vi")
    STOP_WORDS.add("via")
    STOP_WORDS.add("voastră")
    STOP_WORDS.add("voastre")
    STOP_WORDS.add("voi")
    STOP_WORDS.add("voiu")
    STOP_WORDS.add("vom")
    STOP_WORDS.add("vor")
    STOP_WORDS.add("voștri")
    STOP_WORDS.add("vostru")
    STOP_WORDS.add("vouă")
    STOP_WORDS.add("vreo")
    STOP_WORDS.add("vre-o")
    STOP_WORDS.add("vreun")
    STOP_WORDS.add("vre-un")
    STOP_WORDS.add("vreuna")
    STOP_WORDS.add("vre-una")
    STOP_WORDS.add("vreunei")
    STOP_WORDS.add("vre-unei")
    STOP_WORDS.add("vreuneia")
    STOP_WORDS.add("vre-uneia")
    STOP_WORDS.add("vreunele")
    STOP_WORDS.add("vre-unele")
    STOP_WORDS.add("vreunii")
    STOP_WORDS.add("vre-unii")
    STOP_WORDS.add("vreunor")
    STOP_WORDS.add("vre-unor")
    STOP_WORDS.add("vreunora")
    STOP_WORDS.add("vre-unora")
    STOP_WORDS.add("vreunui")
    STOP_WORDS.add("vre-unui")
    STOP_WORDS.add("vreunuia")
    STOP_WORDS.add("vre-unuia")
    STOP_WORDS.add("vreunul")
    STOP_WORDS.add("vre-unul")

    def is_command_verb(self, verb_lemma):
        return verb_lemma.lower() in ["duce", "conduce", "arăta", "aduce"]

    def is_functional_pos(self, pos):
        return not re.match(r"^(N|P[^x]|M|R[gw]|Vm|Af|Y).*$", pos)

    def is_noun_pos(self, pos):
        """
        Some extensions for Romanian, to accommodate
        words such as "unde" and "când"
        :param pos:
        :return:
        """
        return re.match(r"^(N|P[^x]|M|Rw|Yn?).*$", pos)

    def is_pure_noun_pos(self, pos):
        return re.match(r"^(N|Yn?).*$", pos)

    def is_skippable_pos(self, pos):
        return pos.startswith("Sp") or pos.startswith("C") or pos.startswith("I")

    def is_functional_word(self, word):
        return word.lower() in RoLexicon.STOP_WORDS
